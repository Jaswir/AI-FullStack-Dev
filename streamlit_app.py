import os
import streamlit as st
from streamlit_javascript import st_javascript
from PIL import Image

import image_to_code
import script_to_image


if "has_download" not in st.session_state:
    st.session_state.has_download = False

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


    option = st.radio("Select an option:", ("Image URL", "Upload Image", "Write Script"))

    if option == "Image URL":
        IMAGE_URL = st.text_input(
            "Enter the image URL to get started!",
            "https://static.semrush.com/blog/uploads/media/ed/9b/ed9b42a338de806621bdaf70293c2e7e/original.png",
        )
        if IMAGE_URL is not None:
            st.image(image_to_code.get_image_from_url(IMAGE_URL), width = 700)

    elif option == "Upload Image":
        IMAGE_FILE = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if IMAGE_FILE is not None:
            st.image(IMAGE_FILE, width = 700)
        
    elif option == "Write Script":

        script = st.text_area("Write your script here:", height=200)
        file_path = './generated_image.png'


        if st.button("Generate Image"):
            if not clarifai_pat:
                st.warning("Please enter your PAT to continue:", icon="⚠️")
            elif not script:
                st.warning("Please write a script to continue:", icon="⚠️")
            else:
                os.environ["CLARIFAI_PAT"] = clarifai_pat
                
                if option == "Write Script":
                    output_base64 = script_to_image.process_script(script)
                    with open(file_path, 'wb', encoding="utf8") as f:
                        f.write(output_base64)
                    st.success("Image generated successfully!")

        if os.path.exists(file_path):
            st.image(file_path, width= int(window_width / 5 * 3))
            st.download_button(
                label="Download Image",
                data=open(file_path,"rb").read(),
                key="download_image",
                file_name=file_path,
            )
             

    # Add a button to run the script
    llm = st.radio("LLM:", ("Gemini", "GPT-4"))

    if st.button("Build Website"):
        if not clarifai_pat:
            st.warning("Please enter your PAT to continue:", icon="⚠️")
        else:
            os.environ["CLARIFAI_PAT"] = clarifai_pat

            
            if option == "Image URL":
                image_to_code.buildWebsite(IMAGE_URL, option="Image URL", llm = llm)
                st.session_state.has_download = True
                
            elif option == "Upload Image":
                if IMAGE_FILE is not None:                
                    image_to_code.buildWebsite(IMAGE_FILE, option="Upload Image", llm = llm)
                    st.session_state.has_download = True
                else:
                    st.warning("Please upload an image to continue:", icon="⚠️")

            elif option == "Write Script":
                if os.path.exists(file_path):
                    image_to_code.buildWebsite(file_path, option="Write Script", llm = llm)
                    st.session_state.has_download = True
                else:
                    st.warning("Please generate an image to continue:", icon="⚠️")

                    
    # Provide a download link for the zip file
    # if st.session_state.has_download:
     

    file_path_html = "./my_website/index.html"
    file_path_css = "./my_website/styles.css"


    with open(file_path_html, "r", encoding="utf8") as file:
        html_string = file.read()

    with open(file_path_css, "r", encoding="utf8") as file:
        css_string = '<style>' + file.read() + '</style>'

    html_plus_css = html_string.replace('<link rel="stylesheet" href="styles.css">', css_string)

    st.components.v1.html(
        html_plus_css,
        width=window_width,
        height=window_width / 16 * 9,
    )

    st.subheader("Click the button below to get the code")
    st.download_button(
        label="Get Code",
        data=open("my_website.zip", "rb").read(),
        key="download_directory",
        file_name="my_website.zip",
    )


if __name__ == "__main__":
    main()
