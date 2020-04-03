from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class TaskRequest(models.Model):
    task_id = models.UUIDField()
    creation_date = models.DateTimeField(auto_now_add=True)
    json_task_params = models.TextField(blank=False)
    request_status = models.IntegerField(default=1000,
                                         validators=[MaxValueValidator(1004),
                                                     MaxValueValidator(1000)])
    json_task_result = models.TextField(default='{}')
