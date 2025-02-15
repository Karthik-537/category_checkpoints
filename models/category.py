from django.db import models
from constants.utils import generate_uuid4_str


def validate_category_type(value: str):
    from constants.enums import CategoryType

    if value not in CategoryType.get_list_of_values():
        raise Exception(f"Invalid category type: {value}")


def validate_category_checkpoint_type(value: str):
    from constants.enums import CategoryCheckpointType

    if value not in CategoryCheckpointType.get_list_of_values():
        raise Exception(f"Invalid category checkpoint type: {value}")


def validate_category_entity_type(value: str):
    from constants.enums import CategoryEntityType

    if value not in CategoryEntityType.get_list_of_values():
        raise Exception(f"Invalid category checkpoint type: {value}")


class Category(models.Model):
    id = models.CharField(
        max_length=255, primary_key=True, default=generate_uuid4_str
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    parent_category = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True,
        related_name="subcategories"
    )
    order = models.IntegerField()
    category_type = models.CharField(
        max_length=250, validators=[validate_category_type]
    )

    def __str__(self):
        return self.name


class CategoryCheckpoint(models.Model):
    id = models.CharField(
        max_length=255, primary_key=True, default=generate_uuid4_str
    )
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    checkpoint_type = models.CharField(
        max_length=250, validators=[validate_category_checkpoint_type]
    )
    entity_id = models.CharField(max_length=250, null=True, blank=True)
    entity_type = models.CharField(max_length=250, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class EntityCategoryCheckpoint(models.Model):
    id = models.BigAutoField(primary_key=True)
    entity_id = models.CharField(max_length=250)
    entity_type = models.CharField(
        max_length=250, validators=[validate_category_entity_type]
    )
    checkpoint = models.ForeignKey(
        CategoryCheckpoint, on_delete=models.CASCADE
    )
    order = models.IntegerField()
    text = models.TextField(null=True, blank=True)
    checked_by = models.CharField(max_length=255)
    is_checked = models.BooleanField(default=False)

    class Meta:
        unique_together = ["entity_id", "entity_type", "checkpoint"]

