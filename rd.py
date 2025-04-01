from PIL import Image
import os
from pathlib import Path

# Supported image extensions
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')

def compress_jpeg(img, output_path, quality=85):
    """Compress JPEG image with quality control"""
    img.save(output_path, "JPEG", quality=quality, optimize=True, subsampling=0)

def compress_png(img, output_path):
    """Optimize PNG image"""
    img.save(output_path, "PNG", optimize=True)

def compress_webp(img, output_path, quality=80):
    """Compress image using WebP format"""
    img.save(output_path, "WEBP", quality=quality, method=6)

def resize_image(img, max_size=1200):
    """Resize image while maintaining aspect ratio"""
    if max(img.size) > max_size:
        img.thumbnail((max_size, max_size), Image.LANCZOS)
    return img

def process_images(source_folder, dest_folder, jpeg_quality=85, webp_quality=80, max_size=None):
    """
    Process all images in source folder and save compressed versions in destination folder
    :param source_folder: Folder containing original images
    :param dest_folder: Folder to save compressed images
    :param jpeg_quality: Quality for JPEG compression (1-100)
    :param webp_quality: Quality for WebP compression (1-100)
    :param max_size: Maximum width/height for resizing (None to skip resizing)
    """
    # Create destination folder if it doesn't exist
    Path(dest_folder).mkdir(parents=True, exist_ok=True)
    
    # Process each file in source folder
    for filename in os.listdir(source_folder):
        # Check if file is a supported image
        if filename.lower().endswith(SUPPORTED_EXTENSIONS):
            try:
                filepath = os.path.join(source_folder, filename)
                with Image.open(filepath) as img:
                    # Convert to RGB if image is in RGBA or other mode
                    if img.mode in ('RGBA', 'LA'):
                        img = img.convert('RGB')
                    
                    # Resize if max_size is specified
                    if max_size:
                        img = resize_image(img, max_size)
                    
                    # Get filename without extension
                    base_name = os.path.splitext(filename)[0]
                    
                    # Save compressed versions
                    #compress_jpeg(img, os.path.join(dest_folder, f"{base_name}_compressed.jpg"), jpeg_quality)
                    #compress_png(img, os.path.join(dest_folder, f"{base_name}_optimized.png"))
                    compress_webp(img, os.path.join(dest_folder, f"{base_name}_compressed.webp"), webp_quality)
                    
                    print(f"Processed: {filename}")
                    
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    # Configuration
    SOURCE_FOLDER = "input"  # Replace with your source folder
    DEST_FOLDER = "output"  # Replace with your destination folder
    JPEG_QUALITY = 85  # Quality for JPEG compression (1-100)
    WEBP_QUALITY = 80  # Quality for WebP compression (1-100)
    MAX_SIZE = 1200    # Maximum width/height in pixels (None to disable resizing)
    
    # Run the image processing
    process_images(
        source_folder=SOURCE_FOLDER,
        dest_folder=DEST_FOLDER,
        jpeg_quality=JPEG_QUALITY,
        webp_quality=WEBP_QUALITY,
        max_size=MAX_SIZE
    )