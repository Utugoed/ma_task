import json

from bs4 import BeautifulSoup
import httpx



cookies = {
    'region_id': '1',
    'merchant_ID_': '1',
    'methodDelivery_': '1',
    '_GASHOP': '001_Mitishchi',
    'rrpvid': '770996873268121',
    '_userGUID': '0:lj4bwxbm:rDGYlVPZ9bZjR0LBQf5UuWsxfKpprPGY',
    'rcuid': '6491ab597016a2f896df205a',
    'digi_uc': 'W1sidiIsIjcxNDA4OSIsMTY4NzM0NzkwMTg3N10sWyJ2IiwiNTIzMzIiLDE2ODczNDc1NDA4NjldLFsidiIsIjgyODI4MiIsMTY4NzM0Mzg1NzExN10sWyJ2IiwiNjkxNjc1IiwxNjg3MzM2NTY0NTQ0XV0=',
    'acceptCookies_': 'true',
    'rrlevt': '1687347902588',
    'rrviewed': '52332%2C691675%2C828282%2C714089',
    'qrator_jsid': '1687347066.642.mAwFdgmfMj7TCQVl-mk8v35r2kh48dam91o6o2gvl8612dj8g',
    '_dvs': '0:lj5mvpyp:xknCdVz5w7Q5LG8v0XCIL7PYpeoEjEms',
    'dSesn': '13d6cd97-001e-dbf8-6bcf-7fd0910f04c7',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
}

items = []

with open('links_msc', 'r') as file:
    for i, link in enumerate(file):
        print(f'{i} - Parsing {link}')
        
        with httpx.Client(cookies=cookies, headers=headers) as client:
            r = client.get(link[0:-1], timeout=150.0)

        soup = BeautifulSoup(r.text, 'html.parser')

        item = {'link': link[0:-1]}

        sale_price_elements = soup.find_all(class_='css-1129a1l')
        if not sale_price_elements:
            continue
        item['sale_price'] = sale_price_elements[0].text.split()[0]

        item['old_price'] = None
        old_price_elements = soup.find_all(class_='css-1a8h9g1')
        if old_price_elements:
            item['old_price'] = old_price_elements[0].text.split()[0]
        
        product_name = soup.find_all(lambda tag: tag.get('id') == 'productName')[0]
        item['product_name'] = product_name.string
        
        data = soup.find_all(class_='css-2619sg')
        item['product_id'] = data[0].string
        item['product_brand'] = data[1].a.string

        items.append(item)

with open('ice_creams_msc.json', 'w') as file:
    content = json.dumps(items, ensure_ascii=False)
    file.write(content)
