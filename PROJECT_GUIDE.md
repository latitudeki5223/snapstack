# SnapStack Project Guide - Master Document

## Project Overview

SnapStack is an AI-powered smart shopping assistant that transforms how users find and compare products online. Users paste, speak, or type product lists, and we parse, match, compare prices across vendors, and enable streamlined checkout experiences.

**Core Value Proposition**: Turn any list into a price-compared, ready-to-buy shopping cart in seconds.

### Technology Stack
- **Monorepo**: TurboRepo for build orchestration and caching
- **Mobile**: React Native + Expo (iOS/Android)
- **Web**: Vite + React + Tailwind CSS
- **Backend**: Flask + PostgreSQL with pgvector
- **Parser**: Python hybrid (regex → spaCy → OpenAI)
- **Infrastructure**: Docker, Traefik, GCP Cloud Run
- **APIs**: Sovrn Commerce (primary), direct vendor APIs, Amazon PA-API, eBay

### Business Model
- **Primary**: Affiliate commissions (2-10%) via Sovrn and direct partnerships
- **Secondary**: Optional Stripe checkout with markup for curated bundles
- **Future**: Sponsored placements, premium features, white-label platform

## Monorepo Architecture

```
snapstack/
├── apps/
│   ├── web/                 # Vite + React + Tailwind
│   ├── mobile/              # React Native + Expo
│   └── backend/             # Flask API + PostgreSQL
├── packages/
│   ├── parser/              # Shared parsing logic (Python/TS interfaces)
│   ├── ui/                  # Shared React components
│   ├── types/               # TypeScript definitions
│   └── utils/               # Helper functions, formatters
├── docker/                  # Compose files, Dockerfiles
├── .github/
│   └── workflows/           # CI/CD pipelines
├── .claude/
│   ├── commands/            # Custom Claude commands
│   └── CLAUDE.md           # Project context
├── docs/
│   ├── plans/              # Feature planning docs
│   ├── architecture/       # Technical decisions
│   └── ui-ux/             # Design system docs
├── bin/
│   └── verify              # Quality check script
├── turbo.json              # TurboRepo config
└── package.json            # Root package management
```

## Development Workflow

### Quick Start
```bash
# Install dependencies
npm install

# Start all services in dev mode
turbo dev

# Run quality checks before committing
bin/verify

# Run specific app
turbo dev --filter=web
turbo dev --filter=mobile
turbo dev --filter=backend
```

### TurboRepo Commands
```bash
turbo build      # Build all packages
turbo test       # Run all tests
turbo lint       # Lint all code
turbo typecheck  # TypeScript validation
turbo clean      # Clean all build artifacts
```

### Git Workflow
- Branch naming: `feat/parser-improvements`, `fix/cart-calculation`, `ui/mobile-comparison`
- Commit format: `type(scope): description` (e.g., `feat(parser): add electronics category support`)
- PR process: Squash merge to main, each merge = complete feature
- CI/CD: Automatic deployment on merge to main

### Quality Gates (bin/verify)
- Linting: ESLint for JS/TS, Black for Python
- Type checking: TypeScript strict mode
- Testing: Unit tests must pass (target 80% coverage)
- Build: All packages must build successfully
- Security: npm audit for vulnerabilities

## Parser Architecture

### Three-Layer Hybrid Approach
```
User Input → Normalizer → Parser Pipeline → Validator → Structured Output
              ↓               ↓                ↓            ↓
         (clean text)    (confidence score)  (verify)   (product list)

Parser Pipeline:
1. Regex Layer (0-5ms) - Known patterns, instant return if confident
2. NLP Layer (5-50ms) - spaCy entity recognition for semi-structured
3. LLM Layer (200-500ms) - OpenAI for ambiguous cases (cached)
```

### Parser Input/Output
Input Examples:
- "iPhone 15 Pro Max 256GB"
- "Nike Air Max 90 size 10"
- "Samsung 65 inch OLED TV"
- "organic almonds 2 pounds"

Output Structure:
```python
{
    "products": [
        {
            "raw_text": "iPhone 15 Pro Max 256GB",
            "parsed": {
                "name": "iPhone 15 Pro Max",
                "category": "electronics",
                "attributes": {
                    "storage": "256GB",
                    "color": null,
                    "model": "15 Pro Max"
                }
            },
            "confidence": 0.95,
            "parser_used": "regex"
        }
    ],
    "total_confidence": 0.95,
    "parsing_time_ms": 3
}
```

