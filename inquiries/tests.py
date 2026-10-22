from rest_framework import status
from rest_framework.test import APITestCase

from .models import Inquiry


class InquiryAPITests(APITestCase):
    url = "/api/v1/inquiries/"

    def setUp(self):
        self.payload = {
            "name": "Test User",
            "email": "TEST@example.com",
            "company": "Example Ltd",
            "industry": "Technology",
            "message": "I would like to discuss a project.",
        }

    def test_valid_inquiry_is_created(self):
        response = self.client.post(
            self.url, self.payload, format="json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(Inquiry.objects.count(), 1)
        self.assertEqual(
            response.data["email"], "test@example.com"
        )

    def test_invalid_email_is_rejected(self):
        self.payload["email"] = "not-an-email"

        response = self.client.post(
            self.url, self.payload, format="json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertIn("email", response.data)
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_blank_name_is_rejected(self):
        self.payload["name"] = "   "

        response = self.client.post(
            self.url, self.payload, format="json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_blank_message_is_rejected(self):
        self.payload["message"] = "   "

        response = self.client.post(
            self.url, self.payload, format="json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_successful_response_has_no_internal_fields(self):
        response = self.client.post(
            self.url, self.payload, format="json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            set(response.data.keys()),
            {
                "id", "name", "email", "company",
                "industry", "message", "created_at",
            },
        )