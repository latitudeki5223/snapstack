# 🎯 Parser Studio - Working Implementation

## Overview

A fully functional, generic product parser that can handle ANY product type - from iPhones to unicorn onesies! No category assumptions, just intelligent token extraction.

## ✨ Features

- **Truly Generic**: Works with any product - electronics, food, clothing, tools, books, anything!
- **Multi-layer Token Extraction**:
  - Exact phrases (quoted text)
  - Measurements (32oz, 256GB, 6mm)
  - Model numbers (M3, WH-1000XM5)
  - Brand names (capitalized words)
  - Numbers and keywords
- **Visual Interface**: Two-panel React app showing input and parsed results
- **Confidence Scoring**: See how confident the parser is about each token
- **Example Library**: 50+ examples across 8 categories for quick testing

## 🚀 Quick Start

### Option 1: Simple Script (Recommended)
```bash
./start-parser-studio.sh
```
Then open http://localhost:5173 in your browser.

### Option 2: Manual Start
```bash
# Terminal 1 - Backend
cd apps/backend
pip3 install flask flask-cors
python3 app.py

# Terminal 2 - Frontend
cd apps/web
npm install
npm run dev
```

### Option 3: Using TurboRepo
```bash
npm install
turbo dev --filter=web --filter=backend
```

## 🧪 Test Examples

Try these in the Parser Studio:

**Electronics:**
- `iPhone 15 Pro 256GB`
- `Samsung 65 inch OLED TV`

**Kitchen:**
- `instant pot 6 quart`
- `ninja blender 1000 watts`

**Fashion:**
- `red dress size 8`
- `Nike Air Max 90 size 10`

**Random:**
- `that thing from tiktok`
- `unicorn onesie adult medium`

**Books:**
- `"Atomic Habits" by James Clear`

## 📁 Project Structure

```
packages/parser/src/
└── parser.py          # Generic parser implementation

apps/backend/
├── app.py            # Flask API with /api/admin/parser/test endpoint
└── requirements.txt  # Python dependencies

apps/web/src/
├── pages/admin/
│   └── ParserStudio.tsx  # React interface
├── App.tsx
└── main.tsx
```

## 🔧 How It Works

1. **Token Extraction**: The parser extracts meaningful tokens without assuming product categories
2. **Priority Ranking**: Tokens are ranked by type (measurements > brands > keywords)
3. **Search Query Building**: High-priority tokens are combined into search queries
4. **Confidence Scoring**: Each token gets a confidence score based on its type

## 🎨 Parser Logic

```python
# No category assumptions!
"iPhone 15 Pro 256GB" → 
  Tokens: [256GB (measurement), 15 (number), Pro (brand), iPhone (keyword)]
  Search: "256GB 15 Pro iPhone"

"purple yoga mat 6mm thick" →
  Tokens: [6mm (measurement), purple, yoga, mat, thick (keywords)]
  Search: "6mm purple yoga mat"

"that thing from tiktok" →
  Tokens: [that, thing, tiktok (keywords)]
  Search: "that thing tiktok"  # Let the search API figure it out!
```

## 🔑 Key Insight

We don't need to understand WHAT the product is - just extract the meaningful parts for searching. The APIs (Sovrn, Amazon, eBay) are much better at:
- Product categorization
- Fuzzy matching
- Spell correction
- Finding the actual products

## 📊 API Endpoints

- `POST /api/admin/parser/test` - Test parser with text
- `GET /api/admin/parser/examples` - Get example inputs
- `GET /api/health` - Health check

## 🚦 Next Steps

1. **Add NLP Layer**: Integrate spaCy for better entity recognition
2. **Add LLM Fallback**: Use OpenAI for ambiguous inputs
3. **Caching**: Store parsed results in PostgreSQL with pgvector
4. **Performance**: Add Redis caching for repeated queries
5. **Analytics**: Track which tokens lead to successful purchases

## 🐛 Troubleshooting

**Port already in use:**
```bash
# Kill existing processes
lsof -ti:5000 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend
```

**Module not found:**
```bash
pip3 install flask flask-cors
cd apps/web && npm install
```

**CORS errors:**
Make sure the Flask backend is running on port 5000.

---

The parser is **working and ready to use**! Just run `./start-parser-studio.sh` and start testing with any product text you can imagine.