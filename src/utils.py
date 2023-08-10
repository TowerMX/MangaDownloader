from pathlib import Path
from PIL import Image
import shutil
import os
from . import const


def delete_files(manga_name, folder):
    shutil.rmtree(rf"{folder}\{manga_name}", ignore_errors=True)


def convert_to_pdf(manga_name, temp_folder=const.DEFAULT_TEMP_FOLDER, save_folder=const.DEFAULT_SAVE_FOLDER):
    try:
        # Crea carpeta del manga
        Path(rf"{save_folder}\{manga_name}").mkdir(exist_ok=True)
        for volume in os.scandir(rf"{temp_folder}\{manga_name}"):
            if not volume.is_dir():
                continue
            if volume.name == "Oneshot":
                images_folder = rf"{temp_folder}\{manga_name}\{volume.name}"
                pdf_path = rf"{save_folder}\{manga_name}\{volume.name}.pdf"
                _images_to_pdf(images_folder, pdf_path)
            elif volume.name == "No volumes":
                for chapter in os.scandir(rf"{temp_folder}\{manga_name}\{volume.name}"):
                    if not chapter.is_dir():
                        continue
                    images_folder = rf"{temp_folder}\{manga_name}\{volume.name}\{chapter.name}"
                    pdf_path = rf"{save_folder}\{manga_name}\{chapter.name}.pdf"
                    _images_to_pdf(images_folder, pdf_path)
            else:
                for chapter in os.scandir(rf"{temp_folder}\{manga_name}\{volume.name}"):
                    if not chapter.is_dir():
                        continue
                    images_folder = rf"{temp_folder}\{manga_name}\{volume.name}\{chapter.name}"
                    pdf_path = rf"{save_folder}\{manga_name}\{volume.name}, {chapter.name}.pdf"
                    _images_to_pdf(images_folder, pdf_path)
        return True
    except Exception:
        return False


def _images_to_pdf(images_folder, pdf_path):
    images = {}
    for page in os.scandir(images_folder):
        if page.is_dir():
            continue
        # Se convierte a RGB, el tamaño final se reduce en 10 veces
        images[int(page.name.split(".")[0])] = Image.open(page.path).convert('RGB')
    sorted_images = sorted(images.items())
    image_list = [image_tuple[1] for image_tuple in sorted_images]
    if len(image_list) > 1:
        image_list[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True, append_images=image_list[1:]
        )
    elif len(image_list) > 0:
        image_list[0].save(
            pdf_path, "PDF", resolution=100.0
        )


def create_default_config_file():
    with open(const.DEFAULT_CONFIG_FILE, "w") as f:
        f.write(
            '''language: "es"
login: false
delete_images: true
temp_path:
save_path:'''
        )


def create_default_credentials_file():
    with open(const.DEFAULT_CREDENTIALS_FILE, "w") as f:
        f.write(
            '''username:
password:'''
        )


def create_default_mangalist_file():
    with open(const.DEFAULT_MANGALIST_FILE, "w") as f:
        f.write(
            '''- name:
  url:
  first_chapter: "first"
  last_chapter: "last"
- name:
  url:
  first_chapter: "first"
  last_chapter: "last"'''
        )