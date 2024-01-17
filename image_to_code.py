import zipfile
import os
import gpt_4_vision
import gemini_pro_vision

# ANSI escape codes for text colors when using print()
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"  # Reset color to default

prompt = """Generate code (HTML FULL CODE, CSS FULL CODE) 
for a website that looks EXACTLY like the one in the image provided, 
, make sure the stylesheet is called 
styles.css, Make HTML, CSS code, and make sure to put the code inside 
```html and ```css tags MAKE SURE CSS INCLUDES HOVER EFFECTS, LEAVE IMAGES' SRC ATTRIBUTES (if there are any images) AS PLACEHOLDERS, DON'T LEAVE ANY OTHER PLACEHOLDERS, INCLUDE ALL THE TEXT AND DON'T LEAVE OUT ANYTHING, MAKE AN EXACT VERSION OF THE WEBSITE IN THE IMAGE PROVIDED. MAKE SURE NONE OF THE  CODES (HTML OR CSS) IS MISSING, MAKE SURE TO PROVIDE CSS CODE, MAKE SURE THERE IS CSS CODE FOR EVERY SINGLE PART AND ELEMENT OF THE WEBSITE, NEVER LEAVE ANY ELEMENT WITHOUT STYLE!!, MAKE SURE THE WEBSITE DESIGN IS PERFECTLY IDENTICAL WITH THE IMAGE PROVIDED, MAKE SURE THE CODE IS FULL,, INCLUDE CSS FOR NAVIGATION BAR ON TOP OF THE WEBSITE IF THERE'S ONE IN THE IMAGE"""

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

def addCSSToHtml(html):
    with open("./my_website/styles.css", "r") as file:
        css_string = "<style>" + file.read() + "</style>"

    html_plus_css = html.replace(
        '<link rel="stylesheet" href="styles.css">', css_string
    )

    return html_plus_css

# Put Website in directory with html, css files + readme
def makeWebsiteDirectory(html, css):
    directory_name = "my_website"
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

    html_file_name = os.path.join(directory_name, "index.html")
    css_file_name = os.path.join(directory_name, "styles.css")
    readme_file_name = os.path.join(directory_name, "README.md")

    with open(html_file_name, "w") as html_file:
        html_file.write(html)

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
        f"Directory '{directory_name}' created with 'index.html' and 'style.css' files."
    )


def buildWebsite(image, option):
    print("Building website...")
    print("Option: " + option)

    if option == "Image URL":
        r2 = gemini_pro_vision.getGeminiProResponse(image_url=image, input=prompt)

    elif option == "Upload Image":
        r1 = gpt_4_vision.chatbotImageFile(image_file=image, input="What is inside of this image?")
        r2 = gpt_4_vision.chatbotImageFile(
            image_file=image, input="write separate html and css code to make this"
        )

    elif option == "Write Script":
        r1 = gpt_4_vision.chatbotImageFromFilePath(file_path=image, input="What is inside of this image?")
        r2 = gpt_4_vision.chatbotImageFromFilePath(
            file_path=image, input="write separate html and css code to make this"
        )

    rawHTMLCSS = r2
    print(RED + "rawHTMLCSS: " + RESET + rawHTMLCSS)

    html = extractHTMLFromResponse(rawHTMLCSS)
    css = extractCSSFromResponse(rawHTMLCSS)

    print(MAGENTA + "Html: " + RESET)
    print(html)
    print(YELLOW + "CSS: " + RESET)
    print(css)

    makeWebsiteDirectory(html, css)

    # Create a zip file containing the directory
    zip_file_name = "my_website.zip"
    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk("my_website"):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, "my_website"))

    return zip_file_name


# https://colorlib.com/wp/wp-content/uploads/sites/2/table-03.jpg