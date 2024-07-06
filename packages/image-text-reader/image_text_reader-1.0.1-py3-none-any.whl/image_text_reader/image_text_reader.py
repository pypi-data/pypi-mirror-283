import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.convert('L')
    image = image.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    return image

def ocr_image(image_path, tesseract_cmd=None):
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    image = preprocess_image(image_path)
    text = pytesseract.image_to_string(image, lang='hun')
    return text