from django.db import models


class Result(models.Model):
    session_id = models.CharField(primary_key=True, max_length=30)
    json_result = models.TextField(blank=True)