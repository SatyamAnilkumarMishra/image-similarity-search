# 🚀 Complete Setup Guide

This guide will walk you through setting up and running the Image Similarity Search application.

## ✅ What's Already Done

- ✅ React frontend is **already built** and ready to use
- ✅ All Python dependencies should be installed in your virtual environment
- ✅ Flask backend is configured to serve the React app
- ✅ Image index with 20 sample images is ready

## 🎯 Quick Start (3 Steps)

### Step 1: Ensure Virtual Environment is Active

Check if you see `(venv)` in your terminal prompt. If not, activate it:

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows Command Prompt
venv\Scripts\activate.bat
```

### Step 2: Verify the Index Exists

The image index should already be built. Verify it exists:

```powershell
Test-Path models\image_features.pkl
```

If it returns `False`, build the index:

```powershell
python src\indexer.py
```

### Step 3: Start the Server

**Option A: Use the startup script (easiest)**
```powershell
.\start.ps1
```

**Option B: Run directly**
```powershell
python app.py
```

### Step 4: Access the App

Open your browser and go to:
```
http://localhost:5000
```

You should see the React interface! 🎉

## 📋 Troubleshooting

### Issue: "React app not built" message

**Solution:**
```powershell
cd frontend
npm install
npm run build
cd ..
python app.py
```

### Issue: "No index loaded" error

**Solution:**
```powershell
# Make sure you have images in the data directory
python src\indexer.py
```

### Issue: Port 5000 already in use

**Solution:**
1. Find what's using port 5000:
   ```powershell
   Get-NetTCPConnection -LocalPort 5000
   ```
2. Stop that process or change the port in `app.py` (line 174)

### Issue: TensorFlow warnings/errors

**Solution:**
These are usually just warnings. The app should still work. To suppress TensorFlow logs, the code already sets:
```python
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
```

### Issue: Cannot find module 'react-scripts'

**Solution:**
```powershell
cd frontend
npm install
cd ..
```

### Issue: Images not displaying

**Solution:**
1. Check that images exist in the `data` directory
2. Verify the index was built: `Test-Path models\image_features.pkl`
3. Restart the Flask server

## 🔄 Rebuilding the React App

Only needed if you modify the React frontend:

```powershell
cd frontend
npm run build
cd ..
python app.py
```

## 🔧 Development Mode

To work on the React frontend with hot reload:

**Terminal 1 (Backend):**
```powershell
python app.py
```

**Terminal 2 (Frontend):**
```powershell
cd frontend
npm start
```

Then access the app at `http://localhost:3000`

## 📦 Adding More Images

1. Add images to the `data` directory
2. Rebuild the index:
   ```powershell
   python src\indexer.py
   ```
3. Restart the Flask server

## 🎨 Testing the Application

1. **Upload an image**: Drag and drop or click to browse
2. **Adjust results**: Change the number of similar images (1-50)
3. **Search**: Click "Search Similar Images"
4. **Browse**: Click "Load Random Images" to see your dataset

## 📊 System Status

To check the system status, visit:
```
http://localhost:5000/api/health
```

This will show:
- Server status
- Number of indexed images
- Whether the index is loaded

## 🛠️ Manual Setup (If Starting Fresh)

If you need to set up everything from scratch:

```powershell
# 1. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Build React frontend
cd frontend
npm install
npm run build
cd ..

# 4. Add images to data directory
# (Copy your images to the data folder)

# 5. Build image index
python src\indexer.py

# 6. Start server
python app.py
```

## 🎯 Expected Results

When everything is working:
- Flask server starts on `http://localhost:5000`
- You see "System ready! X images indexed" message
- You can upload images and get similarity results
- Images load in the results grid with similarity scores

## 📞 Need Help?

If you're still having issues:

1. Check that Python 3.8+ is installed: `python --version`
2. Check that Node.js is installed: `node --version`
3. Verify virtual environment is active (you should see `(venv)` in prompt)
4. Look at the Flask console for error messages
5. Check the browser console (F12) for JavaScript errors

## ✨ Success Checklist

- [ ] Virtual environment is active
- [ ] Python dependencies are installed
- [ ] React build exists at `frontend/build/index.html`
- [ ] Image index exists at `models/image_features.pkl`
- [ ] Images exist in the `data` directory
- [ ] Flask server starts without errors
- [ ] Browser shows the React interface
- [ ] Can upload and search for similar images

---

**You're all set! Enjoy using the AI-Powered Image Similarity Search! 🎉**
