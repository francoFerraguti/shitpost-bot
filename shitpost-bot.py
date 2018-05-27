from PIL import Image
import os
import random
import json

CONST_TEMPLATES_PATH = "./templates"
CONST_SOURCE_IMAGES_PATH = "./source_images"
CONST_MEMES_PATH = "./memes"
CONST_MEME_NUMBER = 40
CONST_COLOR_MAX_DELTA = 0

CONST_CHROMA_COLORS = [
    (254, 34, 34),  # Red
    (0, 255, 1),  # Lime
    (0, 0, 254),  # Blue
    (92, 42, 131),  # Magenta
    (255, 126, 255),  # Pink
    (254, 244, 0),  # Yellow
    (255, 180, 0),  # Gold
    (0, 114, 138),  # GrayBlue
    (43, 186, 202),  # LightBlue
]


def tupleToString(t):
    return "".join(str(x) for x in t)


def getTemplates(path):
    templates = []

    for file in os.listdir(path):
        if file.endswith(".jpg") or file.endswith(".png"):
            templates.append(path + "/" + file)

    print("TOTAL TEMPLATES: " + str(len(templates)))

    return templates


def colorsMatch(color1, color2):
    redDelta = abs(color1[0] - color2[0])
    greenDelta = abs(color1[1] - color2[1])
    blueDelta = abs(color1[2] - color2[2])

    if redDelta <= CONST_COLOR_MAX_DELTA and greenDelta <= CONST_COLOR_MAX_DELTA and blueDelta <= CONST_COLOR_MAX_DELTA:
        return True

    return False


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
                if colorsMatch(pixels[x, y], color):
                    left[tupleToString(color)] = x if (
                        x < left[tupleToString(color)]
                    ) else left[tupleToString(color)]
                    top[tupleToString(color)] = y if (
                        y < top[tupleToString(color)]
                    ) else top[tupleToString(color)]
                    right[tupleToString(color)] = x if (
                        x > right[tupleToString(color)]
                    ) else right[tupleToString(color)]
                    down[tupleToString(color)] = y if (
                        y > down[tupleToString(color)]
                    ) else down[tupleToString(color)]

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
            c += 1
    return str(c)


def colorDataIsIncorrect(templateCoordinates, color):
    return templateCoordinates[0][color] == 9999999 and templateCoordinates[1][color] == 9999999 and templateCoordinates[2][color] == 0 and templateCoordinates[3][color] == 0


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
        if colorDataIsIncorrect(templatecoordinates, tupleToString(color)):
            continue

        source_image = Image.open(random.choice(source_images))
        print("SELECTED SOURCE IMAGE: " +
              os.path.basename(source_image.filename))

        source_images = [
            x for x in source_images if Image.open(x) != source_image
        ]  # Takes out source_image from pool

        newsize = (templatecoordinates[2][tupleToString(color)] -
                   templatecoordinates[0][tupleToString(color)],
                   templatecoordinates[3][tupleToString(color)] -
                   templatecoordinates[1][tupleToString(color)])

        if newsize[0] == 0 or newsize[1] == 0:
            continue

        source_image = source_image.resize(newsize)

        template.paste(source_image,
                       (templatecoordinates[0][tupleToString(color)],
                        templatecoordinates[1][tupleToString(color)],
                        templatecoordinates[2][tupleToString(color)],
                        templatecoordinates[3][tupleToString(color)]))

    template.save(CONST_MEMES_PATH + "/" +
                  getResultFilename(CONST_MEMES_PATH) + ".png")

    print("Finished meme number " + str(i + 1))
    print("----------------------------------------")
