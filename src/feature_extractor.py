import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Reduce TensorFlow logging
import tensorflow as tf
import keras
from keras.applications import ResNet50
from keras.applications.resnet50 import preprocess_input
from keras.utils import load_img, img_to_array
from keras.models import Model
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class FeatureExtractor:
    """Extract deep learning features from images using pre-trained ResNet50"""
    
    def __init__(self):
        # Load pre-trained ResNet50 model without top classification layer
        base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
        self.model = Model(inputs=base_model.input, outputs=base_model.output)
        print(f"Feature extractor initialized with {config.MODEL_NAME}")
        print(f"Feature vector dimension: {self.model.output_shape[1]}")
    
    def extract_features(self, img_path):
        """
        Extract features from a single image
        
        Args:
            img_path: Path to the image file
            
        Returns:
            Normalized feature vector (numpy array)
        """
        try:
            # Load and preprocess image
            img = load_img(img_path, target_size=config.IMAGE_SIZE)
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            # Extract features
            features = self.model.predict(img_array, verbose=0)
            
            # Normalize features (L2 normalization)
            features = features.flatten()
            features = features / np.linalg.norm(features)
            
            return features
            
        except Exception as e:
            print(f"Error extracting features from {img_path}: {str(e)}")
            return None
    
    def extract_features_batch(self, img_paths, batch_size=None):
        """
        Extract features from multiple images in batches
        
        Args:
            img_paths: List of image file paths
            batch_size: Batch size for processing (default from config)
            
        Returns:
            Array of feature vectors
        """
        if batch_size is None:
            batch_size = config.BATCH_SIZE
        
        features_list = []
        total = len(img_paths)
        
        for i in range(0, total, batch_size):
            batch_paths = img_paths[i:i + batch_size]
            batch_images = []
            
            for img_path in batch_paths:
                try:
                    img = load_img(img_path, target_size=config.IMAGE_SIZE)
                    img_array = img_to_array(img)
                    batch_images.append(img_array)
                except Exception as e:
                    print(f"Error loading {img_path}: {str(e)}")
                    continue
            
            if batch_images:
                # Preprocess batch
                batch_array = np.array(batch_images)
                batch_array = preprocess_input(batch_array)
                
                # Extract features
                batch_features = self.model.predict(batch_array, verbose=0)
                
                # Normalize each feature vector
                for features in batch_features:
                    features = features.flatten()
                    features = features / np.linalg.norm(features)
                    features_list.append(features)
            
            print(f"Processed {min(i + batch_size, total)}/{total} images")
        
        return np.array(features_list)


if __name__ == "__main__":
    # Test feature extractor
    extractor = FeatureExtractor()
    print("Feature extractor is ready!")
