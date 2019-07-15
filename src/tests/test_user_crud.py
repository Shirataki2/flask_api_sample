from .base import BaseTestCase
import json
import re

class UserCRUDTest(BaseTestCase):
    def test_return_404_when_id_is_out_of_range(self):
        resp = self.app.get('/api/user/9999999999999999')
        self.assert_status(resp, 404)

    def test_return_200_when_new_user_created(self):
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

    def test_return_400_when_brank_field_exists(self):
        resp = self.app.post(
            '/api/register',
            data={
                'username': 'example',
            }
        )
        print(resp.get_data())
        self.assert_status(resp, 400)
        data = json.loads(resp.get_data())
        assert data['message'] == {"password": "This field can't be blank"}
        resp = self.app.post(
            '/api/register',
            data={
                'password': 'ex@mp13',
            }
        )
        print(resp.get_data())
        self.assert_status(resp, 400)
        data = json.loads(resp.get_data())
        assert data['message'] == {"username": "This field can't be blank"}

    def test_return_200_when_get_user_no_1(self):
        resp = self.app.post(
            '/api/register',
            data={
                'username': 'example',
                'email': 'valid@app.com',
                'password': 'ex@mp13'
            }
        )
        resp = self.app.get('/api/user/1')
        self.assert_status(resp, 200)
        resp = self.app.get('/api/user/2')
        self.assert_status(resp, 404)

    def test_return_409_if_same_username_register(self):
        resp = self.app.post(
            '/api/register',
            data={
                'username': 'example',
                'email': 'valid@app.com',
                'password': 'ex@mp13'
            }
        )
        data = json.loads(resp.get_data())
        self.assert_status(resp, 200)
        assert data['message'] == 'User example Created!'
        resp = self.app.post(
            '/api/register',
            data={
                'username': 'example',
                'email': 'valid@app.com',
                'password': 'ex@mp13'
            }
        )
        data = json.loads(resp.get_data())
        self.assert_status(resp, 409)
        assert data['message'] == "User Already Exists!"

    def test_return_200_when_valid_login(self):
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

    def test_return_401_when_invalid_login(self):
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
                'email': 'invalid@app.com',
                'password': 'invalid'
            }
        )
        self.assert_status(resp, 401)
        data = json.loads(resp.get_data())
        assert data['message'] == "Invalid Credentials"

    def test_return_401_when_noauth_delete(self):
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
        resp = self.app.delete(
            '/api/user/1'
        )
        self.assert_status(resp, 401)

    def test_return_200_when_auth_delete(self):
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
        resp = self.app.get('/api/user/2')
        self.assert_status(resp, 404)
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
        token = data['access_token']
        resp = self.app.delete(
            '/api/user/1',
            headers={
                "Authorization": "Bearer %s" % token
            }
        )
        print(resp.get_data())
        self.assert_status(resp, 200)
        resp = self.app.get('/api/user/1')
        self.assert_status(resp, 404)

    def test_return_400_when_other_user_token_posted(self):
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
        resp = self.app.post(
            '/api/register',
            data={
                'username': 'example2',
                'email': 'valid@app.com',
                'password': 'ex@mp13'
            }
        )
        self.assert_status(resp, 200)
        resp = self.app.get('/api/user/2')
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
        token = data['access_token']
        resp = self.app.delete(
            '/api/user/2',
            headers={
                "Authorization": "Bearer %s" % token
            }
        )
        self.assert_status(resp, 400)
        resp = self.app.get('/api/user/1')
        self.assert_status(resp, 200)

    def test_return_404_when_delete_same_user_simultanuously(self):
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
        token = data['access_token']
        resp1 = self.app.delete(
            '/api/user/1',
            headers={
                "Authorization": "Bearer %s" % token
            }
        )
        resp2 = self.app.delete(
            '/api/user/1',
            headers={
                "Authorization": "Bearer %s" % token
            }
        )
        assert {resp1.status[:3], resp2.status[:3]} == {'200', '404'}
        resp = self.app.get('/api/user/1')
        self.assert_status(resp, 404)

    def test_return_401_when_post_new_token_before_current_token_expired(self):
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
        token1 = data['access_token']
        rtoken1 = data['refresh_token']
        resp = self.app.post(
            '/api/refresh',
            headers={
                "Authorization": "Bearer %s" % rtoken1
            }
        )
        self.assert_status(resp, 200)
        data = json.loads(resp.get_data())
        token2 = data['access_token']
        resp = self.app.delete(
            '/api/user/1',
            headers={
                "Authorization": "Bearer %s" % token2
            }
        )
        print(resp.get_data())
        self.assert_status(resp, 200)
        resp = self.app.get('/api/user/1')
        self.assert_status(resp, 404)
