import zipfile
import os
import requests
from io import BytesIO
import re

import ai_secret_sauce
import image_feedback
import html_image_filler


# ANSI escape codes for text colors when using print()
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"  # Reset color to default


# Extracts the part between ```html and ``` from raw chat gpt response
def extractHTMLFromResponse(rawHTMLCSS):
    if "```html" not in rawHTMLCSS:
        return getHTMLCode()

    html_without_bullshit_above = rawHTMLCSS.split("<!DOCTYPE html>")[1]
    html = html_without_bullshit_above.split("</html>")[0]
    html = "<!DOCTYPE html>" + html + "</html>"
    return html


# Extracts the part between ```css and ``` from raw chat gpt response
def extractCSSFromResponse(rawHTMLCSS):
    if "```css" not in rawHTMLCSS:
        return getCSSCode()

    css_without_bullshit_above = rawHTMLCSS.split("```css")[1]
    css = css_without_bullshit_above.split("```")[0]
    return css


def addCSSToHtml(html):
    with open("./my_website/styles.css", "r", encoding="utf8") as file:
        css_string = "<style>" + file.read() + "</style>"

    html_plus_css = html.replace(
        '<link rel="stylesheet" href="styles.css">', css_string
    )

    return html_plus_css


# Put Website in directory with html, css files + readme
def writeCodeToWebsiteDirectory(html, css):
    directory_name = "my_website"
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

    html_file_name = os.path.join(directory_name, "index.html")
    css_file_name = os.path.join(directory_name, "styles.css")
    readme_file_name = os.path.join(directory_name, "README.md")

    with open(html_file_name, "w", encoding="utf-8") as html_file:
        html_file.write(html)

    if css != "":
        with open(css_file_name, "w", encoding="utf-8") as css_file:
            css_file.write(css)

    readme_content = """
# How to Run the Application

Follow these steps to run the application:

1. Open the root directory in the terminal.
2. Use the following command to run the website: `npx serve` """

    with open(readme_file_name, "w", encoding="utf8") as readme_file:
        readme_file.write(readme_content)

    print(
        f"Directory '{directory_name}' created with 'index.html' and 'style.css' files."
    )


def updateCodeFiles(response):
    print(RED + "raw response: " + RESET + response)

    # Update html and css
    html = extractHTMLFromResponse(response)
    css = extractCSSFromResponse(response)
    writeCodeToWebsiteDirectory(html, css)


def zipCodeFiles():
    # Create a zip file containing the directory
    zip_file_name = "my_website.zip"
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk("my_website"):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, "my_website"))

    return zip_file_name


def getCode():
    file_path_html = "./my_website/index.html"
    file_path_css = "./my_website/styles.css"

    with open(file_path_html, "r", encoding="utf8") as file:
        html_string = file.read()

    with open(file_path_css, "r", encoding="utf8") as file:
        css_string = "<style>" + file.read() + "</style>"

    html_plus_css = re.sub(r"<link.*?css.*?>", css_string, html_string)
    return html_plus_css


def getHTMLCode():
    file_path_html = "./my_website/index.html"
    if os.path.exists(file_path_html):
        with open(file_path_html, "r", encoding="utf8") as file:
            html_string = file.read()
        return html_string
    return ""


def getCSSCode():
    file_path_css = "./my_website/styles.css"
    if os.path.exists(file_path_css):
        with open(file_path_css, "r", encoding="utf8") as file:
            css_string = file.read()
        return css_string
    return ""


# Helper function for displaying image from url in streamlit
def get_image_from_url(image_url):
    r = requests.get(image_url)
    return r.content


prompt = """Generate code (HTML FULL CODE, CSS FULL CODE) 
for a website that looks EXACTLY like the one in the image provided, 
, make sure the stylesheet is called 
styles.css, Make HTML, CSS code, and make sure to put the code inside 
```html and ```css tags MAKE SURE CSS INCLUDES HOVER EFFECTS, LEAVE IMAGES' SRC ATTRIBUTES (if there are any images) AS PLACEHOLDERS, DON'T LEAVE ANY OTHER PLACEHOLDERS, INCLUDE ALL THE TEXT AND DON'T LEAVE OUT ANYTHING, MAKE AN EXACT VERSION OF THE WEBSITE IN THE IMAGE PROVIDED. MAKE SURE NONE OF THE  CODES (HTML OR CSS) IS MISSING, MAKE SURE TO PROVIDE CSS CODE, MAKE SURE THERE IS CSS CODE FOR EVERY SINGLE PART AND ELEMENT OF THE WEBSITE, NEVER LEAVE ANY ELEMENT WITHOUT STYLE!!, MAKE SURE THE WEBSITE DESIGN IS PERFECTLY IDENTICAL WITH THE IMAGE PROVIDED, MAKE SURE THE CODE IS FULL,, INCLUDE CSS FOR NAVIGATION BAR ON TOP OF THE WEBSITE IF THERE'S ONE IN THE IMAGE"""

prompt2 = "write separate html and css code to make this given the desciption"

prompt3 = """Describe the elements in this image, the positioning, give me all the texts for the elements, and the colours of each element,
if there's a table provide me all the data that it contains in a json"""


prompt0 = "write separate html and css code to make this"

fill_data_prompt = """does the image contain a table? If so, put all of the data 
    inside of this table inside of the following html code, give back 
    full html code inside ```html tag:"""

gemini_just_improve = """improve this code give back 
    full html code inside ```html tag:"""

prompt5 = "improve this code return complete html and css code no placeholders"


def buildWebsite(image, option, llm):
    print("Building website...")
    print("Option: " + option)
    print("LLM: " + llm)

    if llm == "GPT-4":
        response = ai_secret_sauce.getGPT4VisionResponse(image, prompt0, option)
        updateCodeFiles(response)

        # Input data inside of the tables correctly.
        # has_table_string = ai_secret_sauce.getGeminiVisionResponse(
        #     image, "does the image contain a table?", option
        # )
        # has_table = not "No" in has_table_string or True

        # print("Processing layer to fill in data:", has_table)

        # if True:
        #     data_filled_in = ai_secret_sauce.getGeminiVisionResponse(
        #         image, gemini_just_improve + response, option
        #     )

        #     updateCodeFiles(data_filled_in)

        feedback = image_feedback.letGPT4EvaluateAndImproveItsWork()
        updateCodeFiles(feedback)

        html_image_filler.fillHTMLImages(getHTMLCode())
      

    elif llm == "Gemini":
        geminiResponse = ai_secret_sauce.getGeminiVisionResponse(image, prompt, option)
        updateCodeFiles(geminiResponse)
        response = ai_secret_sauce.getGPT4VisionResponse(
            image, prompt5 + geminiResponse, option
        )

        updateCodeFiles(response)

    zipCodeFiles()


def improveWebsite(prompt):
    print("Improving website...")

    # Get current code
    file_path_html = "./my_website/index.html"
    file_path_css = "./my_website/styles.css"

    with open(file_path_html, "r", encoding="utf8") as file:
        html_string = file.read()

    with open(file_path_css, "r", encoding="utf8") as file:
        css_string = "<style>" + file.read() + "</style>"

    code = html_string.replace('<link rel="stylesheet" href="styles.css">', css_string)

    input = prompt + """, improve this code: """ + code
    response = ai_secret_sauce.getGeminiResponse(input)

    updateCodeFiles(response)
    zipCodeFiles()

    return
