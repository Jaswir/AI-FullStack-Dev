from clarifai.client.model import Model
from clarifai.client.input import Inputs
import zipfile
import os

# ANSI escape codes for text colors when using print()
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"  # Reset color to default

inference_params = dict(temperature=0.2, max_tokens=250)
conversation = ""


def chatbotImageFile(input, image_file):
    # Temporarily saves the file to directory and read in as bytes
    uploaded_file = image_file
    file_path = os.path.join("tmpDirUploadedImage", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with open(file_path, "rb") as image_file:
        image_bytes = image_file.read()

    global conversation
    conversation += "user: " + input + "\n\n"
    model_prediction = Model(
        "https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision"
    ).predict(
        inputs=[
            Inputs.get_multimodal_input(
                input_id="", image_bytes=image_bytes, raw_text=conversation
            )
        ],
        inference_params=inference_params,
    )
    response = model_prediction.outputs[0].data.text.raw
    conversation += "assistant: " + response + "\n\n"
    return response


def chatbotImageURL(input, image_url):
    global conversation
    conversation += "user: " + input + "\n\n"
    model_prediction = Model(
        "https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision"
    ).predict(
        inputs=[
            Inputs.get_multimodal_input(
                input_id="", image_url=image_url, raw_text=conversation
            )
        ],
        inference_params=inference_params,
    )
    response = model_prediction.outputs[0].data.text.raw
    conversation += "assistant: " + response + "\n\n"
    return response


# Extracts the part between ```html and ``` from raw chat gpt response
def extractHTMLFromResponse(rawHTMLCSS):
    html_without_bullshit_above = rawHTMLCSS.split("```html")[1]
    html = html_without_bullshit_above.split("```")[0]
    return html


# Extracts the part between ```css and ``` from raw chat gpt response
def extractCSSFromResponse(rawHTMLCSS):
    css_without_bullshit_above = rawHTMLCSS.split("```css")[1]
    css = css_without_bullshit_above.split("```")[0]
    return css


# Put Website in directory with html, css files + readme
def makeWebsiteDirectory(html, css=False):
    directory_name = "my_website"
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

    html_file_name = os.path.join(directory_name, "index.html")
    css_file_name = os.path.join(directory_name, "styles.css") if css else None
    readme_file_name = os.path.join(directory_name, "README.md")

    with open(html_file_name, "w") as html_file:
        html_file.write(html)

    if css:
        with open(css_file_name, "w") as css_file:
            css_file.write(css)

    readme_content = """
# How to Run the Application

Follow these steps to run the application:

1. Open the root directory in the terminal.
2. Use the following command to run the website: `npx serve` """

    with open(readme_file_name, 'w') as readme_file:
        readme_file.write(readme_content)

    print(
        f"Directory '{directory_name}' created successfully"
    )


def buildWebsite(image, option, mode="Separate"):
    print("Building website...")

    if option == "Image URL":
        r1 = chatbotImageURL(
            image_url=image, input="What is inside of this image?")
        r2 = chatbotImageURL(
            image_url=image, input=f"Generate code (HTML FULL CODE, CSS FULL CODE) for a website that looks EXACTLY PRECIESLY like the one in the image provided, make sure the code has no errors, make sure the code is EXACTLY identical, make sure the code is just like the image without any differences, repetitivity IS ACCEPTABLE, Make HTML, CSS code, {'MAKE SURE TO PROVIDE CSS SEPERATELY FROM THE HTML CODE' if mode == 'Seperate' else 'CSS STRAIGHT in <style > tag in the < head >'} , MAKE SURE CODE IS CORRECT WITHOUT ERRORS, REPLY WITH ONLY THE CODE, MAKE SURE CSS INCLUDES HOVER EFFECTS, LEAVE IMAGES' SRC ATTRIBUTES (if there are any images) AS PLACEHOLDERS, DON'T LEAVE ANY OTHER PLACEHOLDERS, INCLUDE ALL THE TEXT AND DON'T LEAVE OUT ANYTHING, MAKE AN EXACT VERSION OF THE WEBSITE IN THE IMAGE PROVIDED. MAKE SURE NONE OF THE  CODES (HTML OR CSS) IS MISSING, MAKE SURE TO PROVIDE CSS CODE, MAKE SURE THERE IS CSS CODE FOR EVERY SINGLE PART AND ELEMENT OF THE WEBSITE, MAKE SURE THERE IS CSS CODE FOR EVERY SINGLE PART AND ELEMENT OF THE WEBSITE!! NEVER LEAVE ANY ELEMENT WITHOUT STYLE!!, MAKE SURE THE WEBSITE DESIGN IS PERFECTLY IDENTICAL WITH THE IMAGE PROVIDED, MAKE SURE THE CODE IS FULL, NO MISSING PARTS ARE ACCEPTABLE, INCLUDE CSS FOR NAVIGATION BAR ON TOP OF THE WEBSITE IF THERE'S ONE IN THE IMAGE"
        )

    elif option == "Upload Image":
        r1 = chatbotImageFile(
            image_file=image, input="What is inside of this image?")
        r2 = chatbotImageFile(
            image_file=image, input=f"Generate code (HTML FULL CODE, CSS FULL CODE) for a website that looks EXACTLY PRECIESLY like the one in the image provided, make sure the code has no errors, make sure the code is EXACTLY identical, make sure the code is just like the image without any differences, repetitivity IS ACCEPTABLE, Make HTML, CSS code, {'MAKE SURE TO PROVIDE CSS SEPERATELY FROM THE HTML CODE' if mode == 'Seperate' else 'CSS STRAIGHT in <style > tag in the < head >'} , MAKE SURE CODE IS CORRECT WITHOUT ERRORS, REPLY WITH ONLY THE CODE, MAKE SURE CSS INCLUDES HOVER EFFECTS, LEAVE IMAGES' SRC ATTRIBUTES (if there are any images) AS PLACEHOLDERS, DON'T LEAVE ANY OTHER PLACEHOLDERS, INCLUDE ALL THE TEXT AND DON'T LEAVE OUT ANYTHING, MAKE AN EXACT VERSION OF THE WEBSITE IN THE IMAGE PROVIDED. MAKE SURE NONE OF THE  CODES (HTML OR CSS) IS MISSING, MAKE SURE TO PROVIDE CSS CODE, MAKE SURE THERE IS CSS CODE FOR EVERY SINGLE PART AND ELEMENT OF THE WEBSITE, MAKE SURE THERE IS CSS CODE FOR EVERY SINGLE PART AND ELEMENT OF THE WEBSITE!! NEVER LEAVE ANY ELEMENT WITHOUT STYLE!!, MAKE SURE THE WEBSITE DESIGN IS PERFECTLY IDENTICAL WITH THE IMAGE PROVIDED, MAKE SURE THE CODE IS FULL, NO MISSING PARTS ARE ACCEPTABLE, INCLUDE CSS FOR NAVIGATION BAR ON TOP OF THE WEBSITE IF THERE'S ONE IN THE IMAGE"
        )

    rawHTMLCSS = r2
    print(RED + "raw: " + RESET + rawHTMLCSS)

    html = extractHTMLFromResponse(rawHTMLCSS) if mode == "Seperate" else r2
    css = extractCSSFromResponse(rawHTMLCSS) if mode == "Seperate" else None

    print(MAGENTA + "index.html: " + RESET)
    print(html)
    if mode == "Seperate":
        print(YELLOW + "CSS: " + RESET)
        print(css)

    makeWebsiteDirectory(html, css if mode == "Seperate" else False)

    # Create a zip file containing the directory
    zip_file_name = "my_website.zip"
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk("my_website"):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, "my_website"))

    return zip_file_name

# https://colorlib.com/wp/wp-content/uploads/sites/2/table-03.jpg
