from django.db import models
from models.category import Category


class CategoryCheckpoint(models.Model):
    SYSTEM = "SYSTEM"
    CUSTOM = "CUSTOM"

    CHECKPOINT_TYPES = [
        (SYSTEM, "System"),
        (CUSTOM, "Custom"),
    ]

    id = models.CharField(primary_key=True, default=True)
    text = models.TextField()
    order = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="checkpoints")
    checkpoint_type = models.CharField(max_length=20, choices=CHECKPOINT_TYPES)
    entity_id = models.CharField(max_length=255, null=True, blank=True)
    entity_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.text