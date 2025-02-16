from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.storage_interfaces.dtos import CategoryDTO
from interactors.mixins.category_mixin import CategoryMixin


class UpdateOrCreateCategories:

    def __init__(self, storage: StorageInterface):

        self.storage = storage

    @property
    def category_mixin(self):
        return CategoryMixin()

    def update_or_create_categories(
            self,
            category_dto: CategoryDTO
    ):
        if category_dto.parent_category_id:
            self.category_mixin.validate_category_id(
                category_id=category_dto.parent_category_id)

