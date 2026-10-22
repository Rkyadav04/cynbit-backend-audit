from django.db import models


class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    company = models.CharField(max_length=150, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    message = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry #{self.pk}"