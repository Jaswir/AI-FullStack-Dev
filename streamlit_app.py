import os
import streamlit as st
import image_to_code

st.set_page_config(layout="wide")

# This must be within the display() function.
# auth = ClarifaiAuthHelper.from_streamlit(st)
# stub = create_stub(auth)
# userDataObject = auth.get_user_app_id_proto()


st.title("AI Full Stack Dev")


def main():
    IMAGE_URL = st.text_input("Enter the image URL to get started!")

    # Clarifai Credentials
    with st.sidebar:
        st.subheader("Add your Clarifai PAT")
        clarifai_pat = st.text_input("Clarifai PAT:", type="password")

    if not clarifai_pat:
        st.warning("Please enter your PAT to continue:", icon="⚠️")
    else:
        os.environ["CLARIFAI_API_KEY"] = clarifai_pat

        # Add a button to run the script
        if st.button("Build Website"):
            image_to_code.buildWebsite(IMAGE_URL)


if __name__ == "__main__":
    main()
