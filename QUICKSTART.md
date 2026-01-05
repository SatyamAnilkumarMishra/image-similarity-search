# 🚀 Quick Start Guide

Get your AI Image Similarity Search system up and running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Internet connection (for downloading dependencies and sample data)

## Step-by-Step Setup

### 1. Install Dependencies

Open PowerShell in this directory and run:

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt
```

**Note**: First installation may take 5-10 minutes as it downloads TensorFlow and other packages.

### 2. Download Sample Images

```powershell
python download_sample_data.py
```

This downloads 20 sample images to the `data/` folder.

### 3. Build the Search Index

```powershell
python src\indexer.py
```

This extracts features from all images. First run downloads ResNet50 model (~100MB).

**Expected output:**
```
Found 20 images
Extracting features...
Processed 20/20 images
Successfully extracted features from 20 images
Index building complete!
```

### 4. Start the Server

```powershell
python app.py
```

**Expected output:**
```
==================================================
Image Similarity Search Server
==================================================
Server running at: http://localhost:5000
Indexed images: 20
==================================================
```

### 5. Open the Web Interface

Open your browser and go to:
```
http://localhost:5000
```

## Usage

1. **Drag & drop** or **click** to upload an image
2. Adjust the number of similar images to find (1-50)
3. Click **"Search Similar Images"**
4. View results with similarity scores!

## Troubleshooting

### PowerShell execution policy error
If you see an error about execution policies, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python not found
Make sure Python is installed and added to PATH. Download from: https://www.python.org/downloads/

### Port 5000 already in use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

## What's Next?

- Add your own images to the `data/` folder
- Re-run `python src\indexer.py` to index them
- Restart the server and search!

## System Requirements

- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: ~500MB for dependencies + your images
- **CPU**: Any modern processor (GPU optional but faster)

## Need Help?

Check the main README.md for detailed documentation and advanced features.

---

Happy searching! 🎨✨
