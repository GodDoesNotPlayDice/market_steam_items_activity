from playwright.sync_api import sync_playwright
import dotenv, json

dot_env_path = '../config/.env'

url = dotenv.get_key(dot_env_path, 'ITEM_URL')

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
        
    print(f"Item nameid: {item_nameid[0]}, appid: {appid[0]}")
    return {"item_nameid" : item_nameid[0], "appid" : appid[0]}

with open('./data/item_info.json', "w") as f:
    json.dump(get_item_ids(url), f)
print('done')
        



