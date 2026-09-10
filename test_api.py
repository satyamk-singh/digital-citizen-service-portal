import tempfile
import unittest
from pathlib import Path

import backend.app as portal
from backend.app import app, init_db


class PortalApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        portal.DB_PATH = Path(self.tmp.name) / "portal.db"
        portal.UPLOAD_DIR = Path(self.tmp.name) / "uploads"
        portal.UPLOAD_DIR.mkdir()
        app.config.update(TESTING=True, SECRET_KEY="test-secret")
        init_db()
        self.client = app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def test_health(self):
        self.assertEqual(self.client.get("/api/health").status_code, 200)

    def test_services(self):
        r = self.client.get("/api/services")
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.json["services"]), 1)

    def test_register_login_and_appointment(self):
        r = self.client.post("/api/auth/register", json={"name":"Test Citizen", "email":"test@example.com", "password":"StrongPass123"})
        self.assertEqual(r.status_code, 201)
        r = self.client.post("/api/auth/login", json={"email":"test@example.com", "password":"StrongPass123"})
        self.assertEqual(r.status_code, 200)
        r = self.client.post("/api/appointments", json={"department":"Citizen Service Center", "date":"2026-09-20", "time":"10:00 AM - 10:30 AM"})
        self.assertEqual(r.status_code, 201)

    def test_tracking_demo(self):
        r = self.client.get("/api/applications/track/DCS-2026-001")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json["application"]["application_number"], "DCS-2026-001")


if __name__ == "__main__":
    unittest.main()
