# 🎨 AI-Powered Image Similarity Search & Recommendation System

A deep learning-based image similarity search engine that uses transfer learning with ResNet50 to find visually similar images. Upload an image and discover similar images from your dataset using state-of-the-art computer vision techniques.

## 🌟 Features

- **Deep Learning Feature Extraction**: Uses pre-trained ResNet50 CNN model from ImageNet
- **Fast Similarity Search**: Cosine similarity with efficient nearest neighbor search
- **Modern React UI**: Beautiful, responsive React interface with drag-and-drop support
- **REST API**: Clean API endpoints for integration with other applications
- **Batch Processing**: Efficient batch feature extraction for large datasets
- **Real-time Search**: Upload an image and get instant recommendations
- **Scalable Architecture**: Easily add new images to the index
- **Production Ready**: Optimized React build served by Flask

## 🏗️ Architecture

```
┌─────────────────┐
│  User Interface │ (HTML/CSS/JS)
└────────┬────────┘
         │
    ┌────▼────┐
    │ Flask   │ REST API
    │ Server  │
    └────┬────┘
         │
    ┌────▼──────────────────┐
    │  Feature Extraction   │
    │  (ResNet50 CNN)       │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │  Similarity Search    │
    │  (Cosine Similarity)  │
    └───────────────────────┘
```

## 📋 Requirements

- Python 3.8 or higher
- TensorFlow 2.x
- Flask
- NumPy, Pillow, scikit-learn

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+ and npm
- Virtual environment activated

### Installation

**1. Navigate to project directory:**
```bash
cd image-similarity-search
```

**2. Activate virtual environment:**
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

**3. Install Python dependencies:**
```bash
pip install -r requirements.txt
```

**4. React frontend is already built and ready!**

The React app has been pre-built. Just run the server!

## 📊 Setup & Usage

### Step 1: Prepare Your Dataset

Add your images to the `data/` directory. The indexer will recursively scan for all image files (JPG, PNG, GIF, BMP).

```
data/
├── category1/
│   ├── image1.jpg
│   ├── image2.jpg
├── category2/
│   ├── image3.png
└── ...
```

**OR** use the sample data downloader:

```bash
python download_sample_data.py
```

This will download 20 sample images to get you started.

### Step 2: Build the Feature Index

Extract features from all images and build the search index:

```bash
python src/indexer.py
```

This will:
- Scan the `data/` directory for images
- Extract deep learning features using ResNet50
- Save the feature index to `models/` directory

**Note**: First run will download the ResNet50 model (~100MB).

### Step 3: Start the Web Server

**Option 1: Use the startup script (recommended)**
```powershell
.\start.ps1
```

**Option 2: Run manually**
```bash
python app.py
```

The server will start at: **http://localhost:5000**

### Step 4: Use the Application

1. Open your browser and go to `http://localhost:5000`
2. Upload an image by dragging & dropping or clicking the upload box
3. Click "Search Similar Images"
4. View the results with similarity scores!

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Model settings
MODEL_NAME = 'ResNet50'
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

# Search settings
TOP_K = 10  # Number of similar images to return

# File upload
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

## 📡 API Endpoints

### Health Check
```
GET /api/health
```

Returns server status and number of indexed images.

### Search Similar Images
```
POST /api/search
Content-Type: multipart/form-data

Parameters:
- image: Image file (required)
- top_k: Number of results (optional, default: 10)

Response:
{
  "query_image": "path/to/uploaded/image",
  "results": [
    {
      "path": "relative/path/to/similar/image",
      "similarity": 0.95
    },
    ...
  ],
  "count": 10
}
```

### Random Images
```
GET /api/random?count=20
```

Returns random images from the index for browsing.

## 🧠 How It Works

### 1. Feature Extraction
- Uses ResNet50 pre-trained on ImageNet
- Removes the classification layer to get feature vectors
- Each image is converted to a 2048-dimensional feature vector
- Features are L2-normalized for better similarity comparison

### 2. Similarity Search
- Uses cosine similarity to compare feature vectors
- Cosine similarity = dot product of normalized vectors
- Returns top-K most similar images
- Similarity score ranges from 0 (dissimilar) to 1 (identical)

### 3. Transfer Learning
- ResNet50 learned rich visual features from 1.2M ImageNet images
- These features generalize well to new images
- No training required - works out of the box!

## 📁 Project Structure

```
image-similarity-search/
├── src/
│   ├── feature_extractor.py   # Deep learning feature extraction
│   ├── similarity_search.py   # Similarity computation
│   └── indexer.py              # Image indexing system
├── frontend/                   # React frontend
│   ├── src/                    # React source code
│   │   ├── App.js
│   │   ├── components/         # React components
│   │   └── App.css
│   ├── build/                  # Production build (pre-built)
│   ├── package.json
│   └── README.md
├── static/
│   └── uploads/                # Uploaded query images
├── templates/
│   └── index.html              # Legacy HTML (not used with React)
├── data/                       # Your image dataset
├── models/                     # Saved feature indices
├── app.py                      # Flask web server
├── config.py                   # Configuration
├── start.ps1                   # Quick start script
├── download_sample_data.py     # Sample data downloader
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🎯 Use Cases

- **E-commerce**: Find similar products
- **Photo Management**: Organize photo libraries
- **Content Moderation**: Find duplicate/similar content
- **Fashion**: Find similar clothing items
- **Art**: Discover similar artworks
- **Real Estate**: Find similar properties

## 🔍 Advanced Usage

### Adding More Images

To add new images to an existing index:

```python
from src.indexer import ImageIndexer

indexer = ImageIndexer()
new_images = ['path/to/new/image1.jpg', 'path/to/new/image2.jpg']
indexer.add_images_to_index(new_images)
```

### Using Different Models

You can modify `feature_extractor.py` to use other pre-trained models:
- VGG16
- InceptionV3
- EfficientNet
- MobileNet

### Batch Processing

For large datasets, adjust batch size in `config.py`:

```python
BATCH_SIZE = 64  # Increase for faster processing (requires more RAM)
```

## ⚡ Performance Tips

1. **GPU Acceleration**: Install `tensorflow-gpu` for faster feature extraction
2. **Batch Size**: Increase batch size if you have more RAM
3. **Image Size**: Smaller images process faster (but may reduce accuracy)
4. **Caching**: Features are saved to disk - only need to extract once

## 🐛 Troubleshooting

**Issue**: "No index found" error
- **Solution**: Run `python src/indexer.py` first to build the index

**Issue**: Out of memory during indexing
- **Solution**: Reduce `BATCH_SIZE` in `config.py`

**Issue**: Slow feature extraction
- **Solution**: Install TensorFlow with GPU support

**Issue**: Images not loading in web interface
- **Solution**: Check that images are in the `data/` directory

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📚 References

- [ResNet Paper](https://arxiv.org/abs/1512.03385)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Transfer Learning Guide](https://www.tensorflow.org/tutorials/images/transfer_learning)

## 👨‍💻 Author



