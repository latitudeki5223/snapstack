# 🎯 SnapStack Admin Dashboard

## Overview

A fully functional admin dashboard foundation for SnapStack with real-time metrics, parser testing, and system monitoring.

## ✨ Features Implemented

### Backend (Flask)
- **Modular Blueprint Architecture**
  - `/api/admin/dashboard/*` - Business metrics endpoints
  - `/api/admin/parser/*` - Parser testing endpoints
  - Clean separation of concerns with sub-blueprints

### Frontend (React)
- **Admin Layout** with collapsible sidebar navigation
- **Dashboard** with real-time metrics and charts
- **Parser Studio** for interactive testing
- **Routing** with React Router v6
- **Responsive Design** with Tailwind CSS

## 🏗️ Architecture

```
apps/backend/admin/
├── __init__.py              # Main admin blueprint
├── dashboard/
│   ├── __init__.py         # Dashboard blueprint
│   └── views.py            # Metrics, alerts, trending
└── parser_studio/
    ├── __init__.py         # Parser blueprint
    └── views.py            # Parser testing endpoints

apps/web/src/admin/
├── AdminLayout.tsx         # Navigation and layout
├── Dashboard.tsx           # Main metrics view
└── ParserStudio.tsx        # Parser testing interface
```

## 📊 Dashboard Components

### Key Metrics Cards
- **GMV (Gross Merchandise Value)** - Total sales volume
- **Revenue** - Commission earned
- **Active Users** - Current user count
- **Parser Accuracy** - Success rate with visual indicators

### System Monitoring
- **API Health Score** - Real-time API status
- **Conversion Rate** - Search to purchase ratio
- **Total Searches** - Daily search volume
- **Products Parsed** - Daily parsing count

### Interactive Features
- **Trending Products** - Top 5 products by search volume
- **System Alerts** - Warning and info notifications
- **24-Hour Activity Chart** - Visual activity timeline
- **Quick Actions** - Shortcuts to common tasks

## 🚀 Running the Admin Dashboard

### Quick Start
```bash
./start-admin.sh
```

Then navigate to:
- **Dashboard**: http://localhost:5173/admin
- **Parser Studio**: http://localhost:5173/admin/parser

### Manual Start
```bash
# Terminal 1 - Backend
cd apps/backend
python3 app.py

# Terminal 2 - Frontend
cd apps/web
npm install
npm run dev
```

## 🔌 API Endpoints

### Dashboard Endpoints
- `GET /api/admin/dashboard/metrics` - Core business metrics
- `GET /api/admin/dashboard/alerts` - System alerts
- `GET /api/admin/dashboard/trending` - Trending products
- `GET /api/admin/dashboard/chart-data` - 24-hour activity data

### Parser Endpoints
- `POST /api/admin/parser/test` - Test parser with text
- `GET /api/admin/parser/examples` - Get example inputs
- `GET /api/admin/parser/stats` - Parser statistics

## 🎨 UI Navigation

The admin interface includes:
- **Collapsible Sidebar** - Toggle between full and icon-only view
- **Smart Navigation** - Active page highlighting
- **User Info** - Admin profile in sidebar
- **Date/Time Display** - Current date in header
- **Responsive Layout** - Works on desktop and tablet

## 📈 Next Steps

### High Priority
1. **Real Data Integration** - Replace demo data with actual metrics
2. **WebSocket Support** - Real-time updates without polling
3. **Authentication** - Add JWT-based admin auth
4. **API Monitor** - Complete vendor API monitoring

### Medium Priority
5. **User Management** - User search and support tools
6. **Financial Dashboard** - Revenue and cost tracking
7. **Content Management** - Curated stacks builder
8. **System Logs** - Log viewer and search

### Future Enhancements
9. **Charts Library** - Add Recharts for better visualizations
10. **Export Features** - Download reports as CSV/PDF
11. **Mobile Admin** - Responsive mobile experience
12. **Audit Logging** - Track all admin actions

## 🛠️ Technologies Used

- **Backend**: Flask with Blueprints
- **Frontend**: React 18 with TypeScript
- **Routing**: React Router v6
- **Styling**: Tailwind CSS
- **State**: React hooks (useState, useEffect)
- **API**: RESTful with JSON responses

## 📝 Development Notes

### Adding New Pages
1. Create component in `apps/web/src/admin/`
2. Add route in `App.tsx`
3. Add navigation item in `AdminLayout.tsx`
4. Create Flask blueprint in `apps/backend/admin/`

### Customizing Metrics
- Edit `dashboard/views.py` for backend data
- Modify `Dashboard.tsx` for frontend display
- Add new metric cards following the existing pattern

### Extending Parser Studio
- Parser logic in `packages/parser/src/parser.py`
- Testing endpoint in `parser_studio/views.py`
- UI in `ParserStudio.tsx`

---

The admin dashboard is **functional and ready to build upon**. It provides a solid foundation for monitoring and managing SnapStack operations.