// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const searchBtn = document.getElementById('searchBtn');
const topKInput = document.getElementById('topK');
const querySection = document.getElementById('querySection');
const queryImage = document.getElementById('queryImage');
const resultsSection = document.getElementById('resultsSection');
const resultsGrid = document.getElementById('resultsGrid');
const resultCount = document.getElementById('resultCount');
const loader = document.getElementById('loader');
const statusDiv = document.getElementById('status');
const browseBtn = document.getElementById('browseBtn');
const browseGrid = document.getElementById('browseGrid');

let selectedFile = null;

// Check server status on load
window.addEventListener('load', checkServerStatus);

async function checkServerStatus() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (data.status === 'ok') {
            if (data.indexed) {
                showStatus(`✓ System ready! ${data.total_images} images indexed.`, 'success');
            } else {
                showStatus('⚠ No image index found. Please run indexer.py first.', 'error');
            }
        }
    } catch (error) {
        showStatus('✗ Unable to connect to server.', 'error');
    }
}

function showStatus(message, type) {
    statusDiv.textContent = message;
    statusDiv.className = `status ${type}`;
}

// Upload box interactions
uploadBox.addEventListener('click', () => fileInput.click());

uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleFileSelect(file);
    }
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileSelect(file);
    }
});

function handleFileSelect(file) {
    selectedFile = file;
    searchBtn.disabled = false;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        queryImage.src = e.target.result;
        querySection.style.display = 'block';
        resultsSection.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// Search similar images
searchBtn.addEventListener('click', searchSimilarImages);

async function searchSimilarImages() {
    if (!selectedFile) return;
    
    // Show loader
    loader.style.display = 'block';
    resultsSection.style.display = 'none';
    searchBtn.disabled = true;
    
    try {
        const formData = new FormData();
        formData.append('image', selectedFile);
        formData.append('top_k', topKInput.value);
        
        const response = await fetch('/api/search', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Search failed');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
        console.error(error);
    } finally {
        loader.style.display = 'none';
        searchBtn.disabled = false;
    }
}

function displayResults(data) {
    resultsGrid.innerHTML = '';
    resultCount.textContent = `(${data.count} results)`;
    
    data.results.forEach((result, index) => {
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';
        
        const similarity = (result.similarity * 100).toFixed(1);
        
        resultItem.innerHTML = `
            <img src="/${result.path}" alt="Similar image ${index + 1}" loading="lazy">
            <div class="similarity-badge">${similarity}%</div>
        `;
        
        resultsGrid.appendChild(resultItem);
    });
    
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Browse random images
browseBtn.addEventListener('click', loadRandomImages);

async function loadRandomImages() {
    browseBtn.disabled = true;
    browseBtn.textContent = 'Loading...';
    
    try {
        const response = await fetch('/api/random?count=20');
        const data = await response.json();
        
        browseGrid.innerHTML = '';
        
        data.results.forEach((result, index) => {
            const resultItem = document.createElement('div');
            resultItem.className = 'result-item';
            
            resultItem.innerHTML = `
                <img src="/${result.path}" alt="Image ${index + 1}" loading="lazy">
            `;
            
            browseGrid.appendChild(resultItem);
        });
        
    } catch (error) {
        showStatus(`Error loading images: ${error.message}`, 'error');
    } finally {
        browseBtn.disabled = false;
        browseBtn.textContent = 'Load Random Images';
    }
}

// Error image handling
document.addEventListener('error', (e) => {
    if (e.target.tagName === 'IMG') {
        e.target.style.display = 'none';
    }
}, true);
