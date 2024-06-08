import unittest
from app import create_app, db
from app.models import SecurityEvent

class SecurityEventTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.client = self.app.test_client()
        with self.app.app_contxt():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_log_events(self):
        response = self.client.post('/events', json={'event_type': 'login', 'description': 'User logged in'})
        self.assertEqual(response.status_code, 201)

    def test_get_events(self):
        response = self.client.get('/events')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()