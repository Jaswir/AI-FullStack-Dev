import streamlit as st
import os
from pathlib import Path

import google.generativeai as genai
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from clarifai.client.model import Model
from clarifai.client.input import Inputs

import image_to_code

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]


inference_params = dict(temperature=0.2, max_tokens=250)
conversation = ""


def getGPT4Response(image, prompt, option):
    if option == "Image URL":
        r1 = chatbotImageURL(image_url=image, input="What is inside of this image?")
        print("r1: " + r1)
        r2 = chatbotImageURL(image_url=image, input=prompt)

    elif option == "Upload Image":
        r1 = chatbotImageFile(image_file=image, input="What is inside of this image?")
        print("r1: " + r1)
        r2 = chatbotImageFile(image_file=image, input=prompt)

    elif option == "Write Script":
        r1 = chatbotImageFromFilePath(
            file_path=image, input="What is inside of this image?"
        )
        print("r1: " + r1)
        r2 = chatbotImageFromFilePath(file_path=image, input=prompt)

    return r2

def getGeminiVisionResponse(image, prompt, option):

    if option == "Image URL":
        r1 = getGeminiVisionResponseImageURL(image_url=image, input=prompt)

    elif option == "Upload Image":
        image_file_path = os.path.join("tmpDirUploadedImage", image.name)
        r1 = getGeminiVisionResponseImageFile(image_path=image_file_path, input=prompt)

    elif option == "Write Script":
        r1 = getGeminiVisionResponseImageFile(image_path=image, input=prompt)

    return r1

def chatbotImageFromFilePath(input, file_path):
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


def chatbotImageFile(input, image_file):
    # Temporarily saves the file to directory and read in as bytes
    uploaded_file = image_file
    file_path = os.path.join("tmpDirUploadedImage", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return chatbotImageFromFilePath(input, file_path)


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

def getGeminiVisionResponseImageFile(input, image_path):
    genai.configure(api_key=GOOGLE_API_KEY)

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


def getGeminiVisionResponseImageURL(image_url, input):
    genai.configure(api_key=GOOGLE_API_KEY)

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": input,
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
