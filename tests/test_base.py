from flask_testing import TestCase
from flask import current_app, url_for
from main import app


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        return app
    
    # Test the app exists
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    # Test the app is in test mode 
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    # Test index route redirect to hello route
    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response, url_for('hello'))

    # Test hello route return 200
    def test_hello_get(self):
        response = self.client.get(url_for('hello'))
        self.assert200(response)

    # Test user login post
    def test_auth_login_post(self):
        fake_form = {
            'username': 'Fake user',
            'password': '1234',
        }

        response = self.client.post(url_for('hello'), data=fake_form)
        self.assertRedirects(response, url_for('index'))