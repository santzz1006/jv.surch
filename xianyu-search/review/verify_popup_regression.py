"""Test Chrome's real action popup sizing and activation in an existing tab."""
import asyncio
import base64
import json
import os
import tempfile
from pathlib import Path
from playwright.async_api import async_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(tempfile.gettempdir()) / 'goofish-br-1.3.1-qa'


async def main():
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        ext = str(ROOT / 'extension-shop')
        browser = str(Path(os.environ['LOCALAPPDATA']) / 'ms-playwright/chromium-1254/chrome-win64/chrome.exe')
        context = await p.chromium.launch_persistent_context(tempfile.mkdtemp(prefix='gb-popup-regression-'),
            executable_path=browser, headless=True, no_viewport=True,
            args=[f'--disable-extensions-except={ext}', f'--load-extension={ext}'])
        try:
            worker = context.service_workers[0] if context.service_workers else await context.wait_for_event('serviceworker')
            await worker.evaluate('() => chrome.action.openPopup()')
            cdp = await context.browser.new_browser_cdp_session()
            targets = await cdp.send('Target.getTargets')
            popup = next(t for t in targets['targetInfos'] if t['url'].endswith('/popup.html'))
            session = (await cdp.send('Target.attachToTarget', {'targetId': popup['targetId']}))['sessionId']
            pending = {}; seq = 0
            def receive(event):
                msg = json.loads(event['message'])
                if event.get('sessionId') == session and msg.get('id') in pending:
                    pending.pop(msg['id']).set_result(msg)
            cdp.on('Target.receivedMessageFromTarget', receive)
            async def call(method, params=None):
                nonlocal seq
                seq += 1; future = asyncio.get_running_loop().create_future(); pending[seq] = future
                await cdp.send('Target.sendMessageToTarget', {'sessionId': session,
                    'message': json.dumps({'id': seq, 'method': method, 'params': params or {}})})
                answer = await asyncio.wait_for(future, 15)
                assert 'error' not in answer, answer
                return answer['result']
            async def evaluate(expression):
                result = await call('Runtime.evaluate', {'expression': expression, 'returnByValue': True})
                assert 'exceptionDetails' not in result, result
                return result['result'].get('value')
            for _ in range(100):
                if await evaluate("document.querySelectorAll('.product-card').length"):
                    break
                await asyncio.sleep(.2)
            width = await evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth,root:getComputedStyle(document.documentElement).minWidth})')
            assert 450 <= width['width'] <= 480, width
            assert width['scroll'] <= width['width'], width
            await evaluate("document.querySelector('#browse-query').value='iphone';document.querySelector('#browse-form').requestSubmit();")
            for _ in range(100):
                if await evaluate("!document.querySelector('#browse-submit').disabled"):
                    break
                await asyncio.sleep(.1)
            assert await evaluate("document.querySelectorAll('.product-card').length") == 24
            await asyncio.sleep(.5)
            shot = await call('Page.captureScreenshot', {'format': 'png'})
            (OUT / 'native-action-popup.png').write_bytes(base64.b64decode(shot['data']))
            await cdp.send('Target.closeTarget', {'targetId': popup['targetId']})

            await context.route('https://www.goofish.com/qa-activation', lambda r: r.fulfill(content_type='text/html', body='<h1>Existing marketplace tab</h1>'))
            page = await context.new_page()
            await page.set_viewport_size({'width': 1280, 'height': 900})
            await page.goto('https://www.goofish.com/qa-activation')
            await page.wait_for_selector('#gb-quick-host')
            document_id = await page.evaluate('() => performance.timeOrigin')
            # Toggle the real Chrome extension control; keep the Goofish tab loaded.
            manager = await context.new_page()
            await manager.goto('chrome://extensions/')
            ident = worker.url.split('/')[2]
            toggle = manager.locator('extensions-item#'+ident).locator('#enableToggle')
            await toggle.click()
            await manager.wait_for_timeout(500)
            async with context.expect_event('serviceworker', timeout=30000) as new_worker:
                await toggle.click()
            worker = await new_worker.value
            await expect(page.locator('#gb-quick-host')).to_have_count(1)
            await page.wait_for_timeout(1200)
            assert await page.evaluate('() => performance.timeOrigin') == document_id
            await page.mouse.click(1078, 40)
            frame = None
            for _ in range(120):
                frame = next((f for f in page.frames if '/popup.html?surface=overlay' in f.url), None)
                if frame and await frame.locator('.product-card').count():
                    break
                await asyncio.sleep(.2)
            assert frame and await frame.locator('.product-card').count() == 24, 'Stale or missing overlay after reload'
            await page.set_viewport_size({'width': 320, 'height': 700})
            assert await frame.evaluate('() => document.documentElement.scrollWidth <= innerWidth')
            await page.screenshot(path=str(OUT / 'embedded-320.png'))
            await frame.locator('[data-view=cloud]').click()
            await frame.locator('#quick-enabled').uncheck()
            await expect(page.locator('#gb-quick-host')).to_be_hidden()
            await worker.evaluate('() => chrome.storage.local.set({gbQuickSearch:true})')
            await expect(page.locator('#gb-quick-host')).to_be_visible()
            await worker.evaluate('() => Promise.all([ensureOpenGoofishPanels(),ensureOpenGoofishPanels()])')
            await expect(page.locator('#gb-quick-host')).to_have_count(1)
            report = {'nativePopup': width, 'searchInsidePopup': True, 'existingTabAfterDisableEnable': True,
                      'noPageReload': True, 'embedded320': True, 'activationToggle': True, 'noDuplicateToolbar': True}
            (OUT / 'result.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
            print(json.dumps(report), flush=True)
        finally:
            await context.close()


if __name__ == '__main__':
    asyncio.run(main())
