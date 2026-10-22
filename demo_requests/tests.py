from rest_framework import status
from rest_framework.test import APITestCase

from .models import DemoRequest


class DemoRequestAPITests(APITestCase):
    url = "/api/v1/demo-requests/"

    def setUp(self):
        self.payload = {
            "name": "Test User",
            "work_email": "TEST@example.com",
            "company": "Example Ltd",
            "product": "cynbit_studio",
            "message": "I would like a product demo.",
        }

    def test_valid_demo_request_is_created(self):
        response = self.client.post(
            self.url, self.payload, format="json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(DemoRequest.objects.count(), 1)
        self.assertEqual(
            response.data["work_email"], "test@example.com"
        )

    def test_invalid_email_is_rejected(self):
        self.payload["work_email"] = "invalid-email"

        response = self.client.post(
            self.url, self.payload, format="json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(DemoRequest.objects.count(), 0)

    def test_invalid_product_is_rejected(self):
        self.payload["product"] = "unknown_product"

        response = self.client.post(
            self.url, self.payload, format="json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_blank_company_is_rejected(self):
        self.payload["company"] = "   "

        response = self.client.post(
            self.url, self.payload, format="json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_internal_fields_are_not_exposed(self):
        response = self.client.post(
            self.url, self.payload, format="json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            set(response.data.keys()),
            {
                "id",
                "name",
                "work_email",
                "company",
                "product",
                "message",
                "created_at",
            },
        )