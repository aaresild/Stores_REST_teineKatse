from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/testItem')

                self.assertEqual(resp.status_code, 401)  # not authorized

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers={'Authorization': self.access_token})

                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual({'message': 'Item not found'}, json.loads(resp.data))

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('testStore').save_to_db()
                ItemModel('testItem', 19.99, 1).save_to_db()
                resp = client.get('/item/testItem', headers={'Authorization': self.access_token})

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'name': 'testItem', 'price': 19.99}, json.loads(resp.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('testStore').save_to_db()
                ItemModel('testItem', 19.99, 1).save_to_db()

                resp = client.delete('/item/testItem')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'message': 'Item deleted'})

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('testStore').save_to_db()

                resp = client.post('/item/testItem', data={'price': 13.20, 'store_id': 1})

                self.assertEqual(201, resp.status_code)
                self.assertDictEqual({'name': 'testItem', 'price': 13.20}, json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('testStore').save_to_db()

                client.post('/item/testItem', data={'price': 13.20, 'store_id': 1})
                resp = client.post('/item/testItem', data={'price': 13.20, 'store_id': 1})

                self.assertEqual(400, resp.status_code)
                self.assertDictEqual({'message': "An item with name 'testItem' already exists."}, json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('testStore').save_to_db()
                resp = client.put('/item/testItem', data={'price': 3.45, 'store_id': 1})

                self.assertEqual(200, resp.status_code)
                self.assertEqual(ItemModel.find_by_name('testItem').price, 3.45)
                self.assertDictEqual({'name': 'testItem', 'price': 3.45}, json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('testStore').save_to_db()
                ItemModel('testItem', 5.55, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('testItem').price, 5.55)

                resp = client.put('/item/testItem', data={'price': 18.99, 'store_id': 1})

                self.assertEqual(200, resp.status_code)
                self.assertEqual(ItemModel.find_by_name('testItem').price, 18.99)
                self.assertDictEqual({'name': 'testItem', 'price': 18.99}, json.loads(resp.data))


    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('testStore').save_to_db()
                ItemModel('red', 0.85, 1).save_to_db()
                ItemModel('green', 0.35, 1).save_to_db()
                ItemModel('blue', 0.55, 1).save_to_db()

                resp = client.get('/items')
                expected = {
                    'items': [
                        {'name': 'red', 'price': 0.85},
                        {'name': 'green', 'price': 0.35},
                        {'name': 'blue', 'price': 0.55}
                    ]
                }

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))