### Caching Strategy
- PostgreSQL + pgvector: Store all parsed results
- Similarity matching: Find similar previous parses
- TTL: 7 days for product matches, 30 days for parse patterns
- Cache hit target: >60% after first month

## API Integration Strategy

### Primary: Sovrn Commerce
```python
class SovrnAdapter:
    """
    Primary product search and affiliate link generation
    - Covers 40,000+ merchants
    - Real-time pricing
    - Unified API for multiple vendors
    """
    async def search(query: str) -> List[Product]
    async def get_affiliate_link(product: Product) -> str
```

### Secondary: Direct Vendor APIs
```python
# Implement adapters for top vendors
adapters = {
    "amazon": AmazonPAAPIAdapter(),
    "ebay": EbayBrowseAdapter(),
    "walmart": WalmartAdapter(),
    # Add more as needed
}
```

### Fallback Chain
1. Try Sovrn Commerce API
2. Try direct vendor API if available
3. Return best available results
4. Never scrape unless absolutely necessary

### Rate Limiting & Retry Logic
```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def fetch_with_retry(adapter, query):
    return await adapter.search(query)
```

## UI Design System

### Core Design Principles
1. Mobile-first: Every interaction optimized for thumb reach
2. Information density: Show maximum value in minimum space
3. Progressive disclosure: Details on demand, not upfront
4. Visual hierarchy: Price and savings always prominent
5. Delightful interactions: Micro-animations for feedback

### Component Library Structure
```typescript
// packages/ui/components/

// Core Components
Button/
Card/
Modal/
Badge/
Input/

// Product Components
ProductCard/
  ├── ProductCard.tsx         // Main component
  ├── ProductCard.styles.ts   // Tailwind styles
  ├── ProductCard.test.tsx    // Tests
  └── ProductCard.stories.tsx // Storybook

ComparisonModal/
  ├── ComparisonTable.tsx
  ├── VendorRow.tsx
  └── PriceHighlight.tsx

StackBuilder/
  ├── StackList.tsx
  ├── StackItem.tsx
  ├── DragHandle.tsx
  └── GroupHeader.tsx

Cart/
  ├── CartSummary.tsx
  ├── VendorGroup.tsx
  └── CheckoutButton.tsx
```

### Design Tokens
```css
/* colors */
--primary: #10B981;        /* Jungle green */
--primary-dark: #059669;
--accent: #FB923C;         /* Snap orange */
--background: #FFFFFF;
--surface: #F9FAFB;
--text-primary: #111827;
--text-secondary: #6B7280;
--success: #10B981;
--warning: #F59E0B;
--error: #EF4444;

/* spacing */
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;

/* typography */
--font-primary: 'Inter', system-ui;
--font-rounded: 'Nunito', sans-serif;
```

### Mobile Patterns
- Bottom sheets for actions and filters
- Swipe gestures for delete/archive
- Pull-to-refresh for price updates
- Floating action button for paste/voice input
- Tab bar for main navigation

### Web Patterns
- Responsive grid that adapts from mobile to desktop
- Keyboard shortcuts for power users
- Hover states with additional information
- Modal overlays for comparison views
- Persistent sidebar on desktop for cart

## UX Flow & Interactions

### Core User Journey
```
1. Input → 2. Parse → 3. Match → 4. Compare → 5. Stack → 6. Checkout
   (3s)      (1s)       (2s)       (user)       (user)      (redirect)
```

### Input Methods

**Paste (Primary)**
- Large textarea with placeholder examples
- Auto-detect clipboard content
- Parse on paste with loading state

**Voice (Mobile)**
- Hold-to-talk button
- Real-time transcription display
- Confirmation before parsing

**Type (Fallback)**
- Search-as-you-type with debouncing
- Autocomplete from previous searches
- Category hints

### Product Matching UX
Loading States:
1. Skeleton cards while fetching
2. Progressive loading (show results as they arrive)
3. "Finding best prices..." animation

Result Display:
- Best price highlighted with badge
- Savings percentage prominent
- Vendor logos for trust
- "Compare X offers" button

