from PIL import Image
import io
import base64

def compress_base64_image(base64_str, quality=95):
    """
    Compress a base64 encoded image.

    Parameters:
        base64_str (str): The base64 encoded image string.
        quality (int): The quality of the output image (1-95). Default is 95.

    Returns:
        str: The compressed base64 encoded image string.
    """
    # Decode base64 string to bytes
    image_data = base64.b64decode(base64_str)
    
    # Open the image from bytes
    image = Image.open(io.BytesIO(image_data))
    
    # Create an in-memory bytes buffer to save the compressed image
    buffer = io.BytesIO()
    
    # Save the image into the buffer in JPEG format with the specified quality
    image.save(buffer, format="JPEG", quality=quality)
    
    # Get the byte data from buffer
    compressed_image_data = buffer.getvalue()
    
    # Encode the byte data to base64 string
    compressed_base64_str = base64.b64encode(compressed_image_data).decode('utf-8')

    return compressed_base64_str
