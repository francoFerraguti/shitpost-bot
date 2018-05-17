from PIL import Image
import os
import random
import json

CONST_TEMPLATES_PATH = "./templates"
CONST_SOURCE_IMAGES_PATH = "./source_images"
CONST_MEMES_PATH = "./memes"
CONST_MEME_NUMBER = 10

CONST_CHROMA_COLORS = [(55, 255, 9)]

def getTemplates(path):
	templates = []

	for file in os.listdir(path):
	    if file.endswith(".jpg") or file.endswith(".png"):
	        templates.append(path + "/" + file)

	print("TOTAL TEMPLATES: " + str(len(templates)))

	return templates

def getTemplateCoordinates(template):
	pixels = template.load()

	left = 9999999
	top = 9999999
	right = 0
	down = 0

	for y in range(template.height):
		for x in range(template.width):
			if pixels[x, y] == (55, 255, 9):
				left = x if (x < left) else left
				top = y if (y < top) else top
				right = x if (x > right) else right
				down = y if (y > down) else down

	return (left, top, right, down)

def getSourceImages(path):
	source_images = []

	for file in os.listdir(path):
	    if file.endswith(".jpg") or file.endswith(".png"):
	        source_images.append(path + "/" + file)

	print("TOTAL SOURCE IMAGES: " + str(len(source_images)))
	return source_images

def getResultFilename(path):
	c = 0

	for file in os.listdir(path):
	    if file.endswith(".png"):
	        c+=1
	return str(c)


for i in range(0, CONST_MEME_NUMBER):
	print("----------------------------------------")
	print("Starting bot")
	print("")

	templates = getTemplates(CONST_TEMPLATES_PATH)
	source_images = getSourceImages(CONST_SOURCE_IMAGES_PATH)

	template = Image.open(random.choice(templates))
	source_image = Image.open(random.choice(source_images))

	print("SELECTED TEMPLATE: " + os.path.basename(template.filename))
	print("SELECTED SOURCE IMAGE: " + os.path.basename(source_image.filename))

	templatecoordinates = getTemplateCoordinates(template)

	newsize = (templatecoordinates[2] - templatecoordinates[0], templatecoordinates[3] - templatecoordinates[1])

	source_image = source_image.resize(newsize)

	template.paste(source_image, templatecoordinates)

	template.save(CONST_MEMES_PATH + "/"+ getResultFilename(CONST_MEMES_PATH) +".png")

	print("----------------------------------------")



