import json
import unittest
from pathlib import Path
from import_evo_catalog import normalize, merge

ROOT = Path(__file__).parent


class PublicCatalogueTests(unittest.TestCase):
    def test_untrusted_fields_are_normalized_without_inventing_gallery_or_sales(self):
        row = {'item_id': '123', 'titulo': 'iPhone 15 Pro', 'preco': 'NaN', 'imagem': 'javascript:alert(1)',
               'loja_nome': '<script>alert(1)</script>', 'loja_avatar': 'https://alicdn.com.evil.test/a.jpg'}
        item = normalize(row, '2026-11-22T00:00:00Z')
        self.assertIsNone(item['priceCny'])
        self.assertEqual(item['images'], [])
        self.assertEqual(item['seller']['avatarUrl'], '')
        self.assertNotIn('soldCount', item['seller'])
        self.assertIn('celulares', item['categories'])

    def test_merge_deduplicates_and_preserves_existing_translation_and_photos(self):
        original = {'items': [{'id': '123', 'title': 'Original', 'titlePt': 'Traduzido', 'priceCny': 19.99,
                              'image': 'old.jpg', 'images': ['old.jpg', 'detail.jpg'], 'categories': ['moda'], 'seller': {'name': 'Anterior'}}],
                    'categories': [{'id': 'moda'}], 'featuredIds': ['123']}
        new = {'id': '123', 'title': 'New title', 'priceCny': 50, 'image': 'new.jpg', 'images': ['new.jpg'], 'categories': [], 'seller': {'name': 'Novo'}}
        result, stats = merge(original, [new, new], 'date')
        self.assertEqual(stats['added'], 0)
        self.assertEqual(result['items'][0]['titlePt'], 'Traduzido')
        self.assertEqual(result['items'][0]['images'], ['old.jpg', 'detail.jpg', 'new.jpg'])
        self.assertEqual(result['items'][0]['priceCny'], 19.99)
        self.assertEqual(original['items'][0]['images'], ['old.jpg', 'detail.jpg'])

    def test_unknown_categories_are_not_fabricated(self):
        self.assertEqual(normalize({'item_id': '1', 'titulo': 'XYZ 123'}, 'date')['categories'], [])
        self.assertIsNone(normalize({'item_id': '../bad', 'titulo': 'Item'}, 'date'))

    def test_every_imported_id_is_present_in_full_catalogue_and_exactly_one_chunk(self):
        data = json.loads((ROOT / 'public/data/products.json').read_text(encoding='utf-8'))
        index = json.loads((ROOT / 'public/data/catalog-index.json').read_text(encoding='utf-8'))
        ids = [i['id'] for i in data['items']]
        self.assertEqual(len(ids), len(set(ids)))
        chunk_ids = []
        for n, chunk in enumerate(index['chunks']):
            rows = json.loads((ROOT / 'public/data' / chunk['file']).read_text(encoding='utf-8'))
            for item in rows:
                self.assertEqual(index['productChunks'][item['id']], n)
            chunk_ids.extend(i['id'] for i in rows)
        self.assertEqual(len(chunk_ids), len(set(chunk_ids)))
        self.assertEqual(set(chunk_ids), set(ids))
        report = json.loads((ROOT / 'EVO-IMPORTACAO.json').read_text(encoding='utf-8'))
        self.assertEqual(len(ids), report['total'])
        self.assertFalse(report['complete'])  # The upstream timed out; do not claim a full export.
        self.assertEqual(report['publicRowsImported'], 41292)


if __name__ == '__main__':
    unittest.main()
