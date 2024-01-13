import os
import streamlit as st
import image_to_code

st.set_page_config(layout="wide")

st.title("AI Website Builder")


def main():


    # st.subheader("or")
    # IMAGE_FILE = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # st.subheader("Choose an option:")

    # Clarifai Credentials
    with st.sidebar:
        st.subheader("Add your Clarifai PAT")
        clarifai_pat = st.text_input("Clarifai PAT:", type="password")

    option = st.radio("Select an option:", ("Image URL", "Upload Image"))

    if option == "Image URL":
        IMAGE_URL = st.text_input(
            "Enter the image URL to get started!",
            "https://colorlib.com/wp/wp-content/uploads/sites/2/table-03.jpg",
        )
        
    elif option == "Upload Image":
        IMAGE_FILE = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # Add a button to run the script
    if st.button("Build Website"):

        if not clarifai_pat:
            st.warning("Please enter your PAT to continue:", icon="⚠️")
        else:
            os.environ["CLARIFAI_PAT"] = clarifai_pat

            if option == "Image URL":
                image_to_code.buildWebsite(IMAGE_URL, option = "Image URL")
            elif option == "Upload Image":
                if IMAGE_FILE is not None:
                    image_to_code.buildWebsite(IMAGE_FILE, option = "Upload Image")

                else:
                    st.warning("Please upload an image to continue:", icon="⚠️")

     

 

   
          

    


if __name__ == "__main__":
    main()
