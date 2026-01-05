import React, { useState } from 'react';
import axios from 'axios';

function BrowseImages() {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadRandomImages = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/random?count=20');
      setImages(response.data.results);
    } catch (error) {
      console.error('Error loading images:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="browse-section">
      <h2>Browse Random Images</h2>
      <button 
        className="btn btn-secondary" 
        onClick={loadRandomImages}
        disabled={loading}
      >
        {loading ? 'Loading...' : 'Load Random Images'}
      </button>
      <div className="results-grid">
        {images.map((image, index) => (
          <div key={index} className="result-item">
            <img 
              src={`/${image.path}`} 
              alt={`Image ${index + 1}`}
              loading="lazy"
              onError={(e) => e.target.style.display = 'none'}
            />
          </div>
        ))}
      </div>
    </section>
  );
}

export default BrowseImages;
