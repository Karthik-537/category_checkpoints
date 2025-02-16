from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.storage_interfaces.dtos import CategoryDTO
from interactors.mixins.category_mixin import CategoryMixin
from exceptions import custom_exceptions
from constants.enums import CategoryType


class UpdateOrCreateCategory:

    def __init__(self, storage: StorageInterface):

        self.storage = storage

    @property
    def category_mixin(self):
        return CategoryMixin()

    def update_or_create_category(
            self,
            category_dto: CategoryDTO
    ):
        if category_dto.parent_category_id:
            self._validate_parent_category_id(
                parent_category_id=category_dto.parent_category_id,

            )
            self._validate_parent_category_type(
                parent_category_id=category_dto.parent_category_id
            )

        valid_ids = self.storage.get_valid_category_ids(
            category_ids=[category_dto.category_id]
        )
        if category_dto.category_id in valid_ids:
            self.storage.update_category(
                category_dto=category_dto
            )
        else:
            self.storage.create_category(
                category_dto=category_dto
            )


    def _validate_parent_category_id(
            self,
            parent_category_id: str
    ):
        valid_category_ids = self.storage.get_valid_category_ids(
            category_ids=[parent_category_id]
        )
        if parent_category_id not in valid_category_ids:
            raise custom_exceptions.InvalidParentCategoryId(
                parent_category_id=parent_category_id
            )


    def _validate_parent_category_type(
            self,
            parent_category_id: str
    ):
        category_type = self.storage.get_category_type(
            category_id=parent_category_id
        )

        if category_type == CategoryType.SUB_CATEGORY.value:
            raise custom_exceptions.NotSupportedParentCategoryType(
                parent_category_id=parent_category_id
            )

