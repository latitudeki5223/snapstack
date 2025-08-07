# SnapStack Project Context

## 🚨 CRITICAL RULES
- Mobile-first React Native + Expo for iOS/Android
- Flask backend with PostgreSQL + pgvector
- Hybrid parser: regex → spaCy → OpenAI fallback
- Dual-mode checkout: Affiliate (default) + Stripe (curated)
- Monorepo with TurboRepo for all services
- Private commercial codebase - maintain confidentiality

## 🎯 PROJECT OVERVIEW
SnapStack is an AI-powered smart shopping assistant that:
1. Parses user lists (paste/type/voice) for products
2. Matches products to live vendor APIs (Sovrn, Amazon, eBay, iHerb)
3. Compares prices and metadata across vendors
4. Enables one-click checkout (affiliate or unified Stripe)
5. Tracks orders and routes support to vendors

Starting with supplements, expanding to groceries, insurance, utilities.

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
│   └── types/        # TypeScript definitions
```

## 🔧 DEVELOPMENT PATTERNS

### Parser Architecture
1. Rule-based regex for known patterns (fast)
2. spaCy NLP for entity recognition (accurate)
3. OpenAI for ambiguous cases (flexible)
4. Cache all results in PostgreSQL with pgvector

### API Integration Priority
1. Sovrn Commerce (broad affiliate coverage)
2. Direct vendor APIs (better data/margins)
3. Fallback scraping only if necessary

### Testing Requirements
- Parser: 95% accuracy on supplement formats
- API: Mock all vendor responses
- UI: Snapshot tests for all components
- E2E: Critical user flows only

## 🏗️ BUILD COMMANDS
- `turbo dev` - Start all services in dev mode
- `turbo build` - Build all packages
- `turbo test` - Run all tests
- `turbo lint` - Lint all code

## 🚀 DEPLOYMENT
- Backend: GCP Cloud Run
- Web: Vercel
- Mobile: Expo EAS
- Database: Cloud SQL with pgvector

## 💼 BUSINESS LOGIC
- Default to affiliate checkout (low risk)
- Stripe only for curated/sponsored bundles
- Track everything: parsing accuracy, conversion, vendor performance
- Optimize for mobile conversion rate

## 🎨 BRAND
- Mascot: Stackie the Alligator
- Colors: Jungle green, white, accent orange
- Voice: Helpful, upbeat, shopping-savvy
- Key phrase: "Let me stack that for you!"