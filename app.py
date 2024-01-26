# For Clarifai UI Module (it requires having app.py)

import os
import streamlit as st
from streamlit_javascript import st_javascript
from PIL import Image
import re
from io import BytesIO

import image_to_code
import script_to_image

import streamlit as st


# code = """
# <!DOCTYPE html>

# <html lang="en">
# <head>
# <meta charset="utf-8"/>
# <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
# <title>Image Descriptions</title>
# </head>
# <body>
# <h1>Image Gallery</h1>
# <img alt="A cute cat playing with a ball of yarn" src="/app/static/cat.jpg"/>
# <img alt="A beautiful landscape with mountains and a lake" src="/app/static/landscape.jpg"/>
# <img alt="A person coding on a laptop with lines of code on the screen" src="/app/static/coding.jpg"/>
# <img alt="Delicious food spread with a variety of dishes" src="/app/static/food.jpg"/>
# <img alt="Adventurous travel scene with a backpack and hiking gear" src="/app/static/travel.jpg"/>
# <p>Explore the images above for a delightful experience!</p>
# </body>
# </html>
# """


# st.components.v1.html(
#     code,
#     width=1920,
#     height=1920 / 16 * 9,
# )

if "has_download" not in st.session_state:
    st.session_state.has_download = False

if "improved" not in st.session_state:
    st.session_state.improved = False

st.set_page_config(layout="wide")

st.title("AI Website Builder")


def main():
    # Javascript variables
    window_width = st_javascript("window.innerWidth")
    hostname = st_javascript("window.location.hostname")

    # Set Clarify PAT from secrets
    clarifai_pat = st.secrets["CLARIFAI_PAT"]

    # Clarifai Credentials
    # with st.sidebar:
    #     st.subheader("Add your Clarifai PAT")
    #     clarifai_pat = st.text_input("Clarifai PAT:", type="password")

    option = st.radio(
        "Select an option:", ("Image URL", "Upload Image", "Write Script")
    )

    if option == "Image URL":
        IMAGE_URL = st.text_input(
            "Enter the image URL to get started!",
            "https://static.semrush.com/blog/uploads/media/ed/9b/ed9b42a338de806621bdaf70293c2e7e/original.png",
        )
        if IMAGE_URL is not None:
            st.image(BytesIO(image_to_code.get_image_from_url(IMAGE_URL)), width=700)

    elif option == "Upload Image":
        IMAGE_FILE = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if IMAGE_FILE is not None:
            st.image(IMAGE_FILE, width=700)

    elif option == "Write Script":
        script = st.text_area("Write your script here:", height=200)
        file_path = "./generated_image.png"

        if st.button("Generate Image"):
            if not clarifai_pat:
                st.warning("Please enter your PAT to continue:", icon="⚠️")
            elif not script:
                st.warning("Please write a script to continue:", icon="⚠️")
            else:
                os.environ["CLARIFAI_PAT"] = clarifai_pat

                if option == "Write Script":
                    output_base64 = script_to_image.process_script(script)
                    with open(file_path, "wb") as f:
                        f.write(output_base64)
                    st.success("Image generated successfully!")

        if os.path.exists(file_path):
            st.image(file_path, width=int(window_width / 5 * 3))
            st.download_button(
                label="Download Image",
                data=open(file_path, "rb").read(),
                key="download_image",
                file_name=file_path,
            )

    # Developer options
    llm = st.radio("LLM:", ("GPT-4", "Gemini"))

    if st.button("Build Website"):
        if not clarifai_pat:
            st.warning("Please enter your PAT to continue:", icon="⚠️")
        else:
            os.environ["CLARIFAI_PAT"] = clarifai_pat

            if option == "Image URL":
                image_to_code.buildWebsite(IMAGE_URL, option="Image URL", llm=llm)
                st.session_state.has_download = True

            elif option == "Upload Image":
                if IMAGE_FILE is not None:
                    image_to_code.buildWebsite(
                        IMAGE_FILE, option="Upload Image", llm=llm
                    )
                    st.session_state.has_download = True
                else:
                    st.warning("Please upload an image to continue:", icon="⚠️")

            elif option == "Write Script":
                if os.path.exists(file_path):
                    image_to_code.buildWebsite(
                        file_path, option="Write Script", llm=llm
                    )
                    st.session_state.has_download = True
                else:
                    st.warning("Please generate an image to continue:", icon="⚠️")

    file_path_html = "./my_website/index.html"
    file_path_css = "./my_website/styles.css"

    if os.path.exists(file_path_html) and os.path.exists(file_path_css):
        with open(file_path_html, "r", encoding="utf8") as file:
            html_string = file.read()
        with open(file_path_css, "r", encoding="utf8") as file:
            css_string = "<style>" + file.read() + "</style>"

        html_plus_css = re.sub(r"<link.*?css.*?>", css_string, html_string)

        st.components.v1.html(
            html_plus_css,
            width=window_width,
            height=window_width / 16 * 9,
        )

        user_feedback = st.text_area(
            label="Improve website:",
            label_visibility="hidden",
            placeholder="insert website improvements",
            height=200,
        )

        if st.button("Improve Website"):
            if user_feedback:
                image_to_code.improveWebsite(user_feedback)
                st.warning("Website improved successfully! Refresh page to see the result", icon="🎉")

            else:
                st.warning("No text inserted", icon="⚠️")


    st.subheader("Click the button below to get the code")
    st.download_button(
        label="Get Code",
        data=open("my_website.zip", "rb").read(),
        key="download_directory",
        file_name="my_website.zip",
    )

if __name__ == "__main__":
    main()
