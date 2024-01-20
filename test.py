from html2image import Html2Image


def htmlToPNG():
    hti = Html2Image(output_path="./image_feedback")
    file_path_html = "./my_website/index.html"
    hti.screenshot(html_file=file_path_html, save_as="output.png")

