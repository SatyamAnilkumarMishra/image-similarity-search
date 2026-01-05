import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';
import ImageUpload from './components/ImageUpload';
import QueryImage from './components/QueryImage';
import SearchResults from './components/SearchResults';
import BrowseImages from './components/BrowseImages';
import StatusMessage from './components/StatusMessage';
import ResultsPage from './components/ResultsPage';

function HomePage() {
  const navigate = useNavigate();
  const [status, setStatus] = useState({ message: '', type: '' });
  const [queryImage, setQueryImage] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [topK, setTopK] = useState(10);

  useEffect(() => {
    checkServerStatus();
  }, []);

  const checkServerStatus = async () => {
    try {
      const response = await axios.get('/api/health');
      const data = response.data;
      
      if (data.status === 'ok') {
        if (data.indexed) {
          setStatus({
            message: `✓ System ready! ${data.total_images} images indexed.`,
            type: 'success'
          });
        } else {
          setStatus({
            message: '⚠ No image index found. Please run indexer.py first.',
            type: 'error'
          });
        }
      }
    } catch (error) {
      setStatus({
        message: '✗ Unable to connect to server.',
        type: 'error'
      });
    }
  };

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      setQueryImage(e.target.result);
      setResults(null);
    };
    reader.readAsDataURL(file);
  };

  const handleSearch = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append('image', selectedFile);
      formData.append('top_k', topK);

      const response = await axios.post('/api/search', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setResults(response.data);
      // Navigate to results page
      navigate('/results', { 
        state: { 
          results: response.data, 
          queryImage: queryImage 
        } 
      });
    } catch (error) {
      setStatus({
        message: `Error: ${error.response?.data?.error || error.message}`,
        type: 'error'
      });
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <header>
          <h1>🎨 AI-Powered Image Similarity Search</h1>
          <p className="subtitle">Upload an image to find visually similar images using deep learning</p>
          <StatusMessage status={status} />
        </header>

        <main>
          <ImageUpload 
            onFileSelect={handleFileSelect}
            onSearch={handleSearch}
            disabled={!selectedFile}
            topK={topK}
            setTopK={setTopK}
          />

          {queryImage && <QueryImage src={queryImage} />}

          {loading && (
            <div className="loader">
              <div className="spinner"></div>
              <p>Analyzing image and finding similar matches...</p>
            </div>
          )}

          {results && <SearchResults results={results} />}

          <BrowseImages />
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/results" element={<ResultsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
