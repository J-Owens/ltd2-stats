import requests
from io import BytesIO
from PIL import Image

def get_unit_icon_url(unit_id):
    if unit_id is 'hell_raiser_buffed':
        unit_id = 'hell_raiser'
    unit_name = ''.join(word.capitalize() for word in unit_id.split('_'))
    return f"https://cdn.legiontd2.com/icons/{unit_name}.png"

def get_unit_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img