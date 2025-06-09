import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from selenium.common.exceptions import StaleElementReferenceException # Import the specific exception

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

def get_cookies(url: str):
    try:
        driver.get(url)

        driver.implicitly_wait(10)

        parsed_main_domain = urlparse(url).netloc
        main_domain_parts = parsed_main_domain.split('.')
        root_main_domain = ".".join(main_domain_parts[-2:]) if len(main_domain_parts) >= 2 else parsed_main_domain
        all_current_cookies = driver.get_cookies()

        #first party cookies
        first_party_cookies = [
            cookie for cookie in all_current_cookies
            if root_main_domain in cookie['domain'] or cookie['domain'].endswith('.' + root_main_domain)
        ]

        # Get all elements that typically load external resources

        resource_elements = driver.find_elements(By.XPATH, "//img[@src] | //script[@src] | //link[@href][@rel='stylesheet'] | //iframe[@src] | //video[@src]")

        third_party_domains = set()

        # Iterate with a try-except block for StaleElementReferenceException
        for element in resource_elements:
            try:
                src_or_href = element.get_attribute("src") or element.get_attribute("href")
                if src_or_href:
                    try:
                        parsed_url = urlparse(src_or_href)
                        resource_domain = parsed_url.netloc

                        # Handle cases like "example.com" vs ".example.com" or "www.example.com"
                        root_resource_domain = ".".join(resource_domain.split('.')[-2:]) if len(resource_domain.split('.')) >= 2 else resource_domain


                        # If the resource domain is different from the main domain, it's a potential third party
                        # Also ensure it's not a subdomain of the main domain (unless you want to count those)
                        if root_resource_domain and \
                        root_resource_domain != root_main_domain and \
                        not root_resource_domain.endswith('.' + root_main_domain): # Exclude direct subdomains of main
                            third_party_domains.add(root_resource_domain)
                    except ValueError:
                        pass
            except StaleElementReferenceException:
                print("  [DEBUG] StaleElementReferenceException caught. Skipping this element.")
                continue

        if third_party_domains:
            for domain in sorted(list(third_party_domains)):
                print(f"- {domain}")
    finally:
        driver.quit()

    return (len(all_current_cookies), first_party_cookies, sorted(list(third_party_domains)))

def get_thirdparty_percent(cookies: tuple):
    return f"{str(len(cookies[2]) / cookies[0])[2:]}% third party cookies"

def analyze_cookies(cookies: tuple):
    return

cookies = get_cookies("https://www.bbc.com/news/articles/cd7gp8l1241o")
print(get_thirdparty_percent(cookies))