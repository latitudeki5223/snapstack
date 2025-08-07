# SnapStack Project Context

## 🚨 CRITICAL RULES
- Mobile-first React Native + Expo for iOS/Android
- Flask backend with PostgreSQL + pgvector
- Hybrid parser: regex → spaCy → OpenAI fallback
- Dual-mode checkout: Affiliate (default) + Stripe (curated)
- Monorepo with TurboRepo for all services
- Private commercial codebase - maintain confidentiality
- ALWAYS run bin/verify before committing code

## 🎯 PROJECT OVERVIEW
SnapStack is an AI-powered smart shopping assistant that:
1. Parses user lists (paste/type/voice) for ANY products (not just supplements)
2. Matches products to live vendor APIs (Sovrn primary, then Amazon, eBay, direct)
3. Compares prices and metadata across vendors
4. Enables one-click checkout (affiliate or unified Stripe)
5. Tracks orders and routes support to vendors

Core value: Turn any list into a price-compared, ready-to-buy cart in seconds.

## 📁 MONOREPO STRUCTURE
```
snapstack/
├── apps/
│   ├── web/          # Vite + React + Tailwind
│   ├── mobile/       # React Native + Expo
│   └── backend/      # Flask + PostgreSQL API
├── packages/
│   ├── parser/       # Shared parsing logic (Python + TS)
│   ├── ui/           # Shared React components
│   ├── types/        # TypeScript definitions
│   └── utils/        # Helper functions, formatters
├── bin/
│   └── verify        # Quality check script
└── PROJECT_GUIDE.md  # Master documentation
```

## 🔧 DEVELOPMENT PATTERNS

### Parser Architecture (3-Layer Hybrid)
1. Regex Layer (0-5ms): Known patterns, instant return
2. NLP Layer (5-50ms): spaCy entity recognition
3. LLM Layer (200-500ms): OpenAI for ambiguous (cached)
- Target: 95% accuracy, <60% cache hit rate after month 1

### API Integration Priority
1. Sovrn Commerce: Primary (40,000+ merchants)
2. Direct vendor APIs: Secondary (better margins)
3. Never scrape unless absolutely necessary
- Implement exponential backoff and rate limiting

### Testing Requirements
- Parser: 95% accuracy on real-world corpus
- API: Mock all vendor responses
- UI: Component tests + visual regression
- Coverage: 80% minimum

## 🏗️ BUILD COMMANDS
```bash
turbo dev         # Start all services
turbo build       # Build all packages
turbo test        # Run all tests
turbo lint        # Lint all code
bin/verify        # Pre-commit checks
```

## 🚀 DEPLOYMENT
- Backend: GCP Cloud Run
- Web: Vercel
- Mobile: Expo EAS
- Database: Cloud SQL with pgvector
- CI/CD: GitHub Actions on merge to main

## 💼 BUSINESS LOGIC
- Phase 1: Affiliate checkout only (0-3 months)
- Phase 2: Single vendor unified checkout (3-6 months)
- Phase 3: Multi-vendor unified checkout (6+ months)
- Track: Parse accuracy, conversion, GMV, commission rates

## 🎨 BRAND & UX
- Mascot: Stackie the Alligator
- Colors: Jungle green (#10B981), orange (#FB923C)
- Voice: Helpful, upbeat, shopping-savvy
- Key phrase: "Let me stack that for you!"
- Mobile-first: Every interaction optimized for thumb
- Micro-interactions: Add to cart animations, price drops

## 📊 KEY METRICS
- User: Activation, retention, conversion funnel
- Technical: Parser accuracy, API uptime, cache hit rate
- Business: GMV, commission rate, CAC/LTV

## 🔒 SECURITY
- API keys in environment variables only
- PostgreSQL encryption at rest
- Stripe handles all PCI compliance
- Rate limiting on all endpoints

## 📚 DOCUMENTATION
- PROJECT_GUIDE.md: Master documentation
- Custom commands in .claude/commands/
- OpenAPI spec for all endpoints
- Component Storybook for UI