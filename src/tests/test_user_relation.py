from .base import BaseTestCase
import json, re

class UserRelationTest(BaseTestCase):
    def test_create_3users(self):
        for i in range(3):
            resp = self.app.post(
                '/api/register',
                data={
                    'username': 'No. %d' % (i + 1),
                    'email': 'valid@app.com',
                    'password': 'password'
                }
            )
            self.assert200(resp)

    def test_login_as_user_1(self):
        self.test_create_3users()
        resp = self.app.post(
            '/api/login',
            data={
                'username': 'No. 1',
                'password': 'password'
            }
        )
        self.assert200(resp)
        data = json.loads(resp.get_data())
        assert re.match('\w+' ,data['access_token']) is not None
        assert re.match('\w+' ,data['refresh_token']) is not None
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']

    def test_follow_1_to_2_and_3(self):
        self.test_login_as_user_1()
        resp = self.app.post(
            '/api/following',
            data={
                'id': 2,
            },
            headers={
                "Authorization": "Bearer %s" % self.access_token
            }
        )
        self.assert200(resp)
        resp = self.app.get(
            '/api/following',
            headers={
                "Authorization": "Bearer %s" % self.access_token
            }
        )
        data = json.loads(resp.get_data())
        self.assert200(resp)
        resp = self.app.post(
            '/api/following',
            data={
                'id': 3,
            },
            headers={
                "Authorization": "Bearer %s" % self.access_token
            }
        )
        self.assert200(resp)
        resp = self.app.get(
            '/api/following',
            headers={
                "Authorization": "Bearer %s" % self.access_token
            }
        )
        data = json.loads(resp.get_data())
        print(data)
        self.assert200(resp)
        assert set([user['id'] for user in data['following']]) == {2, 3}
        self.app.post(
            '/api/logout',
            headers={
                "Authorization": "Bearer %s" % self.access_token
            }
        )

    def test_follow_2_to_3(self):
        self.test_follow_1_to_2_and_3()
        resp = self.app.post(
            '/api/login',
            data={
                'username': 'No. 2',
                'password': 'password'
            }
        )
        data = json.loads(resp.get_data())
        print(data)
        self.assert200(resp)
        assert re.match('\w+' ,data['access_token']) is not None
        assert re.match('\w+' ,data['refresh_token']) is not None
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        resp = self.app.get(
            '/api/following',
            headers={
                "Authorization": "Bearer %s" % self.access_token
            }
        )
        data = json.loads(resp.get_data())
        print(data)
        self.assert200(resp)

