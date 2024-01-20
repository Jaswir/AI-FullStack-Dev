from html2image import Html2Image
import cv2
import numpy as np


def htmlToPNG():
    hti = Html2Image(output_path="./image_feedback")
    file_path_html = "./my_website/index.html"
    hti.screenshot(html_file=file_path_html, save_as="output.png")



image_names = ['./image_feedback/input_mock_website.png', './image_feedback/output.png',]
images = []
max_width = 0 # find the max width of all the images
total_height = 0 # the total height of the images (vertical stacking)

for name in image_names:
    # open all images and find their sizes
    images.append(cv2.imread(name))
    if images[-1].shape[1] > max_width:
        max_width = images[-1].shape[1]
    total_height += images[-1].shape[0]

# create a new array with a size large enough to contain all the images
final_image = np.zeros((total_height,max_width,3),dtype=np.uint8)

current_y = 0 # keep track of where your current image was last placed in the y coordinate
for image in images:
    # add an image to the final array and increment the y coordinate
    final_image[current_y:image.shape[0]+current_y,:image.shape[1],:] = image
    current_y += image.shape[0]

cv2.imwrite('fin.PNG',final_image)