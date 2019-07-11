from .base import BaseTestCase
import json
import re

class PostCRUDTest(BaseTestCase):
    def test_return_200_when_valid_login(self):
        import re
        resp = self.app.post(
            '/api/register',
            data={
                'username': 'example',
                'email': 'valid@app.com',
                'password': 'ex@mp13'
            }
        )
        self.assert_status(resp, 200)
        resp = self.app.get('/api/user/1')
        self.assert_status(resp, 200)
        resp = self.app.post(
            '/api/login',
            data={
                'username': 'example',
                'email': 'valid@app.com',
                'password': 'ex@mp13'
            }
        )
        self.assert_status(resp, 200)
        data = json.loads(resp.get_data())
        assert re.match('\w+' ,data['access_token']) is not None
        assert re.match('\w+' ,data['refresh_token']) is not None
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']

    def test_return_404_invalid_post_url(self):
        resp = self.app.post(
            '/api/register',
            data={
                'username': 'example',
                'email': 'valid@app.com',
                'password': 'ex@mp13'
            }
        )
        print(resp.get_data())
        self.assert_status(resp, 200)
        data = json.loads(resp.get_data())
        assert data['message'] == 'User example Created!'
        resp = self.app.get('/api/user/1/post/999999999999999999')
        print(resp.get_data())
        data = json.loads(resp.get_data())
        self.assert_status(resp, 404)
        assert data['message'] == 'Post not Found'

    def test_return_200_when_new_post_form_is_correct(self):
        self.test_return_200_when_valid_login()
        resp = self.app.post(
            '/api/submit',
            data={
                'text': 'これはサンプルテキストだよ',
            },
            headers={
                "Authorization": "Bearer %s" % self.access_token
            }
        )
        data = json.loads(resp.get_data())
        self.post_id = data['content']['id']
        self.assert_status(resp, 200)

    def test_return_401_when_submited_new_post_if_token_is_invalid(self):
        self.test_return_200_when_valid_login()
        resp = self.app.post(
            '/api/submit',
            data={
                'text': 'これはサンプルテキストだよ',
            }
        )
        self.assert_status(resp, 401)

    def test_return_200_when_get_valid_submited_post(self):
        self.test_return_200_when_new_post_form_is_correct()
        resp = self.app.get(
            '/api/user/1/post/%s' % self.post_id
        )
        self.assert_status(resp, 200)
        data = json.loads(resp.get_data())
        print(data)        
        assert data['text'] == 'これはサンプルテキストだよ'
        assert data['user_id'] == 1
        assert data['id'] == self.post_id

    def test_return_200_when_valid_auth_delete(self):
        self.test_return_200_when_valid_login()
        for i in range(10):
            resp = self.app.post(
                '/api/submit',
                data={
                    'text': 'これはサンプルテキストだよ',
                },
                headers={
                    "Authorization": "Bearer %s" % self.access_token
                }
            )
            self.assert_status(resp, 200)
        resp = self.app.delete(
            '/api/user/1/post/4',
            headers={
                "Authorization": "Bearer %s" % self.access_token
            }
        )
        self.assert_status(resp, 200)
        resp = self.app.get('/api/user/1/post/4')
        self.assert_status(resp, 404)
        resp = self.app.delete(
            '/api/user/1/post/4',
            headers={
                "Authorization": "Bearer %s" % self.access_token
            }
        )
        self.assert_status(resp, 404)
        resp = self.app.delete(
            '/api/user/1/post/999',
            headers={
                "Authorization": "Bearer %s" % self.access_token
            }
        )
        self.assert_status(resp, 404)
        resp = self.app.delete(
            '/api/user/1/post/5'
        )
        self.assert_status(resp, 401)
        resp = self.app.delete(
            '/api/user/2/post/3',
            headers={
                "Authorization": "Bearer %s" % self.access_token
            }
        )
        self.assert_status(resp, 400)
