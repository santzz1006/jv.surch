import unittest
from scraper import normalize, price_number
from server import filter_items

class SearchTests(unittest.TestCase):
    def test_filter_sort_and_missing_prices(self):
        items=[{'priceCny':None},{'priceCny':20},{'priceCny':5},{'priceCny':100}]
        self.assertEqual([x['priceCny'] for x in filter_items(items,{'sort':['desc']})['items']],[100,20,5,None])
        self.assertEqual(filter_items(items,{'min':['10'],'max':['50']})['items'],[{'priceCny':20}])
    def test_validation(self):
        for args in ({'min':['nan']},{'max':['-1']},{'min':['3'],'max':['2']},{'page':['0']},{'sort':['unknown']}):
            with self.assertRaises(ValueError): filter_items([],args)
    def test_pagination(self):
        items=[{'priceCny':i} for i in range(45)]
        page=filter_items(items,{'page':['2']})
        self.assertEqual(len(page['items']),20)
        self.assertEqual(page['items'][0]['priceCny'],20)
        self.assertTrue(page['hasMore'])
        self.assertFalse(filter_items(items,{'page':['3']})['hasMore'])
    def test_normalize(self):
        row={'url':'https://www.goofish.com/item?id=123','title':'Anúncio de teste','text':'Preço ¥ 19.90'}
        result=normalize([row,row,{**row,'url':'javascript:alert(1)'},{**row,'url':'https://other.invalid/item?id=1'}])
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['priceCny'],19.9)
        self.assertIsNone(price_number('a combinar'))

if __name__ == '__main__': unittest.main()
