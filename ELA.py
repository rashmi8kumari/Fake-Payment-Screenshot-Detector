from PIL import Image, ImageChops, ImageEnhance
import cv2
import numpy as np

def error_level_analysis(image_path, output_path="lakshtransaction.jpg", quality=90):
    # Open image
    original = Image.open(image_path).convert('RGB')
    
    # Save image with lower quality
    original.save("lakshtransaction.jpg", "JPEG", quality=quality)

    # Re-open saved image
    recompressed = Image.open("lakshtransaction.jpg")

    # Compute difference
    diff = ImageChops.difference(original, recompressed)

    # Enhance the difference
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0 / max_diff if max_diff else 1
    diff = ImageEnhance.Brightness(diff).enhance(scale)

    # Save the ELA image
    diff.save(output_path)
    print(f"ELA analysis saved as {output_path}")

# Test with a screenshot
error_level_analysis("transaction.jpg")
