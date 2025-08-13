import os
import sys
from PIL import Image
import io

def resize_image(input_path, output_path, scale=0.5):
    """
    Resize an image to a percentage of its original size
    
    Parameters:
    input_path (str): Path to the input image
    output_path (str): Path to save the resized image
    scale (float): Scale factor (default: 0.5 for 50%)
    """
    try:
        # Open the image
        with Image.open(input_path) as image:
            # Get original dimensions
            width, height = image.size
            print(f"Original image size: {width}x{height}")
            
            # Calculate new dimensions
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            # Resize the image
            resized_image = image.resize((new_width, new_height))
            print(f"Resized image size: {new_width}x{new_height}")
            
            # Save the resized image
            resized_image.save(output_path)
            print(f"Resized image saved to: {output_path}")
            
            return True
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_locally.py <input_image_path> [output_image_path] [scale]")
        print("Example: python test_locally.py test.jpg resized_test.jpg 0.5")
        return
    
    input_path = sys.argv[1]
    
    # Set default output path if not provided
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        filename, ext = os.path.splitext(os.path.basename(input_path))
        output_path = f"resized_{filename}{ext}"
    
    # Set default scale if not provided
    scale = 0.5
    if len(sys.argv) >= 4:
        try:
            scale = float(sys.argv[3])
        except ValueError:
            print("Scale must be a number. Using default scale of 0.5.")
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' does not exist.")
        return
    
    # Resize the image
    success = resize_image(input_path, output_path, scale)
    
    if success:
        print("\nImage processing completed successfully!")
        print("This simulates the functionality of the Lambda function.")
        print("When deployed to AWS, this process will be triggered automatically when an image is uploaded to the source S3 bucket.")

if __name__ == "__main__":
    main()