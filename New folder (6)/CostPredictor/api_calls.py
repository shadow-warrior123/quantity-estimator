import requests


def get_unit_price(material_name):
    url = f"https://api.example.com/materials/{material_name}/price"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['unit_price']
    else:
        return None
