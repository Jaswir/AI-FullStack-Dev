from html2image import Html2Image
import cv2
import numpy as np
import re

import ai_secret_sauce
import image_to_code

GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
RESET = "\033[0m"


# def htmlToPNG():
#     hti = Html2Image(output_path="./image_feedback")
#     file_path_html = "./my_website/index.html"
#     file_path_css = "./my_website/styles.css"
#     hti.screenshot(
#         html_file=file_path_html, css_file=file_path_css, save_as="output.png"
#     )


def verticallyConcatImages():
    image_names = [
        "./image_feedback/input_mock_website.png",
        "./image_feedback/output.png",
    ]
    images = []
    max_width = 0  # find the max width of all the images
    total_height = 0  # the total height of the images (vertical stacking)

    for name in image_names:
        # open all images and find their sizes
        images.append(cv2.imread(name))
        if images[-1].shape[1] > max_width:
            max_width = images[-1].shape[1]
        total_height += images[-1].shape[0]

    # create a new array with a size large enough to contain all the images
    final_image = np.zeros((total_height, max_width, 3), dtype=np.uint8)

    current_y = (
        0  # keep track of where your current image was last placed in the y coordinate
    )
    for image in images:
        # add an image to the final array and increment the y coordinate
        final_image[current_y : image.shape[0] + current_y, : image.shape[1], :] = image
        current_y += image.shape[0]

    cv2.imwrite("./image_feedback/fin.png", final_image)


def letGPT4EvaluateAndImproveItsWork():
    # Sets output Image
    # htmlToPNG()
    verticallyConcatImages()

    current_code = image_to_code.getCode()
    feedback_prompt = """This image shows 2 images on top the input mockup of 
    a website and below the generated website. 
    Evaluate the resemblance of input and resulting image 
    and improve the code, here's the code: """
    get_code_prompt = """return full html and css code"""

    image_file_path = "./image_feedback/fin.png"

    r1 = ai_secret_sauce.chatbotImageFromFilePath(
        file_path=image_file_path, input=feedback_prompt + current_code
    )
    print(MAGENTA + "r1: " + RESET + r1)
    r2 = ai_secret_sauce.chatbotImageFromFilePath(
        file_path=image_file_path, input=get_code_prompt
    )

    print(YELLOW + "r2: " + RESET + r2)

    return r2
