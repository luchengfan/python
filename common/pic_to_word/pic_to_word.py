'''
功能描述：识别图片中的文字
'''
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'F:\Program Files\Tesseract-OCR\tesseract.exe'
text_eng = pytesseract.image_to_string(Image.open('python.png'))
print(text_eng)

text_chi = pytesseract.image_to_string(Image.open('denggao.jpg') , lang = 'chi_sim')
print("\n" , text_chi)
