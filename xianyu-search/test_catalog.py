import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import catalog

class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=patch.object(catalog,'ROOT',Path(self.temp.name));self.root.start()
        self.base=patch.object(catalog,'BASE',Path(self.temp.name));self.base.start()
    def tearDown(self):self.base.stop();self.root.stop();self.temp.cleanup()
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
    def test_pagination_preserves_more_than_200_unique_products(self):
        def row(i):return {'url':f'https://www.goofish.com/item?id={i}','title':f'Produto {i}','priceCny':i}
        catalog.save_page('celulares',[row(i) for i in range(1,161)],1)
        catalog.save_page('celulares',[row(i) for i in range(150,301)],2)
        result=catalog.read('celulares')
        self.assertEqual(result['count'],300)
        self.assertEqual(result['scanPage'],2)
        self.assertEqual(len(catalog.export()['items']),300)
    def test_live_product_persists_without_an_assigned_category(self):
        row={'url':'https://www.goofish.com/item?id=123','title':'Teste','priceCny':1}
        item=catalog.save_live([row])[0]
        self.assertEqual(item['categories'],[])
        self.assertEqual(catalog.export()['items'][0]['id'],'123')
    def test_varied_queries_resume_independently_and_keep_prior_pages(self):
        def row(i):return {'url':f'https://www.goofish.com/item?id={i}','title':'Teste','priceCny':1}
        catalog.save_page('moda',[row(1)],3)
        catalog.save_page('moda',[row(2)],1,query='男装')
        catalog.save_page('moda',[row(2),row(3)],2,query='运动鞋')
        result=catalog.read('moda')
        self.assertEqual(result['scanPage'],3)
        self.assertEqual(result['scanPages'],{'男装':1,'运动鞋':2})
        self.assertEqual(result['count'],3)
    def test_variety_reaches_target_without_requesting_extra_pages(self):
        row={'url':'https://www.goofish.com/item?id=123','title':'Tênis','priceCny':20}
        with patch.object(catalog.bridge,'collect',return_value=[row]) as collect,patch.object(catalog.time,'sleep'):
            catalog._collect_variety('esportes',1)
        self.assertEqual(collect.call_count,1)
        self.assertEqual(collect.call_args.args[0],'跑步鞋')
        self.assertEqual(catalog.read('esportes')['count'],1)
    def test_detail_merges_real_gallery_and_preserves_category(self):
        row={'url':'https://www.goofish.com/item?id=123','title':'Teste','priceCny':1,'image':'https://example.com/1.png'}
        catalog.save('celulares',[row])
        detail=catalog.bridge.normalize_products([{**row,'description':'Detalhes','images':['https://example.com/1.png','https://example.com/2.png']}])[0]
        result=catalog.save_detail(detail)
        self.assertEqual(len(result['images']),2)
        self.assertEqual(result['categories'],['celulares'])
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
