from bs4 import BeautifulSoup

from ..network import requests, get
from ..utils.extras import currencies, list_monitors_images, bank_dict

requests.packages.urllib3.disable_warnings()

def _get_rate_by_id(tag_id: str, soup: BeautifulSoup):
    return float(soup.find(id=tag_id).find('strong').text.strip().replace(',', '.'))

def _get_time(soup: BeautifulSoup):
    date = soup.find('span', 'date-display-single').get('content')
    return date.split('T')[0].replace('-', '/')

class BCV:
    def __init__(self, url: str, **kwargs) -> None:
        response = get(f'{url}tasas-informativas-sistema-bancario', verify=False)
        self.soup = BeautifulSoup(response, 'html.parser')

    def _load(self) -> None:
        self.rates = []
        section_tipo_de_cambio_oficial = self.soup.find('div', 'view-tipo-de-cambio-oficial-del-bcv')
        section_sistema_bancario = self.soup.find('div', 'table-responsive')

        for bank in section_sistema_bancario.find('tbody').find_all('tr'):
            title = str(bank.find('td', 'views-field views-field-views-conditional').text).strip()
            key   = bank_dict.get(title)

            if title not in [bank['title'] for bank in self.rates]:
                price = float(str(bank.find('td', 'views-field views-field-field-tasa-venta').text).replace(',', '.'))

                self.rates.append({
                    'key': key,
                    'title': title,
                    'price_old': price,
                    'price': round(price, 2),
                    'last_update': str(bank.find('td', 'views-field views-field-field-fecha-del-indicador').text).strip().replace('-', '/')
                })

        for code, values in currencies.items():
            image = next((image.image for image in list_monitors_images if image.provider == 'bcv' and image.title == code), None)
            self.rates.append({
                'key': code,
                'title': values['name'],
                'price': round(_get_rate_by_id(values['id'], section_tipo_de_cambio_oficial), 2),
                'price_old': _get_rate_by_id(values['id'], section_tipo_de_cambio_oficial),
                'image': image,
                'last_update': _get_time(section_tipo_de_cambio_oficial)
            })

    def get_values(self):
        self._load()
        return self.rates