from playwright.sync_api import sync_playwright
import json
import time
import os

items = {
    "Nightmare Case": "https://steamcommunity.com/market/listings/730/Dreams%20%26%20Nightmares%20Case",
}

path = os.path.abspath(os.path.join('src', 'data'))

if not os.path.exists(path):
    try:
        print('Creating data folder...')
        os.makedirs(path, exist_ok=True)
        print(f'Data folder created at: {path}')
    except OSError as e:
        print(f'Failed to create data folder: {e}')
        exit(1)
else:
    print(f'Data folder already exists at: {path}')


# El codigo extrae el item_nameid y el appid de la urls[0] de un item en steam market
# item_name_id : lo toma desde las request de la network.
# appid: se toma desde la urls[0] de la pagina.
def get_item_ids(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        item_nameid = [None]
        appid = [None]

        def handle_route(route, request):
            if 'itemordershistogram' in request.url:
                item_nameid[0] = request.url.split('item_nameid=')[1].split('&')[0]
            route.continue_()
        page.route('**', handle_route)
        page.goto(url)

        if '/listings/' in url:
            appid[0] = url.split('/listings/')[1].split('/')[0]
        else:
            print(f"Failed to find '/listings/' in {url}")
            print(appid[0])
        page.unroute('**')
        browser.close()
        
    print(f"Item nameid: {item_nameid[0]}, appid: {appid[0]}, name: {list(items.keys())[0]}")
    return {"item_nameid": item_nameid[0], "appid": appid[0], "name": list(items.keys())[0]}

with open(path + "/item_info.json", "+w") as f:
    while True:
        item_info = get_item_ids(url=items["Nightmare Case"])
        if dict(item_info)['item_nameid'] is None:
            print('Failed to get item_nameid')
        else:
            break
    json.dump(item_info, f)
    print('Item info saved to item_info.json')
