from PIL import Image
import os
import random
import json

CONST_TEMPLATES_PATH = "./templates"
CONST_SOURCE_IMAGES_PATH = "./source_images"
CONST_MEMES_PATH = "./memes"
CONST_MEME_NUMBER = 10

def getTemplates(path):
	templates = []

	for file in os.listdir(path):
	    if file.endswith(".jpg") or file.endswith(".png"):
	        templates.append(path + "/" + file)

	print("TOTAL TEMPLATES: " + str(len(templates)))

	return templates

def getTemplateCoordinates(template, path):
	templatecoordinates = (0, 0, 0, 0)

	with open(path + '/templates.json') as templates_json:
		data = json.load(templates_json)
		for template_data in data:
			if path + "/" + template_data["filename"] == template.filename:
				templatecoordinates = (template_data["left"], template_data["top"], template_data["right"], template_data["down"])
				return templatecoordinates


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

	templatecoordinates = getTemplateCoordinates(template, CONST_TEMPLATES_PATH)

	newsize = (templatecoordinates[2] - templatecoordinates[0], templatecoordinates[3] - templatecoordinates[1])

	source_image = source_image.resize(newsize)

	template.paste(source_image, templatecoordinates)

	template.save(CONST_MEMES_PATH + "/"+ getResultFilename(CONST_MEMES_PATH) +".png")

	print("----------------------------------------")



