import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_unit_prices(state):
    state = state.strip().replace(" ", "-")
    url = f'https://property.todaypricerates.com/{state}-construction-building-materials-rate'

    response = requests.get(url)
    if response.status_code == 200:
        web_content = response.content
        soup = BeautifulSoup(web_content, 'html.parser')

        data = []
        categories = soup.find_all('h2')

        for category in categories:
            category_name = category.get_text(strip=True)
            table = category.find_next('table')
            if table:
                headers = [header.get_text(strip=True) for header in table.find_all('th')]
                for row in table.find_all('tr'):
                    cells = row.find_all('td')
                    cells_text = [cell.get_text(strip=True) for cell in cells]
                    if cells_text:
                        data.append([category_name] + cells_text)

        columns = ['Category', 'Item', 'Unit', 'Minimum Rate', 'Average Cost', 'Max. Price']
        df = pd.DataFrame(data, columns=columns)

        excel_file = f'{state}_construction_material_rates.xlsx'
        df.to_excel(excel_file, index=False)

        return excel_file
    else:
        raise Exception(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
