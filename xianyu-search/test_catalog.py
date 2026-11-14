import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import catalog

class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=patch.object(catalog,'ROOT',Path(self.temp.name));self.root.start()
    def tearDown(self):self.root.stop();self.temp.cleanup()
    def test_empty_catalog_is_not_fabricated(self):
        self.assertEqual(len(catalog.index()['categories']),29)
        self.assertEqual(catalog.all_items(),[])
        self.assertIsNone(catalog.read('celulares')['updatedAt'])
    def test_snapshot_deduplicates_and_preserves_decimal_price(self):
        row={'url':'https://www.goofish.com/item?id=123','title':'Câmera','priceCny':19.99}
        catalog.save('eletronicos',[row,row])
        data=catalog.read('eletronicos')
        self.assertEqual(data['items'][0]['priceCny'],19.99)
        self.assertEqual(data['count'],1)
        self.assertEqual(data['coverage'],'partial')
        self.assertIsNotNone(data['updatedAt'])
        catalog.save('celulares',[row])
        self.assertEqual(len(catalog.all_items()),1)
    def test_path_traversal_rejected(self):
        with self.assertRaises(KeyError):catalog.read('../.bridge-key')
        with self.assertRaises(ValueError):catalog.start('../.bridge-key')
    def test_unavailable_bridge_blocks_collection(self):
        with patch('catalog.bridge.status',return_value={'connected':False}):
            with self.assertRaises(RuntimeError):catalog.start()
    def test_failed_refresh_preserves_previous_snapshot(self):
        catalog.save('celulares',[{'url':'https://www.goofish.com/item?id=123','title':'Persistido','priceCny':1}])
        with patch('catalog.bridge.collect',side_effect=RuntimeError('Verificação necessária')):
            catalog._run([catalog.BY_ID['celulares']])
        self.assertEqual(catalog.read('celulares')['items'][0]['title'],'Persistido')
        self.assertFalse(catalog.STATE['running'])

if __name__=='__main__':unittest.main()
