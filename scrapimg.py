import requests
from bs4 import BeautifulSoup
import json

class EbayScraper:
    def __init__(self, url):
        self.url = url
        self.data = {}

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            self.data['title'] = self.get_title(soup)
            self.data['image_url'] = self.get_image_url(soup)
            self.data['product_url'] = self.url
            self.data['price'] = self.get_price(soup)
            self.data['seller'] = self.get_seller(soup)
            self.data['shipping_price'] = self.get_shipping_price(soup)
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

    def get_title(self, soup):
        title_tag = soup.find('h1', {'class': 'x-item-title__mainTitle'})
        if title_tag:
            return title_tag.text.strip()
        return "No title found"

    def get_image_url(self, soup):
        img_tag = soup.find('img', {'data-idx': '0'})
        if img_tag:
            return img_tag['src']
        return "No image URL found"

    def get_price(self, soup):
        price_tag = soup.find('div', {'class': 'x-price-primary'})
        if price_tag:
            return price_tag.text.strip()
        return "No price found"

    def get_seller(self, soup):
        seller_tag = soup.find('div', {'class': 'x-sellercard-atf__info__about-seller'})
        if seller_tag:
            return seller_tag.text.strip()
        return "No seller found"

    def get_shipping_price(self, soup):
        shipping_tag = soup.find('div', {'class': 'ux-labels-values__values col-9'})
        if shipping_tag:
            return shipping_tag.text.strip()
        return "No shipping price found"

    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def print_data(self):
        print(json.dumps(self.data, ensure_ascii=False, indent=4))


url = 'https://www.ebay.com/itm/387182364698?epid=20051901798&itmmeta=01J3BKB88H974DC5BSGW91VWQ1&hash=item5a25de081a:g:Sb0AAOSwc9xmam5I&itmprp=enc%3AAQAJAAAAwLgaSImwHEVCrAhDZXOLb1EFhesvfEoH1teYtxVzvEvCUC9iZIKib03t0RhlzP18%2FhTHoVSznsJ2jg6Q%2FlJnY3jDbXotZhMPsXeJDUVsJifBg63Ap2VOhpGKilVAa2tMINzfsTkvOlfiFFtluMNM4m9MN0cqfnfPnjQ9CrnU7%2BLCY6dwzKrOiWMjXuQvW4vOSWNNlDBnBPgHsH9UxXFaRu1%2BQIh1DeGzdnQtqfLN8SW2%2FmLFQTH3WPIVBasLBDerbg%3D%3D%7Ctkp%3ABk9SR7CErfOaZA' #Ваш URl з сайту ebay
scraper = EbayScraper(url)
scraper.fetch_data()
scraper.print_data()  
scraper.save_to_file('product_data.json')  
