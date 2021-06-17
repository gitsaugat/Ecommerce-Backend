from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CustomerSupportToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=400, null=False, blank=False)

    def __str__(self) -> str:
        return self.token
