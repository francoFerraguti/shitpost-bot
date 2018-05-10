from PIL import Image
import os

CONST_TEMPLATES_PATH = "./templates"

for file in os.listdir(CONST_TEMPLATES_PATH):
	if file.endswith(".jpg") or file.endswith(".png"):
		
		image = Image.open(CONST_TEMPLATES_PATH + "/" + file)

		filename, fileextension = os.path.splitext(file)
		print (filename)
