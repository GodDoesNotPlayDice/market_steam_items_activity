from playwright.sync_api import sync_playwright
import json

def get_item_from_json():
    with open('request.json') as f:
        rq = json.load(f)
        return rq['link']

item_url = get_item_from_json()


def get_item_id(link):
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
        page.goto(link)

        if '/listings/' in link:
            appid[0] = link.split('/listings/')[1].split('/')[0]
        else:
            print(f"Failed to find '/listings/' in {link}")
            print(appid[0])
        page.unroute('**')
        browser.close()
    print(f"Item nameid: {item_nameid[0]}, appid: {appid[0]}")
    return {"item_nameid" : item_nameid[0], "appid" : appid[0]}

with open('item_data.json', "w") as f:
    json.dump(get_item_id(item_url), f)
  
print('done')
        



