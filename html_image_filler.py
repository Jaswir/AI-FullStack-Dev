from bs4 import BeautifulSoup
from b2sdk.v2 import *
from clarifai.client.model import Model
from clarifai.client.input import Inputs
import os


# os.environ["CLARIFAI_PAT"] = 'f3ac13477d814ca79bf0a1d01739e251'

info = InMemoryAccountInfo()
b2_api = B2Api(info)
application_key_id = "0052ef0ca2d41430000000002"
application_key = "K005eb9ELmZNYgglYGhpydbobI1FMUo"
b2_api.authorize_account("production", application_key_id, application_key)


def upload_to_b2(local_path):
    print('uploading to b2')
    local_file_path = local_path
    b2_file_name = local_path
    file_info = {"how": "good-file"}

    bucket = b2_api.get_bucket_by_name("AAAAAAAAAAAA321")
    bucket.upload_local_file(
        local_file=local_file_path,
        file_name=b2_file_name,
        file_infos=file_info,
    )

    url = bucket.get_download_url(b2_file_name)

    return url


def generateImage(image_description: str, src):
    print('generateImage')
    prompt = image_description
    inference_params_dall_e = dict(quality="standard", size='1024x1024')

    model_prediction = Model("https://clarifai.com/openai/dall-e/models/dall-e-3").predict_by_bytes(
        prompt.encode(), input_type="text", inference_params=inference_params_dall_e)

    output_base64 = model_prediction.outputs[0].data.image.base64
    
    with open(f'./static/{src}', 'wb') as f:
        f.write(output_base64)

 
    directory_name = "my_website/app"
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
        os.mkdir(directory_name + '/static')

    with open(f'./my_website/app/static/{src}', 'wb') as f:
        f.write(output_base64)

    return 'image{index}.png'


def generateImageFromAlt(img_element, index):
    soup = BeautifulSoup(img_element, 'html.parser')

    img_tag = soup.find('img')

    if img_tag and 'alt' in img_tag.attrs:
        alt_value = img_tag['alt']
        src =  img_tag['src']
        print(alt_value)
        return generateImage(alt_value, src)
    else:
        return None


def extract_img_elements(html_str):
    soup = BeautifulSoup(html_str, 'html.parser')

    img_tags = soup.find_all('img')

    img_strings = [str(img_tag) for img_tag in img_tags]

    print(img_strings)

    return img_strings


def iterate_and_generate(img_elements):
    img_links = []
    for img_element in img_elements:
        img_links.append(generateImageFromAlt(
            img_element, img_elements.index(img_element)))
    return img_links


def replace_img_srcs(html_str):
    soup = BeautifulSoup(html_str, 'html.parser')

    img_tags = soup.find_all('img')

    for img_tag in img_tags:
        src = img_tag['src']
        img_tag['src'] = './app/static/' + src

    modified_html = str(soup)

    return modified_html

def cleanseImages():
    if os.path.exists('./static'):
        for filename in os.listdir('./static'):
            os.remove(f'./static/{filename}')

    else :
        os.mkdir('./static')
# html_example = """<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Image Descriptions</title>
# </head>
# <body>
#     <h1>Image Gallery</h1>

#     <img src="cat.jpg" alt="A cute cat playing with a ball of yarn">
#     <img src="landscape.jpg" alt="A beautiful landscape with mountains and a lake">
#     <img src="coding.jpg" alt="A person coding on a laptop with lines of code on the screen">
#     <img src="food.jpg" alt="Delicious food spread with a variety of dishes">
#     <img src="travel.jpg" alt="Adventurous travel scene with a backpack and hiking gear">

#     <p>Explore the images above for a delightful experience!</p>
# </body>
# </html>
# """

def fillHTMLImages(html):

    cleanseImages()
    iterate_and_generate(extract_img_elements(html))
    html_with_images = replace_img_srcs(html)
    with open('./my_website/index.html', "w", encoding="utf-8") as html_file:
        html_file.write(html_with_images)

    print(html_with_images)

