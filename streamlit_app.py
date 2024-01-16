import os
import streamlit as st
import image_to_code

# JavaScript code to get the browser's window size
js_code = """
<script>
    const { innerWidth, innerHeight } = window;
    const dimensions = { width: innerWidth, height: innerHeight };
    Streamlit.setComponentValue(dimensions);
</script>
"""

if "has_download" not in st.session_state:
    st.session_state.has_download = False

st.set_page_config(layout="wide")

st.title("AI Website Builder")


def main():
    # Get the dimensions from the JavaScript and display them
    dimensions = st.experimental_get_query_params().get("dimensions", None)
    if dimensions:
        width = dimensions.get("width", "N/A")
        height = dimensions.get("height", "N/A")

        st.write(f"Browser Width: {width}px")
        st.write(f"Browser Height: {height}px")
    else:
        st.warning("Please refresh the page to get the browser dimensions.")
    # st.subheader("or")
    # IMAGE_FILE = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # st.subheader("Choose an option:")

    # Clarifai Credentials
    # with st.sidebar:
    #     st.subheader("Add your Clarifai PAT")
    #     clarifai_pat = st.text_input("Clarifai PAT:", type="password")

    # option = st.radio("Select an option:", ("Image URL", "Upload Image"))

    # if option == "Image URL":
    #     IMAGE_URL = st.text_input(
    #         "Enter the image URL to get started!",
    #         "https://colorlib.com/wp/wp-content/uploads/sites/2/table-03.jpg",
    #     )

    # elif option == "Upload Image":
    #     IMAGE_FILE = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # # Add a button to run the script
    # if st.button("Build Website"):
    #     if not clarifai_pat:
    #         st.warning("Please enter your PAT to continue:", icon="⚠️")
    #     else:
    #         os.environ["CLARIFAI_PAT"] = clarifai_pat

    #         if option == "Image URL":
    #             image_to_code.buildWebsite(IMAGE_URL, option="Image URL")
    #             st.session_state.has_download = True

    #         elif option == "Upload Image":
    #             if IMAGE_FILE is not None:
    #                 image_to_code.buildWebsite(IMAGE_FILE, option="Upload Image")
    #                 st.session_state.has_download = True
    #             else:
    #                 st.warning("Please upload an image to continue:", icon="⚠️")

    # # Provide a download link for the zip file
    # if st.session_state.has_download:
    #     st.subheader("Click the button below to download the website as a zip file:")
    #     st.download_button(
    #         label="Download Website",
    #         data=open("my_website.zip", "rb").read(),
    #         key="download_directory",
    #         file_name="my_website.zip",
    #     )

#     st.components.v1.html(
#         """<!DOCTYPE html>
# <html lang="en">
# <head>
# <meta charset="UTF-8">
# <meta name="viewport" content="width=device-width, initial-scale=1.0">
# <title>Domain Registration Table</title>
# <link rel="stylesheet" href="styles.css">
# </head>
# <body>
# <div class="container">
#     <h1>Table #03</h1>
#     <h2>Create Your Domain Name</h2>
#     <table>
#         <thead>
#             <tr>
#                 <th>TLD</th>
#                 <th>Duration</th>
#                 <th>Registration</th>
#                 <th>Renewal</th>
#                 <th>Transfer</th>
#                 <th></th>
#             </tr>
#         </thead>
#         <tbody>
#             <tr>
#                 <td>.com</td>
#                 <td>1 Year</td>
#                 <td>$12.99</td> 
#                 <td>$8.99</td>
#                 <td>$8.99</td>
#                 <td><button>Register Now</button></td>
#             </tr>
#             <!-- Repeat rows for each domain type -->
#         </tbody>
#     </table>
# </div>
# </body>

# </html>
# <style>

# body {
#     font-family: Arial, sans-serif;
#     padding: 20px;
#     background-color: #f4f4f4;
# }

# .container {
#     max-width: 800px;
#     margin: auto;
#     background: white;
#     padding: 20px;
#     box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
# }

# h1, h2 {
#     text-align: center;
# }

# table {
#     width: 100%;
#     border-collapse: collapse;
#     margin-top: 20px;
# }

# thead {
#     background-color: #6a1b9a;
#     color: white;
# }

# th, td {
#     text-align: left;
#     padding: 10px;
#     border-bottom: 1px solid #ddd;
# }

# button {
#     background-color: #6a1b9a;
#     color: white;
#     border: none;
#     padding: 5px 10px;
#     text-align: center;
#     text-decoration: none;
#     display: inline-block;
#     font-size: 16px;
#     margin: 4px 2px;
#     cursor: pointer;
#     border-radius: 4px;
# }

# button:hover {
#     background-color: #5c007a;
# }

# </style>

# """,
#         width=850,
#         height=618,
#     )


if __name__ == "__main__":
    main()
