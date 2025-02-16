from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.mixins.category_mixin import CategoryMixin
from typing import List


class DeleteCategoriesInteractor:

    def __init__(
            self,
            storage: StorageInterface
    ):
        self.storage = storage

    @property
    def category_mixin(self):
        return CategoryMixin()

    def delete_categories(
            self,
            category_ids: List[str]
    ):
        self.category_mixin.validate_category_ids(
            category_ids=category_ids,
            storage=self.storage
        )

        self.storage.delete_categories(
            category_ids=category_ids
        )
