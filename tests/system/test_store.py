from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/testStore')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('testStore'))
                self.assertDictEqual({'name': 'testStore', 'items': []},
                                     json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/testStore')
                response = client.post('/store/testStore')
                expected = {'message': "A store with name 'testStore' already exists."}

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.delete('store/test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/testStore')
                response = client.get('/store/testStore')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'testStore', 'items': []}, json.loads(response.data))


    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/testStore')

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/testStore')
                ItemModel('testItem', 19.99, 1).save_to_db()

                response = client.get('/store/testStore')
                expected = {'name': 'testStore', 'items': [{'name': 'testItem', 'price': 19.99}]}

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self. app_context():
                client.post('/store/testStore')

                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'name': 'testStore', 'items': []}]}, json.loads(response.data))


    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/testStore')
                ItemModel('testItem', 19.99, 1).save_to_db()
                ItemModel('another', 9.99, 1).save_to_db()
                client.post('/store/testShop')
                ItemModel('car', 2.65, 2).save_to_db()
                ItemModel('vehicle', 1.33, 2).save_to_db()

                response = client.get('/stores')
                expected = {'stores': [
                    {'name': 'testStore', 'items': [
                        {'name': 'testItem', 'price': 19.99},
                        {'name': 'another', 'price': 9.99}
                    ]},
                    {'name': 'testShop', 'items': [
                        {'name': 'car', 'price': 2.65},
                        {'name': 'vehicle', 'price': 1.33}
                    ]}
                 ]}

                self.assertEqual(response.status_code, 200)
                self. assertDictEqual(expected, json.loads(response.data))


