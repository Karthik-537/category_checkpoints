from django.db import models


class Category(models.Model):
    CATEGORY = "CATEGORY"
    SUB_CATEGORY = "SUB_CATEGORY"

    CATEGORY_TYPES = [
        (CATEGORY, "Category"),
        (SUB_CATEGORY, "Sub Category"),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    parent_category = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories"
    )
    order = models.IntegerField()
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)

    def __str__(self):
        return self.name