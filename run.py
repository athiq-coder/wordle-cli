
from server import resize_route
import streamlit as st
import pydaisi as pyd
import numpy as np
from PIL import Image
import cv2
from io import BytesIO
import base64
import uuid
import re

@st.cache
def download_button(object_to_download, download_filename, button_text, isPNG):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    Examples:
    --------
    download_link(Pillow_image_from_cv_matrix, 'your_image.jpg', 'Click to me to download!')
    """

    buffered = BytesIO()
    if isPNG:
        object_to_download.save(buffered, format="PNG")
    else:
        object_to_download.save(buffered, format="JPEG")
    b64 = base64.b64encode(buffered.getvalue()).decode()

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: .25rem .75rem;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'
    return dl_link

    
def run():
    st.set_page_config(layout = "wide")
    st.title("Upload and Download!")
    image_file_buffer = st.file_uploader("Upload your image", type=["jpg", "jpeg", 'png'])
    size = st.text_input('Size', '300x300')

    if image_file_buffer is not None:
        new_image = resize_route(size, image_file_buffer)
        image = np.array(Image.open(new_image))

        st.image(
            image, caption=f"Original Image", use_column_width=True
        )

        if image.shape[2] > 3:
            isPNG = True
            output_extension = ".png"
        else:
            isPNG = False
            output_extension = ".jpg"

        result = Image.fromarray(image)
        st.markdown(download_button(result,f"your_output_file{output_extension}", "Click me to download!!!", isPNG), unsafe_allow_html=True)


if __name__ == "__main__":
    run()