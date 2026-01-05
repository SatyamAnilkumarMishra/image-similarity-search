import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from feature_extractor import FeatureExtractor
from similarity_search import SimilaritySearch
import config

# Determine if we're serving React build or development mode
REACT_BUILD_DIR = os.path.join(os.path.dirname(__file__), 'frontend', 'build')
if os.path.exists(REACT_BUILD_DIR):
    app = Flask(__name__, 
                static_folder='frontend/build/static',
                static_url_path='/static')
else:
    app = Flask(__name__)

CORS(app)
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = config.UPLOAD_DIR

# Initialize components
feature_extractor = None
similarity_search = None


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def initialize_models():
    """Initialize feature extractor and similarity search"""
    global feature_extractor, similarity_search
    
    print("Initializing models...")
    feature_extractor = FeatureExtractor()
    similarity_search = SimilaritySearch()
    
    # Load index
    if not similarity_search.load_index():
        print("Warning: No index loaded. Build index first using indexer.py")
    
    print("Models initialized!")


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'indexed': similarity_search.is_indexed if similarity_search else False,
        'total_images': len(similarity_search.image_paths) if similarity_search and similarity_search.is_indexed else 0
    })


@app.route('/api/search', methods=['POST'])
def search_similar():
    """
    Find similar images based on uploaded image
    
    Expected: multipart/form-data with 'image' file and optional 'top_k' parameter
    Returns: JSON with similar images
    """
    if not similarity_search or not similarity_search.is_indexed:
        return jsonify({'error': 'Index not loaded. Please build index first.'}), 503
    
    # Check if image file is present
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Extract features
        query_features = feature_extractor.extract_features(filepath)
        
        if query_features is None:
            return jsonify({'error': 'Failed to extract features from image'}), 500
        
        # Get top_k parameter
        top_k = request.form.get('top_k', config.TOP_K, type=int)
        
        # Find similar images
        results = similarity_search.find_similar_images(query_features, top_k)
        
        # Check if exact match exists (similarity > 0.99)
        exact_match_found = False
        if results and results[0]['similarity'] > 0.99:
            exact_match_found = True
        
        # Convert absolute paths to API-accessible URLs
        for result in results:
            # Get relative path from data directory for the /images route
            rel_path = os.path.relpath(result['path'], config.DATA_DIR)
            result['path'] = f"images/{rel_path.replace(chr(92), '/')}"
            # Add flag for exact match
            if result['similarity'] > 0.99:
                result['is_exact_match'] = True
        
        response = {
            'query_image': f"/uploads/{unique_filename}",
            'results': results,
            'count': len(results)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/random', methods=['GET'])
def random_images():
    """Get random images from index for browsing"""
    if not similarity_search or not similarity_search.is_indexed:
        return jsonify({'error': 'Index not loaded'}), 503
    
    try:
        import random
        count = request.args.get('count', 20, type=int)
        count = min(count, len(similarity_search.image_paths))
        
        random_paths = random.sample(similarity_search.image_paths, count)
        
        # Convert to API-accessible URLs
        results = []
        for path in random_paths:
            rel_path = os.path.relpath(path, config.DATA_DIR)
            results.append({'path': f"images/{rel_path.replace(chr(92), '/')}"})
        
        return jsonify({'results': results, 'count': len(results)})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve images from data directory"""
    return send_from_directory(config.DATA_DIR, filename)


@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    """Serve uploaded images"""
    return send_from_directory(config.UPLOAD_DIR, filename)


# Catch-all route for React app - MUST BE LAST
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """Serve React app"""
    if not os.path.exists(REACT_BUILD_DIR):
        return jsonify({
            'message': 'React app not built. Run: cd frontend && npm install && npm run build',
            'api_url': 'http://localhost:5000/api/health'
        }), 404
    
    # Always serve index.html for client-side routing
    return send_from_directory(REACT_BUILD_DIR, 'index.html')


if __name__ == '__main__':
    initialize_models()
    print("\n" + "="*50)
    print("Image Similarity Search Server")
    print("="*50)
    print(f"Server running at: http://localhost:5000")
    print(f"Indexed images: {len(similarity_search.image_paths) if similarity_search and similarity_search.is_indexed else 0}")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
