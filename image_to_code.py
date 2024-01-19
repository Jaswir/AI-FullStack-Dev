import zipfile
import os
import requests
from io import BytesIO

import ai_secret_sauce


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
    html_without_bullshit_above = rawHTMLCSS.split("```html")[1]
    html = html_without_bullshit_above.split("```")[0]
    return html


# Extracts the part between ```css and ``` from raw chat gpt response
def extractCSSFromResponse(rawHTMLCSS):
    if "```css" not in rawHTMLCSS:
        return ""

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


# https://colorlib.com/wp/wp-content/uploads/sites/2/table-03.jpg


# Helper function for displaying image from url in streamlit
def get_image_from_url(image_url):
    r = requests.get(image_url)
    return BytesIO(r.content)


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


def buildWebsite(image, option, llm):
    print("Building website...")
    print("Option: " + option)
    print("LLM: " + llm)

    if llm == "GPT-4":
        response = ai_secret_sauce.getGPT4Response(image, prompt0, option)
        updateCodeFiles(response)

        # Input data inside of the tables correctly.

        has_table_string = ai_secret_sauce.getGeminiVisionResponse(
            image, "does the image contain a table?", option
        )
        has_table = not "No" in has_table_string

        print("Processing layer to fill in data:" , has_table)

        if has_table:
            data_filled_in = ai_secret_sauce.getGeminiVisionResponse(
                image, fill_data_prompt + response, option
            )

            updateCodeFiles(data_filled_in)

    elif llm == "Gemini":
        geminiResponse = ai_secret_sauce.getGeminiVisionResponse(image, prompt, option)

        # print(BLUE + "Gemini response: " + RESET + geminiResponse)

        # geminiResponse2 = ai_secret_sauce.getGeminiVisionResponse(
        #     image=None, input=prompt2, option=option
        # )
        response = geminiResponse
        updateCodeFiles(response)

    zipCodeFiles()


# geminiResponse = ai_secret_sauce.getGeminiVisionResponse(image, prompt, option)
# print(BLUE + "Gemini response: " + RESET + geminiResponse)

# colorfixed = ai_secret_sauce.chatbotImageURL(
#     image_url=image,
#     input="""fix the colors of the website to match colours in the image
#     return the fixed html and css code for the website"""
#     + geminiResponse,
# )

# response = colorfixed
