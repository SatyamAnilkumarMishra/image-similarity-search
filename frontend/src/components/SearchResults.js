import React from 'react';

function SearchResults({ results }) {
  if (!results || !results.results || results.results.length === 0) {
    return null;
  }

  const hasExactMatch = results.results.length > 0 && results.results[0].similarity > 0.99;

  return (
    <section className="results-section">
      {hasExactMatch && (
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
              onError={(e) => e.target.style.display = 'none'}
            />
            <div className="similarity-badge" style={{background: result.is_exact_match ? '#4CAF50' : ''}}>
              {result.is_exact_match && '⭐ '}{(result.similarity * 100).toFixed(1)}%
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default SearchResults;
