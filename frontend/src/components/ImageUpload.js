import React, { useRef } from 'react';

function ImageUpload({ onFileSelect, onSearch, disabled, topK, setTopK }) {
  const fileInputRef = useRef(null);
  const uploadBoxRef = useRef(null);

  const handleClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onFileSelect(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    uploadBoxRef.current.classList.add('dragover');
  };

  const handleDragLeave = () => {
    uploadBoxRef.current.classList.remove('dragover');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    uploadBoxRef.current.classList.remove('dragover');
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      onFileSelect(file);
    }
  };

  return (
    <section className="upload-section">
      <div 
        ref={uploadBoxRef}
        className="upload-box" 
        onClick={handleClick}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="upload-content">
          <svg className="upload-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <p className="upload-text">Drag & drop an image here or click to browse</p>
          <p className="upload-hint">Supports: JPG, PNG, GIF, BMP</p>
        </div>
        <input 
          ref={fileInputRef}
          type="file" 
          accept="image/*" 
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
      </div>

      <div className="controls">
        <label htmlFor="topK">Number of similar images:</label>
        <input 
          type="number" 
          id="topK" 
          value={topK} 
          onChange={(e) => setTopK(e.target.value)}
          min="1" 
          max="50"
        />
        <button 
          className="btn btn-primary" 
          onClick={onSearch}
          disabled={disabled}
        >
          Search Similar Images
        </button>
      </div>
    </section>
  );
}

export default ImageUpload;
