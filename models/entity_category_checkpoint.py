from django.db import models
from models.category_checkpoint import CategoryCheckpoint


class EntityCategoryCheckpoint(models.Model):
    PIPELINE_ITEM = "PIPELINE_ITEM"

    ENTITY_TYPES = [
        (PIPELINE_ITEM, "Pipeline Item"),
    ]

    id = models.BigAutoField(primary_key=True)
    entity_id = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPES)
    checkpoint = models.ForeignKey(CategoryCheckpoint, on_delete=models.CASCADE, related_name="entity_checkpoints")
    text = models.TextField(null=True, blank=True)
    checked_by = models.CharField(max_length=255)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"Checkpoint {self.checkpoint_id} - Checked by {self.checked_by}"
