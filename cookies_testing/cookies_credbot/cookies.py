from playwright.sync_api import sync_playwright
import math

def get_cookies(url: str, domain: str) -> tuple:
    """
    Returns a tuple containing lists of first party and third party cookies hosted on a given website.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Use True for headless
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        cookies = context.cookies()
        print(cookies)
        browser.close()

        first_party = []
        third_party = []
        for cookie in cookies:
            if domain in cookie['domain']:
                first_party.append(cookie)
            else:
                third_party.append(cookie)
        return (first_party, third_party)
    
def get_percent_third_party(cookies: tuple) -> tuple:
    "Returns a tuple containing the number of third party and the total number of cookies, as well as the percent third party."
    thirdparty = len(cookies[1])
    total = len(cookies[0] + cookies[1])
    if thirdparty != 0:
        percent = round((thirdparty / total)*100, 2)
    else:
        percent = None
    return (thirdparty, total, percent)

def get_secure_cookies(cookies: tuple) -> dict:
    """
    Returns a dict containing the domains of cookies hosted on a given website and whether they are secure.
    """
    secure_cookies = {"secure":[], "insecure":[]}
    for cookie in (cookies[0] + cookies[1]):
        if cookie['secure'] == True:
            secure_cookies['secure'].append(cookie['domain'])
        else:
            secure_cookies['insecure'].append(cookie['domain'])
    return secure_cookies

cookies = get_cookies("https://www.bbc.com/news/articles/cd7gp8l1241o", "bbc")

print(get_percent_third_party(cookies))
print(get_secure_cookies(cookies))