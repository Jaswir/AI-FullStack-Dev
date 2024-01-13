import streamlit as st

import image_to_code

# Define a Streamlit app
def main():
    st.title("Run Python Script with Button")

    # Add a button to run the script
    if st.button("Build Website"):
        # Execute your Python script when the button is pressed
        run_script()

# Define the function to run your Python script
def run_script():
    try:
        # Replace 'your_script.py' with the actual filename of your Python script
        script_filename = 'image_to_code.py'

        # Run the script using subprocess
        result = subprocess.run(['python', script_filename], capture_output=True, text=True)

        # Display the script output in the Streamlit app
        st.code(result.stdout, language='python')

    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

