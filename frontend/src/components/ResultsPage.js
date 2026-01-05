import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { results, queryImage } = location.state || {};

  if (!results) {
    return (
      <div className="container">
        <div className="error-message">
          <p>No results to display</p>
          <button onClick={() => navigate('/')} className="btn btn-primary">
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="container">
        <header>
          <h1>🎨 Search Results</h1>
          <button onClick={() => navigate('/')} className="btn btn-secondary">
            ← Back to Search
          </button>
        </header>

        <main>
          {queryImage && (
            <section className="query-section">
              <h2>Query Image</h2>
              <div className="query-image-container">
                <img src={queryImage} alt="Query" />
              </div>
            </section>
          )}

          <section className="results-section">
            {results.results.length > 0 && results.results[0].similarity > 0.99 && (
              <div style={{padding: '10px', background: '#4CAF50', color: 'white', borderRadius: '5px', marginBottom: '15px'}}>
                ✓ Exact match found! This image exists in the database.
              </div>
            )}
            <h2>Similar Images <span>({results.count} results)</span></h2>
            <div className="results-grid">
              {results.results.map((result, index) => (
                <div key={index} className={`result-item ${result.is_exact_match ? 'exact-match' : ''}`}>
                  <img 
                    src={`/${result.path}`} 
                    alt={`Similar ${index + 1}`}
                    loading="lazy"
                    onError={(e) => {
                      console.error('Image load error:', result.path);
                      e.target.style.display = 'none';
                    }}
                  />
                  <div className="similarity-badge" style={{background: result.is_exact_match ? '#4CAF50' : ''}}>
                    {result.is_exact_match && '⭐ '}{(result.similarity * 100).toFixed(1)}%
                  </div>
                </div>
              ))}
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}

export default ResultsPage;
