from pathlib import Path
import google.generativeai as genai
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai.client.model import Model
from clarifai.client.input import Inputs
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

import image_to_code

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

inference_params = dict(temperature=0.4, max_tokens=4096)


def getResponseFromGPT4(input, pat):
    PAT = pat
    USER_ID = "openai"
    APP_ID = "chat-completion"
    MODEL_ID = "GPT-4"
    MODEL_VERSION_ID = "5d7a50b44aec4a01a9c492c5a5fcf387"
    RAW_TEXT = "I love your product very much"

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (("authorization", "Key " + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(text=resources_pb2.Text(raw=RAW_TEXT))
                )
            ],
        ),
        metadata=metadata,
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception(
            f"Post model outputs failed, status: {post_model_outputs_response.status.description}"
        )

    output = post_model_outputs_response.outputs[0]

    return output.data.text.raw


def getGeminiVisionResponseImageFile(key, input, image_path):
    genai.configure(api_key=key)

    generation_config = {
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 4096,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-pro-vision",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    if not (img := Path(image_path)).exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [
        {"mime_type": "image/jpeg", "data": Path(image_path).read_bytes()},
    ]

    prompt_parts = [
        f"{input}\n",
        image_parts[0],
    ]

    response = model.generate_content(prompt_parts)
    return response.text


def getGeminiVisionResponseImageURL(key, image_url, prompt):
    genai.configure(api_key = key)

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": prompt,
            },  # You can optionally provide text parts
            {
                "type": "image_url",
                "image_url": image_url,
            },
        ]
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro-vision", temperature=0.4, max_output_tokens=4096
    )
    print("Generating response...")
    response = llm.invoke([message])

    text = str(response)
    text = text.split("content='")[1]
    text = text.encode().decode("unicode_escape")

    return text


prompt = """Generate code (HTML FULL CODE, CSS FULL CODE) 
for a website that looks EXACTLY like the one in the image provided, 
, make sure the stylesheet is called 
styles.css, Make HTML, CSS code, and make sure to put the code inside 
```html and ```css tags MAKE SURE CSS INCLUDES HOVER EFFECTS, LEAVE IMAGES' SRC ATTRIBUTES (if there are any images) AS PLACEHOLDERS, DON'T LEAVE ANY OTHER PLACEHOLDERS, INCLUDE ALL THE TEXT AND DON'T LEAVE OUT ANYTHING, MAKE AN EXACT VERSION OF THE WEBSITE IN THE IMAGE PROVIDED. MAKE SURE NONE OF THE  CODES (HTML OR CSS) IS MISSING, MAKE SURE TO PROVIDE CSS CODE, MAKE SURE THERE IS CSS CODE FOR EVERY SINGLE PART AND ELEMENT OF THE WEBSITE, NEVER LEAVE ANY ELEMENT WITHOUT STYLE!!, MAKE SURE THE WEBSITE DESIGN IS PERFECTLY IDENTICAL WITH THE IMAGE PROVIDED, MAKE SURE THE CODE IS FULL,, INCLUDE CSS FOR NAVIGATION BAR ON TOP OF THE WEBSITE IF THERE'S ONE IN THE IMAGE"""
image_path = "./tmpDirUploadedImage/table-03.jpg"
image_url = "https://colorlib.com/wp/wp-content/uploads/sites/2/table-03.jpg"
res = getGeminiVisionResponseFileURL(GOOGLE_API_KEY, image_url, prompt)
image_to_code.responseToCodeFiles(res)
