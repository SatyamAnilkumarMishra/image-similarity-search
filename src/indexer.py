import os
import sys
import glob
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from feature_extractor import FeatureExtractor
from similarity_search import SimilaritySearch


class ImageIndexer:
    """Index images by extracting and storing their features"""
    
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.similarity_search = SimilaritySearch()
    
    def get_image_files(self, directory):
        """
        Recursively find all image files in directory
        
        Args:
            directory: Root directory to search
            
        Returns:
            List of image file paths
        """
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
        image_files = []
        
        for ext in extensions:
            pattern = os.path.join(directory, '**', ext)
            image_files.extend(glob.glob(pattern, recursive=True))
        
        # Also check uppercase extensions
        for ext in extensions:
            pattern = os.path.join(directory, '**', ext.upper())
            image_files.extend(glob.glob(pattern, recursive=True))
        
        return sorted(list(set(image_files)))
    
    def build_index(self, image_directory):
        """
        Build feature index for all images in directory
        
        Args:
            image_directory: Directory containing images to index
            
        Returns:
            True if successful, False otherwise
        """
        print(f"Scanning for images in: {image_directory}")
        image_paths = self.get_image_files(image_directory)
        
        if not image_paths:
            print(f"No images found in {image_directory}")
            return False
        
        print(f"Found {len(image_paths)} images")
        print("Extracting features...")
        
        # Extract features for all images
        features = self.feature_extractor.extract_features_batch(image_paths)
        
        if len(features) == 0:
            print("Failed to extract features from any images")
            return False
        
        print(f"Successfully extracted features from {len(features)} images")
        
        # Save index
        self.similarity_search.save_index(features, image_paths)
        
        print("Index building complete!")
        return True
    
    def add_images_to_index(self, new_image_paths):
        """
        Add new images to existing index
        
        Args:
            new_image_paths: List of new image paths to add
            
        Returns:
            True if successful, False otherwise
        """
        # Load existing index
        if not self.similarity_search.load_index():
            print("No existing index found. Use build_index() instead.")
            return False
        
        # Extract features for new images
        print(f"Adding {len(new_image_paths)} new images to index...")
        new_features = self.feature_extractor.extract_features_batch(new_image_paths)
        
        if len(new_features) == 0:
            print("Failed to extract features from new images")
            return False
        
        # Combine with existing features
        import numpy as np
        combined_features = np.vstack([
            self.similarity_search.features,
            new_features
        ])
        combined_paths = self.similarity_search.image_paths + new_image_paths
        
        # Save updated index
        self.similarity_search.save_index(combined_features, combined_paths)
        
        print(f"Added {len(new_features)} images. Total images: {len(combined_paths)}")
        return True


def main():
    """Main function to build index from data directory"""
    indexer = ImageIndexer()
    
    # Build index from data directory
    data_dir = config.DATA_DIR
    
    if not os.path.exists(data_dir):
        print(f"Data directory not found: {data_dir}")
        print("Please create the directory and add images to it.")
        return
    
    indexer.build_index(data_dir)


if __name__ == "__main__":
    main()
