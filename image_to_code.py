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

def extractHTMLFromResponse(rawHTMLCSS):
    # Extracts the part between ```html and ```
    html_without_bullshit_above = rawHTMLCSS.split("```html")[1]
    html = html_without_bullshit_above.split("```")[0]
    return html

def extractCSSFromResponse(rawHTMLCSS):
    # Extracts the part between ```css and ```
    css_without_bullshit_above = rawHTMLCSS.split("```css")[1]
    css = css_without_bullshit_above.split("```")[0]
    return css

image_url = "https://colorlib.com/wp/wp-content/uploads/sites/2/table-03.jpg"
r1 = chatbot(image_url = image_url, input = "What is inside of this image?")
r2  = chatbot(image_url = image_url, input = "write a html, css code to make this")

rawHTMLCSS = r2
html = extractHTMLFromResponse(rawHTMLCSS)
css = extractHTMLFromResponse(rawHTMLCSS)

print(html)
print(css)