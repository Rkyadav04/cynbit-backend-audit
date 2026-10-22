from django.db import models


class DemoRequest(models.Model):
    class Product(models.TextChoices):
        CYNBIT_STUDIO = "cynbit_studio", "Cynbit Studio"
        TENANTEASE = "tenantease", "TenantEase"
        REVIO = "revio", "Revio"

    name = models.CharField(max_length=100)
    work_email = models.EmailField(max_length=254)
    company = models.CharField(max_length=150)
    product = models.CharField(
        max_length=30,
        choices=Product.choices,
    )
    message = models.CharField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demo request #{self.pk}"