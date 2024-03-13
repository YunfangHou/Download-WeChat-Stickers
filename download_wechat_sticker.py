# Download WeChat stickers. Only tested on macOS.

import xml.etree.ElementTree as ET
import requests
import os
import subprocess


def convert_to_xml(file_name):
    command = ['plutil', '-convert', 'xml1', file_name]

    result = subprocess.run(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print("success")
    else:
        print("fail")


def check_content_type(content):
    png_magic = b'\x89PNG\r\n\x1a\n'
    gif_magic_89a = b'GIF89a'
    gif_magic_87a = b'GIF87a'

    if content.startswith(png_magic):
        return ".png"
    elif content.startswith(gif_magic_89a) or content.startswith(gif_magic_87a):
        return ".gif"
    else:
        return ".png" # fallback to .png


def download_images_from_xml(xml_file, download_folder):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    image_ctr = 0
    for string_element in root.iter('string'):
        url = string_element.text
        if url.startswith('http'):
            try:
                response = requests.get(url)
                content = response.content
                if response.status_code == 200:
                    image_ctr += 1
                    image_name = str(image_ctr) + check_content_type(content)
                    image_path = os.path.join(download_folder, image_name)
                    with open(image_path, 'wb') as file:
                        file.write(content)
                    print(f"Downloaded {image_name}")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading {url}: {e}")


convert_to_xml('fav.archive.plist')
download_images_from_xml('fav.archive.plist', 'stickers')
