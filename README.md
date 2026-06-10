# 🏥 Medical Research Agent

A full-stack AI-powered web application for discovering, searching, and managing medical research papers with an intuitive interface and powerful backend.

## 🌟 Features

### Search & Discovery
- 🔍 **Intelligent Search**: Find medical research papers by query and topic
- 📚 **Rich Results**: View comprehensive paper details including abstracts, authors, citations
- 🏥 **Medical Topics**: Diabetes, Cancer, Heart Disease, COVID-19, Neuroscience
- ⚡ **Fast Performance**: Optimized for quick responses and smooth user experience

### Content Management
- ⭐ **Save Articles**: Bookmark important research papers for later
- 💾 **Persistent Storage**: Saved articles stored in browser localStorage
- 📋 **Favorites List**: Dedicated tab for viewing and managing saved articles

### Activity Tracking
- 🔄 **Search History**: Automatic tracking of all your searches
- 📊 **Statistics Dashboard**: View your research activity metrics
- 📈 **Analytics**: Total searches, saved articles, topics explored

### Design & UX
- 💻 **Responsive Design**: Perfect experience on desktop, tablet, and mobile
- 🎨 **Modern UI**: Clean, intuitive interface with smooth animations
- 🌈 **Beautiful Gradient**: Professional purple gradient theme
- ⚙️ **Backend Status**: Real-time connection status indicator

## 🛠️ Tech Stack

### Frontend
- **React 18.2**: Modern UI library
- **CSS3**: Advanced styling with CSS variables and animations
- **LocalStorage API**: Client-side data persistence
- **Fetch API**: HTTP client for API communication

### Backend
- **Express.js 4.18**: RESTful API framework
- **Node.js**: Server runtime
- **CORS**: Cross-origin request handling
- **Dotenv**: Environment configuration

### DevOps
- **Docker & Docker Compose**: Containerization and orchestration
- **Nodemon**: Development hot-reload

## 📋 Requirements

### System Requirements
- Node.js v14 or higher
- npm v6 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Docker & Docker Compose (optional, for containerized setup)

### Disk Space
- ~500MB for node_modules
- ~200MB for Docker images (if using Docker)

## 🚀 Quick Start

### Method 1: Manual Setup (Development)

```bash
# Clone or extract the project
cd medical-research-agent

# Backend Setup
cd backend
npm install
npm run dev

# In another terminal, Frontend Setup
cd frontend
npm install
npm start
```

Visit `http://localhost:3000` in your browser.

### Method 2: Docker Setup (Production)

```bash
cd medical-research-agent
docker-compose up --build
```

Access the application at `http://localhost:3000`

See [QUICK_START.md](./QUICK_START.md) for detailed setup instructions.

## 📁 Project Structure

```
medical-research-agent/
├── backend/                    # Express.js API server
│   ├── server.js              # Main server file
│   ├── package.json           # Dependencies
│   ├── .env                   # Configuration
│   └── Dockerfile             # Container config
│
├── frontend/                   # React application
│   ├── src/
│   │   ├── App.js            # Main component
│   │   ├── App.css           # Styles
│   │   └── index.js          # Entry point
│   ├── public/
│   │   └── index.html        # HTML template
│   ├── package.json          # Dependencies
│   ├── .env                  # Configuration
│   └── Dockerfile            # Container config
│
├── docker-compose.yml        # Multi-container setup
├── README.md                 # This file
├── QUICK_START.md           # Quick start guide
└── .gitignore               # Git ignore rules
```

## 🔌 API Reference

### Endpoints

#### Search Research
```http
POST /api/research/search
Content-Type: application/json

{
  "query": "new treatment methods",
  "topic": "diabetes"
}

Response: {
  "success": true,
  "data": [...],
  "count": 3,
  "timestamp": "2024-01-15T..."
}
```

#### Get All Research Records
```http
GET /api/research
Response: {
  "success": true,
  "data": [...],
  "total": 5
}
```

#### Get Research by ID
```http
GET /api/research/:id
Response: {
  "success": true,
  "data": {...}
}
```

#### Get Statistics
```http
GET /api/stats
Response: {
  "success": true,
  "data": {
    "totalSearches": 10,
    "savedCount": 3,
    "uniqueTopics": 4,
    "topics": ["diabetes", "cancer", "heart"]
  }
}
```

#### Health Check
```http
GET /api/health
Response: {
  "success": true,
  "status": "Backend is running",
  "timestamp": "2024-01-15T..."
}
```

#### Save Research
```http
POST /api/research/:id/save
Response: {
  "success": true,
  "message": "Research saved successfully",
  "data": {...}
}
```

