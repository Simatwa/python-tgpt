import unittest
from fastapi.testclient import TestClient
from fastapi import status
from pytgpt.api import app


class TestV1(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app, headers={"accept": "application/json"})

    def test_home_redirect_to_docs(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_server_status(self):
        """Server is running"""
        resp = self.client.get("/status")
        self.assertTrue(resp.json().get("is_alive"))

    def test_chat_providers(self):
        """Check supported providers"""
        resp = self.client.get("/v1/chat/providers")
        self.assertEqual(len(resp.json()), 2)

    def test_text_no_stream(self):
        """Non-streaming response"""
        resp = self.client.post(
            "/v1/chat/nostream",
            json={
                "prompt": "Hello there",
                "provider": "phind",
                "whole": False,
                "max_tokens": 600,
                "timeout": 30,
                "proxy": None,
            },
        )
        self.assertIn("text", resp.json())

    def test_text_no_tream_whole(self):
        """Raw body returned"""
        resp = self.client.post(
            "/v1/chat/nostream",
            json={
                "prompt": "Hello there",
                "provider": "phind",
                "whole": True,
                "max_tokens": 600,
                "timeout": 30,
                "proxy": None,
            },
        )
        resp_dict = resp.json()
        self.assertIsNotNone(resp_dict["text"])
        self.assertIsInstance(resp_dict["body"], dict)

    def test_text_stream(self):
        """Streaming response"""
        resp = self.client.post(
            "/v1/chat/stream",
            json={
                "prompt": "Hello there",
                "provider": "phind",
                "whole": False,
                "max_tokens": 600,
                "timeout": 30,
                "proxy": None,
            },
        )
        self.assertTrue(resp.is_success)

    def test_prompt_to_image_post(self):
        resp = self.client.post(
            "/v1/image",
            json={
                "prompt": "Developed Nairobi in 3050",
                "amount": 2,
                "proxy": None,
                "timeout": 30,
            },
        )
        resp_dict = resp.json()
        self.assertIsNotNone(resp_dict.get("urls"))
        self.assertEqual(len(resp_dict["urls"]), 2)

    def test_prompt_to_image_bytes_post(self):
        resp = self.client.post(
            "/v1/image/bytes", json={"prompt": "Jay Z performing", "timeout": 30}
        )
        self.assertIsNotNone(resp.headers.get("Content-Disposition"))

    def test_prompt_to_image_bytes_get(self):
        resp = self.client.get(
            "/v1/image/bytes", params={"prompt": "Jay Z performing", "timeout": 30}
        )
        self.assertIsNotNone(resp.headers.get("Content-Disposition"))

    def test_prompt_to_image_bytes_get_redirect(self):
        resp = self.client.get(
            "/v1/image/bytes",
            params={
                "prompt": "Jay Z performing",
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
