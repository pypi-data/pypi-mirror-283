import sys
from .compressor import compress_base64_image

def main():
    if len(sys.argv) != 3:
        print("Usage: python -m base64image <base64_string> <quality>")
        sys.exit(1)

    base64_string = sys.argv[1]
    quality = int(sys.argv[2])

    compressed_base64_str = compress_base64_image(base64_string, quality)
    print(f"Compressed Base64 String: {compressed_base64_str}")
    print(f"Length of Compressed Base64 String: {len(compressed_base64_str)}")

if __name__ == "__main__":
    main()
