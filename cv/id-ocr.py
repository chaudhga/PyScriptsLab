from PIL import Image
from pytesseract import image_to_string

print(image_to_string(Image.open('hkdid_new_test.png'), lang='chi_sim'))
print(image_to_string(Image.open('Macau_id_card2.jpg'), lang='chi_sim'))

