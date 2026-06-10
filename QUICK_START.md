# 🏥 Medical Research Agent - Quick Start Guide

## Project Overview

Medical Research Agent is a full-stack AI-powered application for discovering and managing medical research papers. It features a React frontend and Express.js backend with search, save, and statistics capabilities.

### Features
- ✨ **Smart Search**: Query medical research by topic
- 💾 **Save Articles**: Bookmark your favorite research papers
- 📊 **Statistics**: Track your research activities
- 🔄 **Search History**: Quick access to previous searches
- 🎯 **Advanced Filtering**: Filter by topic, relevance, and citations
- 💻 **Responsive Design**: Works on desktop and mobile devices

---

## Prerequisites

Before you begin, ensure you have installed:

- **Node.js** (v14 or higher) - [Download](https://nodejs.org/)
- **npm** (comes with Node.js)
- **Git** (optional, for cloning the repo)

Check your installations:
```bash
node --version
npm --version
```

---

## Installation & Setup

### Option 1: Manual Setup (Recommended for Development)

#### 1. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Install dependencies
npm install

# Create environment file (if not exists)
cp .env.example .env

# Start the backend server
npm start
# or for development with auto-reload:
npm run dev
```

The backend will start on `http://localhost:5000`

#### 2. Frontend Setup (in a new terminal)

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file (if not exists)
cp .env.example .env

# Start the React development server
npm start
```

The frontend will start on `http://localhost:3000` and open automatically in your browser

### Option 2: Docker Setup

Ensure Docker and Docker Compose are installed, then run:

```bash
# From the project root
docker-compose up --build

# Access the application at http://localhost:3000
# The backend runs on http://localhost:5000
```

---

## Configuration

### Backend Configuration (.env)

```env
PORT=5000                    # Server port
NODE_ENV=development         # Environment mode
API_URL=http://localhost:5000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5000
LOG_LEVEL=debug
```

### Frontend Configuration (.env)

```env
REACT_APP_API_URL=http://localhost:5000  # Backend URL
REACT_APP_ENV=development
REACT_APP_ENABLE_ANALYTICS=false
REACT_APP_ENABLE_CACHE=true
```

---

## Usage

### 1. **Search Research**
   - Navigate to the "Search" tab
   - Enter your research query (e.g., "latest treatment methods")
   - Select a medical topic from the dropdown
   - Click "Search Research"
   - Browse the results with detailed information

### 2. **Save Articles**
   - Click the ⭐ star icon on any research card to save
   - Access saved articles from the "Saved" tab
   - Your saved articles persist in local storage

### 3. **View Search History**
   - Go to the "History" tab to see your past searches
   - Click "Search Again" to quickly re-run a previous search
   - Clear your entire history with the "Clear History" button

### 4. **Check Statistics**
   - Visit the "Stats" tab to see:
     - Total searches performed
     - Number of saved articles
     - Unique topics explored

---

## Project Structure

```
medical-research-agent/
├── backend/
│   ├── server.js           # Express server with API routes
│   ├── package.json        # Backend dependencies
│   ├── .env               # Backend configuration
│   ├── .env.example       # Template for .env
│   └── Dockerfile         # Docker configuration
│
├── frontend/
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── App.css        # Styling
│   │   └── index.js       # React entry point
│   ├── public/
│   │   └── index.html     # HTML template
│   ├── package.json       # Frontend dependencies
│   ├── .env              # Frontend configuration
│   ├── .env.example      # Template for .env
│   └── Dockerfile        # Docker configuration
│
├── docker-compose.yml     # Docker composition config
├── README.md             # Full documentation
└── QUICK_START.md        # This file
```

---

## API Endpoints

### Search Research
```
POST /api/research/search
Body: { "query": "treatment methods", "topic": "diabetes" }
Returns: Array of research papers
```

### Get All Research
```
GET /api/research
Returns: Array of all search records
```

### Get Research by ID
```
GET /api/research/:id
Returns: Single research record
```

### Get Statistics
```
GET /api/stats
Returns: { totalSearches, savedCount, uniqueTopics }
```

### Health Check
```
GET /api/health
Returns: { status: "Backend is running" }
```

---

## Troubleshooting

### Port Already in Use
```bash
# Kill the process using port 5000 (backend)
# On Mac/Linux:
lsof -ti:5000 | xargs kill -9

# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Backend Connection Error
- Ensure backend is running: `npm run dev` in `/backend`
- Check that `REACT_APP_API_URL` in frontend `.env` is correct
- Verify CORS settings in backend

### Dependencies Not Installing
```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Docker Issues
```bash
# Rebuild containers
docker-compose down
docker-compose up --build

# View logs
docker-compose logs -f
```

---

## Development Tips

### Hot Reload
- **Frontend**: Changes auto-reload in browser
- **Backend**: Use `npm run dev` for automatic restart with nodemon

### Browser DevTools
- Open DevTools (F12) to inspect network requests
- Check the "Network" tab to verify API calls to `/api/research/search`

### Local Storage
- Saved articles are stored in browser's localStorage
- Clear it from DevTools > Application > Local Storage

---

## Building for Production

### Frontend
```bash
cd frontend
npm run build
# Creates optimized build in ./build directory
```

### Using Docker
```bash
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up
```

---

## Common Tasks

### Reset Application
```bash
# Clear browser localStorage
# In browser console:
localStorage.clear()

# Restart servers
# Terminal 1: Ctrl+C in frontend
# Terminal 2: Ctrl+C in backend
# Then restart both
```

### Update Dependencies
```bash
npm update
```

### Check Backend Health
```bash
curl http://localhost:5000/api/health
```

---

## Support & Documentation

- Full documentation: See `README.md`
- API documentation: Check backend `server.js` comments
- React documentation: [react.dev](https://react.dev)
- Express documentation: [expressjs.com](https://expressjs.com)

---

## License

MIT License - See LICENSE file for details

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Start backend server
3. ✅ Start frontend application
4. ✅ Open browser at `http://localhost:3000`
5. ✅ Try searching for medical research!

Happy researching! 🔬📚