#### Clear Research History
```http
DELETE /api/research
Response: {
  "success": true,
  "message": "Cleared 5 research records"
}
```

## 🎯 Usage Guide

### Search for Research Papers

1. Open the application (http://localhost:3000)
2. Go to the "Search" tab (default)
3. Enter your research query
4. Select a medical topic
5. Click "Search Research"
6. Browse the results

### Save Your Favorite Papers

1. Find a paper you like in the search results
2. Click the ⭐ star icon
3. The paper is saved to your collection
4. Access saved papers in the "Saved" tab

### Review Search History

1. Go to the "History" tab
2. See all your previous searches with timestamps
3. Click "Search Again" to repeat a search
4. Use "Clear History" to remove all history

### Check Your Statistics

1. Click the "Stats" tab
2. View your research activity metrics:
   - Total searches performed
   - Number of saved articles
   - Number of unique topics explored

## ⚙️ Configuration

### Backend (.env)

```env
PORT=5000
NODE_ENV=development
API_URL=http://localhost:5000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5000
LOG_LEVEL=debug
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ENV=development
REACT_APP_ENABLE_ANALYTICS=false
REACT_APP_ENABLE_CACHE=true
```

## 🐛 Troubleshooting

### Backend Connection Failed
```bash
# Check if backend is running
curl http://localhost:5000/api/health

# Verify frontend .env has correct API_URL
cat frontend/.env | grep REACT_APP_API_URL

# Check CORS configuration in backend
# Backend should be running on port 5000
```

### Port Already in Use
```bash
# Linux/Mac - Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Windows - Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Dependencies Issues
```bash
# Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Docker Issues
```bash
# Rebuild everything
docker-compose down -v
docker-compose up --build

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 📊 Development Workflow

### Local Development

```bash
# Terminal 1: Start Backend
cd backend
npm run dev

# Terminal 2: Start Frontend
cd frontend
npm start
```

### Enable Hot Reload
- Frontend: Changes auto-reload
- Backend: Use `npm run dev` (runs with nodemon)

### Debug Mode
- Open browser DevTools (F12)
- Check Network tab for API calls
- Use Console for React errors
- Check Application > LocalStorage for saved data

## 🚀 Deployment

### Build for Production

```bash
# Frontend build
cd frontend
npm run build
# Output: ./build directory

# Backend is production-ready as-is
```

### Docker Deployment

```bash
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f
```

### Environment Setup for Production

1. Update backend `.env`:
   - Set `NODE_ENV=production`
   - Update `ALLOWED_ORIGINS` with your domain

2. Update frontend `.env`:
   - Set `REACT_APP_API_URL` to your backend URL
   - Set `REACT_APP_ENV=production`

## 📝 Database Schema

### Research Record
```javascript
{
  id: string,
  timestamp: Date,
  query: string,
  topic: string,
  results: Array<ResearchPaper>,
  status: 'completed' | 'in_progress' | 'failed',
  saved: boolean,
  savedAt: Date
}
```

### Research Paper
```javascript
{
  id: string,
  title: string,
  abstract: string,
  authors: string[],
  year: number,
  citations: number,
  relevance: number,
  matchScore: number
}
```

## 🔒 Security

- CORS enabled for trusted origins only
- Input validation on backend
- No sensitive data in localStorage
- Environment variables for configuration
- No hardcoded API keys

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Commit with clear messages
5. Push and create a Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support

### Getting Help
- Check [QUICK_START.md](./QUICK_START.md) for setup issues
- Review API Reference section above
- Check browser console for errors
- Verify backend health with `/api/health` endpoint

### Common Issues

| Issue | Solution |
|-------|----------|
| Port 5000 in use | Kill process on port 5000 |
| Cannot connect to backend | Ensure backend running, check API_URL |
| No search results | Try searching for: diabetes, cancer, heart, covid, neuroscience |
| Saved articles lost | Check browser localStorage settings |

## 🗺️ Roadmap

### Future Features
- [ ] User authentication
- [ ] Database persistence (MongoDB)
- [ ] Advanced filtering options
- [ ] PDF download of papers
- [ ] Export search results
- [ ] Dark mode
- [ ] Multi-language support
- [ ] Real medical API integration

## 👤 Author

Created as a full-stack AI agent project

## 🎓 Learning Resources

- [React Documentation](https://react.dev)
- [Express.js Guide](https://expressjs.com)
- [Node.js Best Practices](https://nodejs.org/en/docs/)
- [Docker Tutorial](https://docs.docker.com/get-started/)

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Status**: ✅ Production Ready

Start discovering medical research now! 🔬📚
