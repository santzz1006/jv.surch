"""Exercise the actual unpacked extension in an isolated Chromium profile."""
import asyncio
import json
import os
import tempfile
from pathlib import Path
from playwright.async_api import async_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(tempfile.gettempdir()) / 'goofish-br-1.3.3-qa'


async def main():
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser = Path(os.environ['LOCALAPPDATA']) / 'ms-playwright/chromium-1254/chrome-win64/chrome.exe'
        extension = str(ROOT / 'extension-shop')
        context = await p.chromium.launch_persistent_context(tempfile.mkdtemp(prefix='goofish-br-qa-'),
            executable_path=str(browser), headless=True,
            args=[f'--disable-extensions-except={extension}', f'--load-extension={extension}'],
            viewport={'width': 460, 'height': 600})
        try:
            worker = context.service_workers[0] if context.service_workers else await context.wait_for_event('serviceworker')
            ident = worker.url.split('/')[2]
            page = await context.new_page(); errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            await page.goto(f'chrome-extension://{ident}/popup.html')
            await page.wait_for_selector('.product-card', timeout=60000)
            await page.wait_for_timeout(1500)
            await page.screenshot(path=str(OUT / 'popup-460.png'))
            tabs = len(context.pages)
            await page.locator('#browse-query').fill('iphone')
            await page.locator('#browse-submit').click()
            await expect(page.locator('#browse-submit')).to_be_enabled()
            assert await page.locator('.product-card').count() == 24
            await page.locator('#search-next').click()
            await expect(page.locator('#search-count')).to_contain_text('página 2')
            assert len(context.pages) == tabs, 'Search must not open a tab'
            await page.locator('.product-cover').first.click()
            assert await page.locator('#product-dialog').is_visible()
            assert await page.locator('#detail-agents a').count() >= 4
            await page.screenshot(path=str(OUT / 'product-460.png'))
            await page.locator('#detail-save').click()
            await page.locator('#detail-close').click()
            await page.locator('[data-view=saved]').click()
            await page.wait_for_selector('.saved-card')
            await page.locator('[data-view=alerts]').click()
            await page.locator('#target-price').fill('10')
            await page.locator('#watch-form button').click()
            await expect(page.locator('#watches .card')).to_have_count(1)
            await page.locator('#check-alerts').click()
            await expect(page.locator('#check-alerts')).to_be_enabled()
            await expect(page.locator('#watches')).to_contain_text('Aguardando uma nova consulta')
            await page.locator('#watches button').click()
            await expect(page.locator('#watches .card')).to_have_count(0)
            await page.locator('[data-view=explore]').click()
            assert not errors, errors
            # A deterministic marketplace document tests the injected toolbar and real iframe permissions.
            await context.route('https://www.goofish.com/qa-extension', lambda route: route.fulfill(content_type='text/html', body='<html><body><h1>Marketplace test</h1><div id="login">Login original</div></body></html>'))
            market = await context.new_page()
            await market.set_viewport_size({'width': 1280, 'height': 900})
            await market.goto('https://www.goofish.com/qa-extension')
            await market.wait_for_selector('#gb-quick-host')
            # The shadow root is intentionally closed. Use its stable screen position as a user would.
            await market.mouse.click(1280 - 16 - 3*54 - 24, 40)
            frame = None
            for _ in range(80):
                frame = next((f for f in market.frames if f.url.startswith(f'chrome-extension://{ident}/popup.html')), None)
                if frame and await frame.locator('.product-card').count():
                    break
                await asyncio.sleep(.25)
            assert frame and await frame.locator('.product-card').count(), 'Quick-search iframe did not render'
            await frame.locator('#browse-query').fill('ipad')
            await frame.locator('#browse-submit').click()
            await expect(frame.locator('#browse-submit')).to_be_enabled()
            assert await market.locator('#login').inner_text() == 'Login original'
            await market.screenshot(path=str(OUT / 'overlay-desktop.png'))
            await market.set_viewport_size({'width':320,'height':700})
            assert await frame.evaluate('() => document.documentElement.scrollWidth <= innerWidth')
            await market.screenshot(path=str(OUT / 'popup-320.png'))
            await frame.locator('[data-view=cloud]').click()
            await frame.locator('#quick-enabled').uncheck()
            await expect(market.locator('#gb-quick-host')).to_be_hidden()
            result = {'version': json.loads((ROOT/'extension-shop/manifest.json').read_text(encoding='utf-8'))['version'], 'products': len(json.loads((ROOT/'extension-shop/data/catalog.json').read_text(encoding='utf-8'))['items']), 'localAlertsWithoutAdminKey': True, 'searchWithoutNewTab': True,
                      'pagination': True, 'detailsAndSave': True, 'responsive320': True,
                      'realExtensionIframe': True, 'overlayToggle': True, 'pageErrors': errors}
            (OUT / 'result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
            print(json.dumps(result), flush=True)
        finally:
            await context.close()


if __name__ == '__main__':
    asyncio.run(main())
