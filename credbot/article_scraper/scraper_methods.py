import requests
from bs4 import BeautifulSoup

def get_urls(domain_url: str) -> list:
    """
    Returns a list of article URLS present on a webpage.
    """
    try:
        domain = f"https://{domain_url}"
        try:
            html = requests.get(domain, timeout=5)
        except requests.exceptions.Timeout:
            print("The request timed out.")
            return None
        soup = BeautifulSoup(html.text, "html.parser")
        links = soup.find_all("a")
        urls = []
        for link in links:
            l = link.get('href')
            if l:
                # if len(l) > len(domain)+5:
                if ("-" in l) and ("?" not in l):
                    if domain_url in l:
                        if "https" in l:
                            urls.append(l)
                        else:
                            if domain_url[-1] != "/":
                                urls.append(f"{domain_url}/{l}")
                            else:
                                urls.append(f"{domain_url}{l}")

        if urls:
            urls = list(set(urls))
            urls = sorted(urls, key=lambda url: len(url), reverse=True)
            return urls
        return None
    except Exception as e:
        return None

def scrape_url(domain_url:str, url:str) -> str:
    """
    Returns the HTML string of the content within all 'p', 'h1', 'h2', 'h3', 'li' and 'a' tags from a URL.
    Checks whether the article is part of the domain before scraping.
    """
    if domain_url in url:
        try:
            try:
                response = requests.get(url, timeout = 5)
            except requests.exceptions.Timeout:
                print("The request timed out.")
                return None
            soup = BeautifulSoup(response.text, "html.parser")
            tags = soup.find_all(['p', 'h1', 'h2', 'h3', "li", "a"])

            html_parts = [str(tag) for tag in tags]
            html_string = '\n'.join(html_parts)
            return html_string
        
        except Exception:
            return None
            pass
    else:
        print("URL is external from domain.")
        return None

def is_integer(char:str) -> bool:
    """
    Returns a bool indicating whether a character is an integer
    """
    return char in ['1','2','3','4','5','6','7','8','9','0']

def get_article_title(url: str) -> str:
    """
    Returns the article title from a URL, otherwise returns 'Unknown'.
    """
    parts = url.split("/")
    couldbtitles = []
    for part in parts:
        if "-" in part:
            couldbtitles.append(part)
    if couldbtitles == None:
        return None
    num = len(couldbtitles)
    if num == 0:
        return None
    else:
        try:
            tries = 0
            index = 0
            titles = []
            while tries < len(couldbtitles):
                ints = 0
                for word in [word.capitalize() for word in couldbtitles[index-1].split("-")]:
                    for char in word:
                        if is_integer(char):
                            ints += 1
                if ints < (len(couldbtitles[index-1])/7):
                    titles.append(" ".join([word.capitalize() for word in couldbtitles[index-1].split("-")]))
                tries += 1
                index -= 1
            if titles:
                t = sorted(titles, key=lambda x: len(x))
                return t[-1]
        except IndexError:
            return None
        return None

# print(get_article_title("https://www.10news.com/americavotes/san-diego-county-district-1-debate/full-interview-imperial-beach-mayor-paloma-aguirre-sits-down-with-10news-ahead-of-district-1-debate"))
# print(get_article_title("https://www.11alive.com/article/syndication/smart-deals/stackcommerce/excel-at-work-by-supercharging-your-pc-with-microsoft-office-and-windows-11-pro-for-less-than-50/608-b76cb1ea-0466-4725-96a8-68d1a63082eb"))
# print(get_article_title("https://actaneurocomms.biomedcentral.com/articles/10.1186/s40478-023-01513-0"))
# print(get_article_title("https://twitter.com/intent/tweet?&text=Where%20to%20Escape%20the%20Crowds%20within%20Prague%20and%20the%20Czech%20Republic%20This%20Summer&via=alexcityoutlook&url=https%3A%2F%2Fwww.alexcityoutlook.com%2Fnews%2Fcontent_exchange%2Fwhere-to-escape-the-crowds-within-prague-and-the-czech-republic-this-summer%2Farticle_1025f887-999e-5551-bb85-923a3dd533b9.html%3Futm_medium%3Dsocial%26utm_source%3Dtwitter%26utm_campaign%3Duser-share"))
# print(get_article_title("https://www.boredpanda.com/jojo-siwa-dropped-by-record-label-revealing-not-lesbian-admitting-relationship-with-chris-hughes/#post-comments"))
