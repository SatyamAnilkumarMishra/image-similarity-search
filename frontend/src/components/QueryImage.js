import React from 'react';

function QueryImage({ src }) {
  return (
    <section className="query-section">
      <h2>Query Image</h2>
      <div className="query-image-container">
        <img src={src} alt="Query" />
      </div>
    </section>
  );
}

export default QueryImage;
