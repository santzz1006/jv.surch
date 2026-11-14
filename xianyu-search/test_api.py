"""Testes HTTP com coletor simulado; não comprovam acesso à fonte externa."""
import json
import threading
import unittest
import urllib.request
import urllib.error
from unittest.mock import patch, AsyncMock, Mock
import server
from scraper import ScrapeError, normalize, price_number

class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http = server.ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        cls.thread = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = 'http://127.0.0.1:' + str(cls.http.server_port)
    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()
        cls.thread.join()
    def setUp(self):
        server.CACHE.clear()
        server.LAST_RUN = 0
        server.LOGIN_PROCESS = None
        server.LAST_SOURCE = {'state':'not_checked','message':'Teste'}
    def request(self, path, method='GET', headers=None):
        req = urllib.request.Request(self.base+path, method=method, headers=headers or {})
        try: response = urllib.request.urlopen(req,timeout=5)
        except urllib.error.HTTPError as e: response=e
        with response:
            body=response.read()
            return response.status, json.loads(body) if 'application/json' in response.headers.get('Content-Type','') else body
    def test_health(self):
        status, body=self.request('/api/health')
        self.assertEqual(status,200)
        self.assertEqual(body['source']['state'],'not_checked')
    def test_static_and_private_files(self):
        for path in ['/','/app.js','/app.css','/assets/base.css']:
            self.assertEqual(self.request(path)[0],200)
        for path in ['/server.py','/scraper.py','/.browser-profile/','/../server.py']:
            self.assertEqual(self.request(path)[0],404)
    def test_validation_before_collect(self):
        with patch('server.collect',new_callable=AsyncMock) as collect:
            for query in ['','q=','q='+('x'*121),'q=a&min=nan','q=a&max=inf','q=a&min=9&max=2','q=a&page=0','q=a&page=1.5','q=a&sort=wrong']:
                self.assertEqual(self.request('/api/search?'+query)[0],400)
            collect.assert_not_called()
    def test_cache_and_filter_no_second_scrape(self):
        rows=[{'id':str(i),'priceCny':i,'title':'TEST FIXTURE'} for i in range(45)]
        with patch('server.collect',new_callable=AsyncMock,return_value=rows) as collect:
            status, body=self.request('/api/search?q=test')
            self.assertEqual(status,200)
            self.assertFalse(body['cached'])
            status, body=self.request('/api/search?q=test&min=10&max=40&sort=desc&page=2')
            self.assertEqual(status,200)
            self.assertTrue(body['cached'])
            self.assertEqual(body['total'],31)
            self.assertEqual(body['items'][0]['priceCny'],20)
            self.assertEqual(collect.await_count,1)
    def test_empty_results(self):
        with patch('server.collect',new_callable=AsyncMock,return_value=[]):
            status, body=self.request('/api/search?q=empty')
            self.assertEqual(status,200)
            self.assertEqual(body['total'],0)
            self.assertFalse(body['hasMore'])
    def test_login_error_is_not_empty_success(self):
        with patch('server.collect',new_callable=AsyncMock,side_effect=ScrapeError('Login necessário','LOGIN_REQUIRED')):
            status, body=self.request('/api/search?q=blocked')
            self.assertEqual(status,503)
            self.assertEqual(body['code'],'LOGIN_REQUIRED')
            self.assertNotIn('blocked',server.CACHE)
            self.assertEqual(self.request('/api/health')[1]['source']['state'],'LOGIN_REQUIRED')
    def test_unexpected_error_is_sanitized(self):
        with patch('server.collect',new_callable=AsyncMock,side_effect=RuntimeError('secret test string')):
            status, body=self.request('/api/search?q=failed')
            self.assertEqual(status,502)
            self.assertNotIn('secret',json.dumps(body))
    def test_rate_limit(self):
        with patch('server.collect',new_callable=AsyncMock,return_value=[]):
            self.assertEqual(self.request('/api/search?q=first')[0],200)
            self.assertEqual(self.request('/api/search?q=second')[0],429)
    def test_busy(self):
        server.LOCK.acquire()
        try: self.assertEqual(self.request('/api/search?q=busy')[0],429)
        finally: server.LOCK.release()
    def test_cross_origin(self):
        for headers in [{'Origin':'https://evil.invalid'},{'Host':'evil.invalid'},{'Sec-Fetch-Site':'cross-site'}]:
            self.assertEqual(self.request('/api/search?q=test',headers=headers)[0],403)
            self.assertEqual(self.request('/api/session/open','POST',headers)[0],403)
    def test_unknown_api(self):
        self.assertEqual(self.request('/api/nope')[0],404)
        self.assertEqual(self.request('/api/nope','POST')[0],404)
    def test_session_open_close(self):
        process=Mock()
        process.poll.return_value=None
        process.stdin.closed=False
        with patch('server.subprocess.Popen',return_value=process) as launch:
            self.assertEqual(self.request('/api/session/open','POST')[0],200)
            self.assertEqual(self.request('/api/session/open','POST')[0],200)
            self.assertEqual(launch.call_count,1)
            self.assertEqual(self.request('/api/search?q=test')[0],409)
            self.assertEqual(self.request('/api/session/finish','POST')[0],200)
            process.stdin.write.assert_called_once_with('\n')
    def test_session_open_while_busy(self):
        server.LOCK.acquire()
        try: self.assertEqual(self.request('/api/session/open','POST')[0],409)
        finally: server.LOCK.release()
    def test_cache_expiry(self):
        server.CACHE['old']=(0,[])
        with patch('server.collect',new_callable=AsyncMock,return_value=[]) as collect:
            self.assertFalse(self.request('/api/search?q=old')[1]['cached'])
            self.assertEqual(collect.await_count,1)

class NormalizationTests(unittest.TestCase):
    def test_translation_validation(self):
        for text,lang in [('', 'en'),('x','invalid'),('x'*3001,'en')]:
            with self.assertRaises(ValueError): server.translate_text(text,lang)
    def test_translation_cache(self):
        server.TRANSLATIONS.clear()
        import io
        with patch('server.urllib.request.urlopen',return_value=io.BytesIO(b'{"responseStatus":200,"responseData":{"translatedText":"camera"}}')) as fetch:
            self.assertEqual(server.translate_text('test camera','en'),'camera')
            self.assertEqual(server.translate_text('test camera','en'),'camera')
            self.assertEqual(fetch.call_count,1)
    def test_price_formats(self):
        for text, expected in [('¥1,299.50',1299.5),('￥ 0',0),('¥9999',9999),('negociável',None)]:
            self.assertEqual(price_number(text),expected)
    def test_canonical_deduplication(self):
        rows=[{'url':'https://www.goofish.com/item?id=123&track=a','title':'Teste','text':'¥1'},
              {'url':'http://goofish.com/item?track=b&id=123','title':'Teste','text':'¥1'},
              {'url':'https://www.goofish.com/item?bad=1','title':'Teste','text':'¥1'}]
        result=normalize(rows)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['url'],'https://www.goofish.com/item?id=123')

if __name__=='__main__': unittest.main()
