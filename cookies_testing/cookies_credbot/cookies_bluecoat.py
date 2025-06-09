from playwright.async_api import async_playwright
import asyncio
import random

async def get_category(url: str) -> list:
    """
    Returns a tuple containing lists of first party and third party cookies hosted on a given website.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        
        await page.wait_for_selector('span.clickable-category')

        html = await page.content()
        print(html)
        await browser.close()

async def main():
    await get_category("https://sitereview.bluecoat.com/#/lookup-result/https%253A%252F%252Fwww.youtube.com%252F")

if __name__ == "__main__":
    asyncio.run(main())

#doesn't work due to recaptcha