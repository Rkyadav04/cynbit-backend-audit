from rest_framework import serializers
from .models import DemoRequest


class DemoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoRequest
        fields = [
            "id",
            "name",
            "work_email",
            "company",
            "product",
            "message",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Name cannot be empty."
            )
        return value

    def validate_work_email(self, value):
        return value.strip().lower()

    def validate_company(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Company cannot be empty."
            )
        return value