### Comparison Modal
```
┌─────────────────────────────────┐
│ iPhone 15 Pro Max 256GB         │
│ ┌─────────────────────────────┐ │
│ │ ✓ Amazon    $1,199  Save $50│ │
│ │   eBay      $1,229  -       │ │
│ │   Best Buy  $1,249  -       │ │
│ └─────────────────────────────┘ │
│ [Select] [More Info] [Close]    │
└─────────────────────────────────┘
```

### Stack Building
- Drag & drop to reorder
- Swipe right to save for later
- Swipe left to remove
- Group by: Category, vendor, or custom
- Inline edit: Quantity adjustment with +/- buttons

## Cart & Checkout

### Dual-Mode Checkout UX

**Mode 1: QuickStack (Affiliate)**
```
┌─────────────────────────────────┐
│ Your Stack (3 items)            │
│ ─────────────────────────────── │
│ Total: $459.97                  │
│ You save: $67.43 (12%)         │
│                                 │
│ [🟢 Checkout at Each Store]     │
│ "Best prices, separate orders"  │
└─────────────────────────────────┘
```

**Mode 2: OneClick (Stripe)**
```
┌─────────────────────────────────┐
│ Your Stack (3 items)            │
│ ─────────────────────────────── │
│ Total: $469.97                  │
│ You save: $57.43 (10%)         │
│                                 │
│ [🟠 One Payment - We Handle It] │
│ "Single checkout, we order all" │
└─────────────────────────────────┘
```

### Micro-interactions
- Add to stack: Item flies to cart with number badge update
- Price drop: Pulse animation with green highlight
- Remove item: Fade out with undo option (5s)
- Quantity change: Smooth number transition
- Success state: Stackie animation with confetti

### Error Handling UX
- No results: Suggest alternatives or broader search
- API timeout: Show cached results with "Prices from [time]"
- Parse failure: Show what we understood, ask for clarification
- Network error: Offline mode with saved stacks

## Payment Aggregation Strategy

### The Game-Changing Feature
The unified checkout is our key differentiator but requires careful implementation:

### Technical Architecture
```python
class CheckoutOrchestrator:
    """
    Handles the complex multi-vendor checkout flow
    """
    async def process_unified_checkout(cart: Cart):
        # 1. Charge customer via Stripe
        charge = await stripe.create_charge(cart.total)
        
        # 2. Place orders with each vendor
        orders = []
        for vendor_group in cart.vendor_groups:
            if vendor_group.supports_api_checkout:
                order = await place_api_order(vendor_group)
            else:
                order = await queue_manual_order(vendor_group)
            orders.append(order)
        
        # 3. Track all orders
        await create_order_tracking(orders)
        
        # 4. Handle failures with refunds
        if any_failed(orders):
            await handle_partial_failure(charge, orders)
```

### Risk Mitigation
- Start with trusted vendors only
- Implement spending limits ($500/order initially)
- Manual review queue for suspicious orders
- Automated refund system for failures
- Clear terms of service about our role as purchasing agent

### Progressive Rollout
1. Phase 1: Affiliate only (0-3 months)
2. Phase 2: Unified checkout for single vendor (3-6 months)
3. Phase 3: Multi-vendor unified checkout (6+ months)
4. Phase 4: Subscription/recurring orders (12+ months)

## Code Style Guide

### TypeScript/React
```typescript
// Use functional components with TypeScript
interface ProductCardProps {
  product: Product;
  onSelect: (product: Product) => void;
  isSelected?: boolean;
}

export const ProductCard: FC<ProductCardProps> = ({ 
  product, 
  onSelect, 
  isSelected = false 
}) => {
  // Early returns for edge cases
  if (!product) return null;
  
  // Destructure for clarity
  const { name, price, vendor, savings } = product;
  
  // Event handlers as const arrows
  const handleClick = useCallback(() => {
    onSelect(product);
  }, [product, onSelect]);
  
  return (
    <Card 
      onClick={handleClick}
      className={cn(
        "transition-all cursor-pointer",
        isSelected && "ring-2 ring-primary"
      )}
    >
      {/* Component JSX */}
    </Card>
  );
};
```

