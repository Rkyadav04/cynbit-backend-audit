from rest_framework import serializers
from .models import Inquiry


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = [
            "id",
            "name",
            "email",
            "company",
            "industry",
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

    def validate_email(self, value):
        return value.strip().lower()

    def validate_message(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Message cannot be empty."
            )
        return value