from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test')

        self.assertListEqual(store.items.all(), [])

    def test_crud(self):
        with self.app_context():
            store = StoreModel('testStore')

            self.assertIsNone(StoreModel.find_by_name('testStore'))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('testStore'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('testStore'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('testStore')
            item = ItemModel('testItem', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'testItem')

    def test_store_json(self):
        store = StoreModel('test')
        expected = {
            'id': None,
            'name': 'test',
            'items': []
        }

        self.assertDictEqual(store.json(), expected)

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('testStore')
            item = ItemModel('testItem', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'id': 1,
                'name': 'testStore',
                'items': [{
                    'name': 'testItem',
                    'price': 19.99
                }]
            }

            self.assertDictEqual(store.json(), expected)