### Python/Flask
```python
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class ParseResult:
    """Structured parsing result with confidence scoring"""
    products: List[Product]
    confidence: float
    parser_used: str
    parsing_time_ms: int
    
class ParserService:
    """
    Hybrid parser with fallback chain
    """
    async def parse(self, text: str) -> ParseResult:
        # Try regex first (fastest)
        if result := self._try_regex(text):
            return result
            
        # Try NLP (medium speed)
        if result := self._try_nlp(text):
            return result
            
        # Fallback to LLM (slowest but most flexible)
        return await self._try_llm(text)
    
    def _try_regex(self, text: str) -> Optional[ParseResult]:
        """Pattern matching for known formats"""
        patterns = [
            r'(?P<product>[\w\s]+)\s+(?P<quantity>\d+)',
            # Add more patterns
        ]
        # Implementation
```

### Testing Standards
```typescript
// Component tests
describe('ProductCard', () => {
  it('should display product information', () => {
    const product = mockProduct();
    render(<ProductCard product={product} onSelect={jest.fn()} />);
    
    expect(screen.getByText(product.name)).toBeInTheDocument();
    expect(screen.getByText(`${product.price}`)).toBeInTheDocument();
  });
  
  it('should call onSelect when clicked', () => {
    const onSelect = jest.fn();
    const product = mockProduct();
    
    render(<ProductCard product={product} onSelect={onSelect} />);
    fireEvent.click(screen.getByRole('article'));
    
    expect(onSelect).toHaveBeenCalledWith(product);
  });
});
```

## Development Phases

### Phase 1: Foundation (Weeks 1-2) ✅
- [x] Monorepo setup with TurboRepo
- [x] Basic project structure
- [x] Claude Code integration
- [x] Core type definitions
- [ ] Docker development environment

### Phase 2: Parser Core (Weeks 3-4) 🚧
- [ ] Regex pattern library for common products
- [ ] spaCy integration for NLP
- [ ] OpenAI fallback with caching
- [ ] Parser API endpoints
- [ ] 95% accuracy on test corpus

### Phase 3: API Integrations (Weeks 5-6)
- [ ] Sovrn Commerce adapter
- [ ] Amazon PA-API adapter
- [ ] eBay Browse API adapter
- [ ] Parallel fetching orchestrator
- [ ] Rate limiting and retry logic

### Phase 4: Core UI (Weeks 7-9)
- [ ] Component library setup
- [ ] Product card component
- [ ] Comparison modal
- [ ] Stack builder interface
- [ ] Mobile app shell

### Phase 5: Cart & Checkout (Weeks 10-11)
- [ ] Cart state management
- [ ] Affiliate link generation
- [ ] Checkout flow (affiliate mode)
- [ ] Order tracking UI
- [ ] Support routing

### Phase 6: Polish & Launch (Weeks 12-14)
- [ ] Stackie animations
- [ ] Performance optimization
- [ ] Error handling
- [ ] Analytics integration
- [ ] Beta testing

### Phase 7: Unified Checkout (Post-MVP)
- [ ] Stripe integration
- [ ] Order orchestration
- [ ] Manual order queue
- [ ] Refund automation
- [ ] Advanced tracking

## Testing Strategy

### Testing Pyramid
```
         /\
        /E2E\       (5%) - Critical user journeys
       /──────\
      /  Integ  \   (20%) - API integrations, parser accuracy
     /────────────\
    /     Unit      \ (75%) - Components, utilities, business logic
   /──────────────────\
```

### Parser Testing
```python
# Test corpus with real-world examples
test_cases = [
    ("iPhone 15 Pro 256GB", {"name": "iPhone 15 Pro", "storage": "256GB"}),
    ("Nike Air Max size 10", {"name": "Nike Air Max", "size": "10"}),
    # 1000+ test cases covering edge cases
]

# Accuracy metrics
def test_parser_accuracy():
    correct = 0
    for input_text, expected in test_cases:
        result = parser.parse(input_text)
        if matches(result, expected):
            correct += 1
    
    accuracy = correct / len(test_cases)
    assert accuracy >= 0.95  # 95% accuracy requirement
```

### API Integration Testing
```python
@pytest.mark.asyncio
async def test_sovrn_adapter():
    adapter = SovrnAdapter()
    
    # Test with mocked responses
    with mock_sovrn_api():
        results = await adapter.search("iPhone")
        assert len(results) > 0
        assert all(r.price > 0 for r in results)
```

### UI Component Testing
- Unit tests: Each component in isolation
- Integration tests: Component interactions
- Visual regression: Storybook + Chromatic
- Accessibility: aXe automated testing

## Monitoring & Analytics

### Key Metrics

