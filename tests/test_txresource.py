from unittest import TestCase

import responses

from requests_threads import AsyncSession
from twisted.internet.defer import inlineCallbacks
from twisted.internet import threads

from genericclient import GenericClient, Resource, AmbiguousComparison


MOCK_API_URL = 'http://dummy.org'

session = AsyncSession(n=100)
generic_client = GenericClient(url=MOCK_API_URL, session=session)


# Create your tests here.
class ResourceTestCase(TestCase):

    def test_resource_delete(self):
        @inlineCallbacks
        def f(*args):
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, MOCK_API_URL + '/users/1', json={
                    'id': 1,
                    'username': 'user1',
                    'group': 'watchers',
                })

                user1 = yield generic_client.users.get(id=1)
                self.assertEqual(user1.username, 'user1')

            with responses.RequestsMock() as rsps:
                rsps.add(responses.DELETE, MOCK_API_URL + '/users/1', status=204)

                yield user1.delete()
        threads.deferToThread(f)

    def test_resource_delete_uuid(self):
        @inlineCallbacks
        def f(*args):
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, MOCK_API_URL + '/users/1', json={
                    'uuid': 1,
                    'username': 'user1',
                    'group': 'watchers',
                })

                user1 = yield generic_client.users.get(uuid=1)
                self.assertEqual(user1.username, 'user1')

            with responses.RequestsMock() as rsps:
                rsps.add(responses.DELETE, MOCK_API_URL + '/users/1', status=204)

                yield user1.delete()
        threads.deferToThread(f)

    def test_resource_save(self):
        @inlineCallbacks
        def f(*args):
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, MOCK_API_URL + '/users/1', json={
                    'id': 1,
                    'username': 'user1',
                    'group': 'watchers',
                })

                user1 = yield generic_client.users.get(id=1)
                self.assertEqual(user1.username, 'user1')

            with responses.RequestsMock() as rsps:
                rsps.add(responses.PUT, MOCK_API_URL + '/users/1', json={
                    'id': 1,
                    'username': 'user1',
                    'group': 'admins',
                })

                user1.group = 'admins'
                yield user1.save()
        threads.deferToThread(f)

    def test_resource_save_uuid(self):
        @inlineCallbacks
        def f(*args):
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, MOCK_API_URL + '/users/1', json={
                    'uuid': 1,
                    'username': 'user1',
                    'group': 'watchers',
                })

                user1 = yield generic_client.users.get(uuid=1)
                self.assertEqual(user1.username, 'user1')

            with responses.RequestsMock() as rsps:
                rsps.add(responses.PUT, MOCK_API_URL + '/users/1', json={
                    'uuid': 1,
                    'username': 'user1',
                    'group': 'admins',
                })

                user1.group = 'admins'
                yield user1.save()
        threads.deferToThread(f)

    def test_equality(self):
        endpoint = generic_client.users
        res1 = Resource(endpoint, id=1)
        res2 = Resource(endpoint, id=1)
        res3 = Resource(endpoint, id=3)
        res4 = Resource(endpoint, id=1, username='username')

        self.assertEqual(res1, res2)
        self.assertNotEqual(res3, res2)
        with self.assertRaises(AmbiguousComparison):
            res4 == res1

    def test_repr(self):
        endpoint = generic_client.users
        res1 = Resource(endpoint, id=1)

        representation = repr(res1)
        self.assertEqual(representation, '<Resource `users` id: 1>')