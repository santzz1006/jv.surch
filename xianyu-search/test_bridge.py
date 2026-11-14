import threading
import time
import unittest
from unittest.mock import patch
import bridge

class BridgeTests(unittest.TestCase):
    def setUp(self):
        bridge.JOB=None;bridge.LAST_SEEN=0
    def test_requires_connected_extension(self):
        with self.assertRaisesRegex(RuntimeError,'Conecte'):bridge.collect(timeout=.01)
    def test_timeout_clears_queue(self):
        bridge.poll()
        with self.assertRaises(RuntimeError):bridge.collect(timeout=.01)
        self.assertIsNone(bridge.JOB)
    def test_query_response_round_trip(self):
        bridge.poll();result=[]
        thread=threading.Thread(target=lambda:result.extend(bridge.collect('camera',timeout=2)))
        thread.start()
        deadline=time.monotonic()+1
        while bridge.JOB is None and time.monotonic()<deadline:time.sleep(.001)
        job=bridge.poll()
        self.assertEqual(job['query'],'camera')
        self.assertIsNone(bridge.poll())
        bridge.submit({'id':job['id'],'items':[{'url':'https://www.goofish.com/item?id=123','title':'Produto de teste','priceCny':42}]})
        thread.join(2)
        self.assertEqual(result[0]['priceCny'],42)
        self.assertIsNone(bridge.JOB)
    def test_wrong_job_rejected(self):
        with self.assertRaises(ValueError):bridge.submit({'id':'not-pending','items':[]})
    def test_untrusted_items(self):
        good={'url':'https://www.goofish.com/item?id=123','title':'Teste','image':'javascript:alert(1)','priceCny':float('nan')}
        result=bridge.normalize_products([good,good,{'url':'https://evil.invalid/item?id=2','title':'bad'}])
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['image'],'')
        self.assertIsNone(result[0]['priceCny'])

if __name__=='__main__':unittest.main()