**User Metrics**
- Activation: First successful parse → checkout
- Retention: Daily/weekly active users
- Conversion funnel: Input → Parse → Compare → Cart → Checkout
- Stack reuse: Saved stacks used multiple times

**Technical Metrics**
- Parser accuracy: Confidence scores, user corrections
- API performance: Response times, success rates
- Cache hit rate: Parser and product caches
- Error rates: By component and error type

**Business Metrics**
- GMV: Gross merchandise value routed
- Commission rate: Average across vendors
- CAC/LTV: Customer acquisition cost vs lifetime value
- Vendor performance: Which vendors convert best

### Monitoring Stack
```yaml
# docker-compose.monitoring.yml
services:
  prometheus:
    image: prom/prometheus
    
  grafana:
    image: grafana/grafana
    
  sentry:
    # Error tracking
    
  posthog:
    # Product analytics
```

## Security & Compliance

### Security Measures
- API Keys: Environment variables, never in code
- User Data: Encrypted at rest (PostgreSQL encryption)
- Payment Data: Never stored, Stripe handles PCI compliance
- Rate Limiting: On our API to prevent abuse
- Input Sanitization: Prevent injection attacks

### Privacy Compliance
- Data minimization: Only collect what's needed
- User consent: Clear privacy policy
- Data deletion: User can request deletion
- No selling data: Revenue from commissions only

## Deployment Strategy

### Environments
```
Development → Staging → Production
(local)       (GCP)      (GCP + CloudFlare)
```

### CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: turbo test
      
  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: |
          gcloud run deploy snapstack-api \
            --source apps/backend \
            --region us-central1
            
  deploy-web:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: |
          cd apps/web
          vercel --prod
```

### Infrastructure as Code
```terraform
# infrastructure/main.tf
resource "google_cloud_run_service" "api" {
  name     = "snapstack-api"
  location = "us-central1"
  
  template {
    spec {
      containers {
        image = "gcr.io/snapstack/api"
        
        resources {
          limits = {
            cpu    = "2"
            memory = "2Gi"
          }
        }
      }
    }
  }
}
```

## Documentation Standards

### Code Documentation
```python
def parse_product_list(text: str) -> ParseResult:
    """
    Parse user input into structured product list.
    
    Uses three-layer approach:
    1. Regex for known patterns (fastest)
    2. NLP for semi-structured (accurate)
    3. LLM for ambiguous (flexible)
    
    Args:
        text: Raw user input (paste, voice, or typed)
        
    Returns:
        ParseResult with products, confidence, and metadata
        
    Example:
        >>> parse_product_list("iPhone 15 Pro 256GB")
        ParseResult(
            products=[Product(name="iPhone 15 Pro", ...)],
            confidence=0.95,
            parser_used="regex"
        )
    """
```

### API Documentation
- OpenAPI/Swagger spec for all endpoints
- Postman collection for testing
- README in each package with examples

## Future Roadmap

### Near-term (3-6 months)
- Voice input optimization
- Barcode scanning
- Price tracking/alerts
- Social features (share stacks)
- Browser extension

### Medium-term (6-12 months)
- Unified checkout for all vendors
- Subscription management
- Price prediction ML
- Personalized recommendations
- White-label platform

### Long-term (12+ months)
- International expansion
- B2B procurement platform
- API marketplace for developers
- AI shopping assistant (chat)
- Predictive reordering

## Appendix: Quick Reference

### Common Commands
```bash
# Development
turbo dev                    # Start everything
turbo dev --filter=web      # Start specific app
bin/verify                  # Run quality checks

# Testing
turbo test                  # Run all tests
turbo test --filter=parser # Test specific package

# Deployment
./deploy.sh staging        # Deploy to staging
./deploy.sh production     # Deploy to production

# Database
cd apps/backend
flask db migrate          # Create migration
flask db upgrade          # Apply migrations
```

### Environment Variables
```env
# .env.local
DATABASE_URL=postgresql://localhost/snapstack
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=sk-...
SOVRN_API_KEY=...
STRIPE_SECRET_KEY=sk_test_...
SENTRY_DSN=...
```

### Useful Links
- [Sovrn Commerce API Docs](https://developers.sovrn.com)
- [TurboRepo Documentation](https://turbo.build/repo/docs)
- [React Native + Expo Guide](https://docs.expo.dev)
- [Flask Best Practices](https://flask.palletsprojects.com)

---

*This is a living document. Update it as the project evolves.*