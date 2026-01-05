import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directories
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
UPLOAD_DIR = os.path.join(STATIC_DIR, 'uploads')

# Model configuration
MODEL_NAME = 'ResNet50'
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

# Feature extraction
FEATURES_FILE = os.path.join(MODELS_DIR, 'image_features.pkl')
IMAGE_PATHS_FILE = os.path.join(MODELS_DIR, 'image_paths.pkl')

# Similarity search
TOP_K = 10  # Number of similar images to return

# Flask configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
