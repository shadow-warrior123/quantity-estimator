import os
from PIL import Image
import customtkinter

def setup_images():
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
    logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(30, 30))
    return logo_image