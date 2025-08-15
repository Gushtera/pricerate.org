import asyncio
from playwright.async_api import async_playwright
from .models import Category, Product, Price

class Crawler:
    def __init__(self):
        self.base_url = "https://www.ebag.bg"

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            await self.get_categories(page)

            await browser.close()

    async def get_categories(self, page):
        await page.goto(self.base_url)

        # This is an assumption. The actual selector will likely be different.
        # The user will need to run this and we may need to adjust based on the output.
        category_elements = await page.query_selector_all("nav .categories a")

        for element in category_elements:
            name = await element.inner_text()
            url = await element.get_attribute("href")

            category, created = await Category.objects.aget_or_create(
                name=name,
                url=self.base_url + url
            )

            if created:
                print(f"New category found: {name}")
                await self.get_products_for_category(page, category)

    async def get_products_for_category(self, page, category):
        await page.goto(category.url)

        # This is another assumption. We will likely need to refine this.
        product_elements = await page.query_selector_all(".product-item")

        for element in product_elements:
            try:
                name_element = await element.query_selector(".product-title a")
                name = await name_element.inner_text()
                url = await name_element.get_attribute("href")

                price_element = await element.query_selector(".price .value")
                price_text = await price_element.inner_text()
                price = float(price_text.replace("лв.", "").replace(",", ".").strip())

                product, created = await Product.objects.aget_or_create(
                    name=name,
                    url=self.base_url + url,
                    defaults={'category': category}
                )

                if created:
                    print(f"New product found: {name}")

                await Price.objects.acreate(product=product, price=price)
                print(f"Price updated for {name}: {price}")

            except Exception as e:
                print(f"Error processing product: {e}")

async def main():
    crawler = Crawler()
    await crawler.run()

if __name__ == "__main__":
    asyncio.run(main())
