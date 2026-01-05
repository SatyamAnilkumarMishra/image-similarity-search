# Image Similarity Search - React Frontend

## Setup Instructions

### 1. Install Node.js Dependencies

```bash
cd frontend
npm install
```

### 2. Run Development Server (Option 1)

For development with hot reload:

```bash
npm start
```

This will start the React dev server on `http://localhost:3000` and proxy API requests to `http://localhost:5000`.

Make sure the Flask backend is running on port 5000.

### 3. Build for Production (Option 2)

To build the React app for production:

```bash
npm run build
```

This creates a `build` folder with optimized production files. The Flask app will automatically serve this build.

## Running the Full Application

### Development Mode
1. Start Flask backend: `python app.py` (runs on port 5000)
2. Start React frontend: `cd frontend && npm start` (runs on port 3000)
3. Access the app at `http://localhost:3000`

### Production Mode
1. Build React: `cd frontend && npm run build`
2. Start Flask backend: `python app.py` (runs on port 5000)
3. Access the app at `http://localhost:5000` (Flask serves the React build)

## Features

- 🎨 Modern React UI with hooks
- 📤 Drag & drop image upload
- 🔍 AI-powered similarity search
- 📊 Visual results with similarity scores
- 🖼️ Browse random images
- 📱 Responsive design

## Troubleshooting

**If the model is not generating output:**
1. Make sure you've built the image index: `python src/indexer.py`
2. Verify images exist in the `data` directory
3. Check that `models/image_features.pkl` and `models/image_paths.pkl` exist

**If you see CORS errors:**
- Make sure Flask-CORS is installed: `pip install flask-cors`
- The Flask backend already has CORS enabled

**If images don't load:**
- Verify the Flask backend is running
- Check that image paths in the data directory are correct
