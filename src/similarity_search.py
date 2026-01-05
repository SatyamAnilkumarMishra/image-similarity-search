import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class SimilaritySearch:
    """Find similar images using cosine similarity on feature vectors"""
    
    def __init__(self):
        self.features = None
        self.image_paths = None
        self.is_indexed = False
    
    def load_index(self):
        """Load pre-computed feature index from disk"""
        try:
            with open(config.FEATURES_FILE, 'rb') as f:
                self.features = pickle.load(f)
            
            with open(config.IMAGE_PATHS_FILE, 'rb') as f:
                self.image_paths = pickle.load(f)
            
            self.is_indexed = True
            print(f"Loaded index with {len(self.image_paths)} images")
            return True
            
        except FileNotFoundError:
            print("No index found. Please build index first.")
            return False
        except Exception as e:
            print(f"Error loading index: {str(e)}")
            return False
    
    def save_index(self, features, image_paths):
        """Save feature index to disk"""
        try:
            with open(config.FEATURES_FILE, 'wb') as f:
                pickle.dump(features, f)
            
            with open(config.IMAGE_PATHS_FILE, 'wb') as f:
                pickle.dump(image_paths, f)
            
            self.features = features
            self.image_paths = image_paths
            self.is_indexed = True
            print(f"Saved index with {len(image_paths)} images")
            return True
            
        except Exception as e:
            print(f"Error saving index: {str(e)}")
            return False
    
    def compute_similarity(self, query_features):
        """
        Compute cosine similarity between query and all indexed images
        
        Args:
            query_features: Feature vector of query image
            
        Returns:
            Array of similarity scores (0 to 1, higher is more similar)
        """
        if not self.is_indexed:
            raise ValueError("Index not loaded. Call load_index() first.")
        
        # Reshape for sklearn
        query_features = query_features.reshape(1, -1)
        
        # Compute cosine similarity
        similarities = cosine_similarity(query_features, self.features)[0]
        
        return similarities
    
    def find_similar_images(self, query_features, top_k=None):
        """
        Find top K most similar images to the query
        
        Args:
            query_features: Feature vector of query image
            top_k: Number of similar images to return (default from config)
            
        Returns:
            List of tuples: (image_path, similarity_score)
        """
        if top_k is None:
            top_k = config.TOP_K
        
        # Compute similarities
        similarities = self.compute_similarity(query_features)
        
        # Get top K indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Build results
        results = []
        for idx in top_indices:
            results.append({
                'path': self.image_paths[idx],
                'similarity': float(similarities[idx])
            })
        
        return results
    
    def find_similar_by_index(self, query_index, top_k=None):
        """
        Find similar images given the index of an image in the database
        
        Args:
            query_index: Index of the query image
            top_k: Number of similar images to return
            
        Returns:
            List of similar images (excluding the query itself)
        """
        if top_k is None:
            top_k = config.TOP_K
        
        query_features = self.features[query_index]
        results = self.find_similar_images(query_features, top_k + 1)
        
        # Remove the query image itself
        results = [r for r in results if r['path'] != self.image_paths[query_index]]
        
        return results[:top_k]


if __name__ == "__main__":
    # Test similarity search
    searcher = SimilaritySearch()
    if searcher.load_index():
        print(f"Similarity search ready with {len(searcher.image_paths)} images")
