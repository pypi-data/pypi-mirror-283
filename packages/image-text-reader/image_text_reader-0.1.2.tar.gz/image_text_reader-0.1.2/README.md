# Image Text Reader

The `image-text-reader` library allows you to extract text from images using Optical Character Recognition (OCR) with the help of the `pytesseract` library and `Pillow` for image processing.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.x
- Tesseract-OCR

## Installation

1. **Install the required Python libraries:**

    ```bash
    pip install image-text-reader
    ```

2. **Install Tesseract-OCR:**
    - **Windows:** Download and install from [here](https://github.com/UB-Mannheim/tesseract/wiki).
    - **macOS:** Use Homebrew to install:

      ```bash
      brew install tesseract
      ```

    - **Linux:** Use your package manager, for example:

      ```bash
      sudo apt-get install tesseract-ocr
      ```

## Usage

1. **Create a Python script** (e.g., `test_script.py`) and import the `ocr_image` function from the `image_text_reader` library:

    ```python
    from image_text_reader import ocr_image
    ```

2. **Set the path to your image and Tesseract-OCR executable:**

    ```python
    # Update these paths for your system
    image_path = 'C:/path_to_your_image.jpg'  # Replace with the path to your test image
    tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'  # Path to Tesseract executable

    extracted_text = ocr_image(image_path, tesseract_cmd=tesseract_cmd)
    print("Extracted Text:")
    print(extracted_text)
    ```

3. **Run your script:**

    ```bash
    python test_script.py
    ```

## Code Explanation

- **Preprocessing Function:**

    The `preprocess_image` function prepares the image for OCR by converting it to grayscale, sharpening it, and enhancing its contrast:

    ```python
    def preprocess_image(image_path):
        image = Image.open(image_path).convert('L')
        image = image.filter(ImageFilter.SHARPEN)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)
        return image
    ```

- **OCR Function:**

    The `ocr_image` function processes the image and then extracts the text using `pytesseract`:

    ```python
    def ocr_image(image_path, tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        image = preprocess_image(image_path)
        text = pytesseract.image_to_string(image, lang='eng')
        return text
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

For more information, visit the [image-text-reader library page on PyPI](https://pypi.org/project/image-text-reader/).
