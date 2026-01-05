"""
Download sample images for testing the image similarity search system.
This script downloads a small set of diverse images from public sources.
"""

import os
import requests
from pathlib import Path
import config

# Sample image URLs (free stock photos)
SAMPLE_IMAGES = [
    "https://picsum.photos/800/600?random=1",
    "https://picsum.photos/800/600?random=2",
    "https://picsum.photos/800/600?random=3",
    "https://picsum.photos/800/600?random=4",
    "https://picsum.photos/800/600?random=5",
    "https://picsum.photos/800/600?random=6",
    "https://picsum.photos/800/600?random=7",
    "https://picsum.photos/800/600?random=8",
    "https://picsum.photos/800/600?random=9",
    "https://picsum.photos/800/600?random=10",
    "https://picsum.photos/800/600?random=11",
    "https://picsum.photos/800/600?random=12",
    "https://picsum.photos/800/600?random=13",
    "https://picsum.photos/800/600?random=14",
    "https://picsum.photos/800/600?random=15",
    "https://picsum.photos/800/600?random=16",
    "https://picsum.photos/800/600?random=17",
    "https://picsum.photos/800/600?random=18",
    "https://picsum.photos/800/600?random=19",
    "https://picsum.photos/800/600?random=20",
]


def download_images():
    """Download sample images to data directory"""
    
    # Create data directory if it doesn't exist
    os.makedirs(config.DATA_DIR, exist_ok=True)
    
    print("Downloading sample images...")
    print(f"Target directory: {config.DATA_DIR}")
    print("=" * 50)
    
    for idx, url in enumerate(SAMPLE_IMAGES, 1):
        try:
            print(f"Downloading image {idx}/{len(SAMPLE_IMAGES)}...", end=" ")
            
            # Download image
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Save image
            filename = f"sample_{idx:03d}.jpg"
            filepath = os.path.join(config.DATA_DIR, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Saved as {filename}")
            
        except Exception as e:
            print(f"✗ Failed: {str(e)}")
    
    print("=" * 50)
    print(f"Download complete! Images saved to: {config.DATA_DIR}")
    print("\nNext steps:")
    print("1. Run 'python src/indexer.py' to build the feature index")
    print("2. Run 'python app.py' to start the web server")


if __name__ == "__main__":
    download_images()
