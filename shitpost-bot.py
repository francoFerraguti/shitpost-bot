from PIL import Image
import os
import random
import json

CONST_TEMPLATES_PATH = "./templates"
CONST_SOURCE_IMAGES_PATH = "./source_images"
CONST_MEMES_PATH = "./memes"

templates = []
source_images = []

print("----------------------------------------")
print("Starting bot")
print("")

for file in os.listdir(CONST_TEMPLATES_PATH):
    if file.endswith(".jpg") or file.endswith(".png"):
        templates.append(CONST_TEMPLATES_PATH + "/" + file)
        print("Added template: " + CONST_TEMPLATES_PATH + "/" + file + " to the bot")

print("")
print("TOTAL TEMPLATES: " + str(len(templates)))
print("")

template = Image.open(random.choice(templates))
print("Selected template: " + template.filename)

templatecoordinates = (0, 0, 0, 0)

with open(CONST_TEMPLATES_PATH + '/templates.json') as templates_json:
    data = json.load(templates_json)
    for template_data in data:
    	if CONST_TEMPLATES_PATH + "/" + template_data["filename"] == template.filename:
    		templatecoordinates = (template_data["left"], template_data["top"], template_data["right"], template_data["down"])

print("Selected coordinates: " + str(templatecoordinates))
print("")

for file in os.listdir(CONST_SOURCE_IMAGES_PATH):
    if file.endswith(".jpg") or file.endswith(".png"):
        source_images.append(CONST_SOURCE_IMAGES_PATH + "/" + file)
        print("Added source image: " + CONST_TEMPLATES_PATH + "/" + file + " to the bot")

print("")
print("TOTAL SOURCE IMAGES: " + str(len(source_images)))
print("")

source_image = Image.open(random.choice(source_images))
print("Selected source image: " + source_image.filename)

print("")
print(">>>>>>>>STARTING MEME GENERATION<<<<<<<<<")
print("Source image old size: " + str(source_image.size))

newsize = (templatecoordinates[2] - templatecoordinates[0], templatecoordinates[3] - templatecoordinates[1])
print("Source image new size: " + str(newsize))

source_image = source_image.resize(newsize)
print("Source image actual size: " + str(source_image.size))

template.paste(source_image, templatecoordinates)

print("")
print("Meme generated! Saving to: " + CONST_MEMES_PATH + "/meme.png")

template.save(CONST_MEMES_PATH + "/meme.png")

print("----------------------------------------")
