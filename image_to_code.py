from clarifai.client.model import Model
from clarifai.client.input import Inputs

import os
os.environ["CLARIFAI_PAT"] = "f3ac13477d814ca79bf0a1d01739e251" 


inference_params = dict(temperature=0.2, max_tokens=100)

conversation =""

def chatbot(input, image_url):
    global conversation
    conversation += "user: " + input + "\n\n"
    model_prediction = Model("https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision").predict(inputs = [Inputs.get_multimodal_input(input_id="",image_url=image_url, raw_text=conversation)],inference_params=inference_params)
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

image_url = "https://colorlib.com/wp/wp-content/uploads/sites/2/table-03.jpg"
r1 = chatbot(image_url = image_url, input = "What is inside of this image?")
r2  = chatbot(image_url = image_url, input = "write separate html and css code to make this")

rawHTMLCSS = r2
html = extractHTMLFromResponse(rawHTMLCSS)
css = extractCSSFromResponse(rawHTMLCSS)

# ANSI escape codes for text colors
# RED = "\033[91m"
# GREEN = "\033[92m"
# YELLOW = "\033[93m"
# BLUE = "\033[94m"
# MAGENTA = "\033[95m"
# CYAN = "\033[96m"
# RESET = "\033[0m"  # Reset color to default

# print(RED + "rawHTMLCSS: "  + RESET + rawHTMLCSS )



# print(MAGENTA  + "Html: "  + RESET)
# print(html)
# print(YELLOW  + "CSS: "  + RESET)
# print(css)


# Put Website in directory with html, css files
directory_name = "my_website"
if not os.path.exists(directory_name):
    os.mkdir(directory_name)

html_file_name = os.path.join(directory_name, "index.html")
css_file_name = os.path.join(directory_name, "styles.css")

with open(html_file_name, "w") as html_file:
    html_file.write(html)

with open(css_file_name, "w") as css_file:
    css_file.write(css)

print(f"Directory '{directory_name}' created with 'index.html' and 'style.css' files.")