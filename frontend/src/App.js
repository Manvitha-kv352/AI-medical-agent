import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [query, setQuery] = useState('');
  const [topic, setTopic] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [savedArticles, setSavedArticles] = useState([]);
  const [stats, setStats] = useState(null);
  const [activeTab, setActiveTab] = useState('search');
  const [backendHealthy, setBackendHealthy] = useState(false);
  const [searchHistory, setSearchHistory] = useState([]);

  const topics = ['diabetes', 'cancer', 'heart', 'covid', 'neuroscience'];

  // Fetch stats on mount
  useEffect(() => {
    fetchStats();
    checkBackendHealth();
    const savedItems = localStorage.getItem('savedArticles');
    if (savedItems) {
      setSavedArticles(JSON.parse(savedItems));
    }
  }, []);

  // Save articles to localStorage
  useEffect(() => {
    localStorage.setItem('savedArticles', JSON.stringify(savedArticles));
  }, [savedArticles]);

  const checkBackendHealth = async () => {
    try {
      const res = await fetch(`${API_URL}/api/health`, { timeout: 5000 });
      if (res.ok) {
        setBackendHealthy(true);
      }
    } catch (err) {
      setBackendHealthy(false);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await fetch(`${API_URL}/api/stats`);
      const data = await res.json();
      if (data.success) {
        setStats(data.data);
      }
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!query.trim() || !topic) {
      setError('Please enter a query and select a topic');
      return;
    }

    setLoading(true);
    setError('');
    setResults([]);

    try {
      const res = await fetch(`${API_URL}/api/research/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, topic })
      });

      const data = await res.json();

      if (data.success) {
        setResults(data.data);
        // Add to search history
        setSearchHistory([{ query, topic, timestamp: new Date() }, ...searchHistory.slice(0, 9)]);
        fetchStats();
      } else {
        setError(data.error || 'Search failed');
      }
    } catch (err) {
      setError('Error connecting to backend: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveArticle = async (article) => {
    if (savedArticles.find(a => a.id === article.id)) {
      setSavedArticles(savedArticles.filter(a => a.id !== article.id));
    } else {
      setSavedArticles([...savedArticles, article]);
    }
  };

  const isArticleSaved = (id) => savedArticles.some(a => a.id === id);

  const quickSearch = (hist) => {
    setQuery(hist.query);
    setTopic(hist.topic);
  };

  const clearHistory = () => {
    if (window.confirm('Clear all search history?')) {
      setSearchHistory([]);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="header-top">
            <h1>🏥 Medical Research Agent</h1>
            <div className={`health-badge ${backendHealthy ? 'healthy' : 'unhealthy'}`}>
              <span className="status-dot"></span>
              {backendHealthy ? 'Backend Connected' : 'Backend Offline'}
            </div>
          </div>
          <p>Discover cutting-edge medical research papers with AI-powered search</p>
        </div>
      </header>

      <div className="tabs">
        <button 
          className={`tab-btn ${activeTab === 'search' ? 'active' : ''}`}
          onClick={() => setActiveTab('search')}
        >
          Search
        </button>
        <button 
          className={`tab-btn ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          History ({searchHistory.length})
        </button>
        <button 
          className={`tab-btn ${activeTab === 'saved' ? 'active' : ''}`}
          onClick={() => setActiveTab('saved')}
        >
          Saved ({savedArticles.length})
        </button>
        <button 
          className={`tab-btn ${activeTab === 'stats' ? 'active' : ''}`}
          onClick={() => setActiveTab('stats')}
        >
          Stats
        </button>
      </div>

      <main className="container">
        {activeTab === 'search' && (
          <div className="search-section">
            <form className="search-form" onSubmit={handleSearch}>
              <div className="form-group">
                <label htmlFor="query">Research Query</label>
                <input
                  type="text"
                  id="query"
                  placeholder="e.g., new treatment methods, latest findings..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="topic">Select Topic</label>
                <select
                  id="topic"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  disabled={loading}
                >
                  <option value="">Choose a topic...</option>
                  {topics.map(t => (
                    <option key={t} value={t}>
                      {t.charAt(0).toUpperCase() + t.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              <button 
                type="submit" 
                className="search-btn"
                disabled={loading}
              >
                {loading ? 'Searching...' : 'Search Research'}
              </button>
            </form>

            {error && <div className="error-message">{error}</div>}

            {results.length > 0 && (
              <div className="results-section">
                <h2>Search Results ({results.length} found)</h2>
                <div className="results-grid">
                  {results.map((result) => (
                    <div key={result.id} className="research-card">
                      <div className="card-header">
                        <h3>{result.title}</h3>
                        <button 
                          className={`save-btn ${isArticleSaved(result.id) ? 'saved' : ''}`}
                          onClick={() => handleSaveArticle(result)}
                          title={isArticleSaved(result.id) ? 'Remove from saved' : 'Save article'}
                        >
                          ⭐
                        </button>
                      </div>
                      <p className="abstract">{result.abstract}</p>
                      
                      <div className="metadata">
                        <div className="authors">
                          <strong>Authors:</strong> {result.authors.join(', ')}
                        </div>
                        <div className="year">
                          <strong>Year:</strong> {result.year}
                        </div>
                      </div>

                      <div className="stats-row">
                        <div className="stat">
                          <span className="stat-label">Citations</span>
                          <span className="stat-value">{result.citations}</span>
                        </div>
                        <div className="stat">
                          <span className="stat-label">Relevance</span>
                          <span className="stat-value">{(result.relevance * 100).toFixed(0)}%</span>
                        </div>
                        <div className="stat">
                          <span className="stat-label">Match Score</span>
                          <span className="stat-value">{(result.matchScore * 100).toFixed(0)}%</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {!loading && results.length === 0 && query && (
              <div className="empty-state">
                <p>No results yet. Try refining your search.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'saved' && (
          <div className="saved-section">
            <h2>Saved Articles ({savedArticles.length})</h2>
            {savedArticles.length === 0 ? (
              <div className="empty-state">
                <p>No saved articles yet. Start searching and save your favorites! ⭐</p>
              </div>
            ) : (
              <div className="results-grid">
                {savedArticles.map((article) => (
                  <div key={article.id} className="research-card">
                    <div className="card-header">
                      <h3>{article.title}</h3>
                      <button 
                        className="save-btn saved"
                        onClick={() => handleSaveArticle(article)}
                        title="Remove from saved"
                      >
                        ⭐
                      </button>
                    </div>
                    <p className="abstract">{article.abstract}</p>
                    
                    <div className="metadata">
                      <div className="authors">
                        <strong>Authors:</strong> {article.authors.join(', ')}
                      </div>
                      <div className="year">
                        <strong>Year:</strong> {article.year}
                      </div>
                    </div>

                    <div className="stats-row">
                      <div className="stat">
                        <span className="stat-label">Citations</span>
                        <span className="stat-value">{article.citations}</span>
                      </div>
                      <div className="stat">
                        <span className="stat-label">Relevance</span>
                        <span className="stat-value">{(article.relevance * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'history' && (
          <div className="history-section">
            <div className="history-header">
              <h2>Search History</h2>
              {searchHistory.length > 0 && (
                <button className="clear-history-btn" onClick={clearHistory}>
                  Clear History
                </button>
              )}
            </div>
            {searchHistory.length === 0 ? (
              <div className="empty-state">
                <p>No search history yet. Try searching for medical research! 🔍</p>
              </div>
            ) : (
              <div className="history-list">
                {searchHistory.map((hist, idx) => (
                  <div key={idx} className="history-item">
                    <div className="history-content">
                      <div className="history-topic">
                        <span className="topic-badge">{hist.topic}</span>
                      </div>
                      <div className="history-query">
                        <p className="query-text">{hist.query}</p>
                        <p className="query-time">
                          {new Date(hist.timestamp).toLocaleString()}
                        </p>
                      </div>
                    </div>
                    <button 
                      className="quick-search-btn"
                      onClick={() => quickSearch(hist)}
                    >
                      Search Again →
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'stats' && (
          <div className="stats-section">
            <h2>Research Statistics</h2>
            {stats ? (
              <div className="stats-grid">
                <div className="stat-card">
                  <h3>{stats.totalSearches}</h3>
                  <p>Total Searches</p>
                </div>
                <div className="stat-card">
                  <h3>{stats.savedCount}</h3>
                  <p>Saved Articles</p>
                </div>
                <div className="stat-card">
                  <h3>{stats.uniqueTopics}</h3>
                  <p>Topics Explored</p>
                </div>
              </div>
            ) : (
              <div className="empty-state">
                <p>No data yet. Start searching to build statistics.</p>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Medical Research Agent © 2024 | Powered by AI</p>
      </footer>
    </div>
  );
}

export default App;
