# 🚀 SnapStack

> AI-powered smart shopping assistant that transforms any list into a price-compared, ready-to-buy shopping cart in seconds.

[![TurboRepo](https://img.shields.io/badge/Built%20with-TurboRepo-blue)](https://turbo.build)
[![Claude Code](https://img.shields.io/badge/AI%20Powered-Claude%20Code-orange)](https://claude.ai)

## 📖 Documentation

**→ See [PROJECT_GUIDE.md](./PROJECT_GUIDE.md) for complete documentation**

## 🏃 Quick Start

```bash
# Install dependencies
npm install

# Start all services in development mode
npm run dev

# Run quality checks before committing
npm run verify
```

## 🏗️ Project Structure

```
snapstack/
├── apps/
│   ├── web/        # Vite + React + Tailwind
│   ├── mobile/     # React Native + Expo
│   └── backend/    # Flask + PostgreSQL
├── packages/
│   ├── parser/     # Hybrid parsing engine
│   ├── ui/         # Shared components
│   ├── types/      # TypeScript definitions
│   └── utils/      # Helper functions
└── PROJECT_GUIDE.md # Master documentation
```

## 🎯 Core Features

- **Smart Parser**: Hybrid 3-layer parsing (regex → NLP → LLM)
- **Price Comparison**: Real-time prices from 40,000+ merchants
- **Dual Checkout**: Affiliate links or unified Stripe payment
- **Mobile-First**: Native iOS/Android apps with Expo
- **Monorepo**: TurboRepo for efficient builds

## 🛠️ Development

```bash
# Run specific app
npm run dev -- --filter=web
npm run dev -- --filter=mobile
npm run dev -- --filter=backend

# Build everything
npm run build

# Run tests
npm run test

# Lint code
npm run lint
```

## 🤖 Claude Code Integration

This repository uses Claude Code GitHub Actions. Mention `@claude` in:
- Pull requests
- Issues  
- Code reviews

Claude will automatically:
- Write code and create PRs
- Review code for improvements
- Fix bugs
- Refactor based on instructions

### Setup Claude Code

1. Add `ANTHROPIC_API_KEY` to repository secrets
2. Enable GitHub Actions
3. Mention `@claude` in any issue or PR

## 📊 Status

- Phase 1: Foundation ✅
- Phase 2: Parser Core 🚧
- Phase 3: API Integrations ⏳
- Phase 4: Core UI ⏳
- Phase 5: Cart & Checkout ⏳
- Phase 6: Polish & Launch ⏳

## 🔗 Links

- [Project Guide](./PROJECT_GUIDE.md)
- [Claude Context](./CLAUDE.md)
- [TurboRepo Docs](https://turbo.build/repo/docs)
- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)

## 📄 License

Private commercial codebase - All rights reserved

---

*Built with ❤️ by the SnapStack team*