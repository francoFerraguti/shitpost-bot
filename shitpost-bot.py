from PIL import Image
import os
import random
import json

CONST_TEMPLATES_PATH = "./templates"
CONST_SOURCE_IMAGES_PATH = "./source_images"
CONST_MEMES_PATH = "./memes"
CONST_MEME_NUMBER = 10

CONST_CHROMA_COLORS = [(55, 255, 9)]

def tupleToString(t):
	return "".join(str(x) for x in t)

def getTemplates(path):
	templates = []

	for file in os.listdir(path):
	    if file.endswith(".jpg") or file.endswith(".png"):
	        templates.append(path + "/" + file)

	print("TOTAL TEMPLATES: " + str(len(templates)))

	return templates

def getTemplateCoordinates(template):
	pixels = template.load()

	left = {}
	top = {}
	right = {}
	down = {}

	for color in CONST_CHROMA_COLORS:
		left[tupleToString(color)] = 9999999
		top[tupleToString(color)] = 9999999
		right[tupleToString(color)] = 0
		down[tupleToString(color)] = 0

	for y in range(template.height):
		for x in range(template.width):
			for color in CONST_CHROMA_COLORS:
				if pixels[x, y] == color:
					left[tupleToString(color)] = x if (x < left[tupleToString(color)]) else left[tupleToString(color)]
					top[tupleToString(color)] = y if (y < top[tupleToString(color)]) else top[tupleToString(color)]
					right[tupleToString(color)] = x if (x > right[tupleToString(color)]) else right[tupleToString(color)]
					down[tupleToString(color)] = y if (y > down[tupleToString(color)]) else down[tupleToString(color)]

	for color in CONST_CHROMA_COLORS:
		print(str(left[tupleToString(color)]))
		print(str(top[tupleToString(color)]))
		print(str(right[tupleToString(color)]))
		print(str(down[tupleToString(color)]))

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

	print("SELECTED TEMPLATE: " + os.path.basename(template.filename))

	templatecoordinates = getTemplateCoordinates(template)

	for color in CONST_CHROMA_COLORS:
		source_image = Image.open(random.choice(source_images))
		print("SELECTED SOURCE IMAGE: " + os.path.basename(source_image.filename))

		newsize = (templatecoordinates[2][tupleToString(color)] - templatecoordinates[0][tupleToString(color)], templatecoordinates[3][tupleToString(color)] - templatecoordinates[1][tupleToString(color)])

		source_image = source_image.resize(newsize)

		template.paste(source_image, (templatecoordinates[0][tupleToString(color)], templatecoordinates[1][tupleToString(color)], templatecoordinates[2][tupleToString(color)], templatecoordinates[3][tupleToString(color)]))

	template.save(CONST_MEMES_PATH + "/"+ getResultFilename(CONST_MEMES_PATH) +".png")

	print("----------------------------------------")



