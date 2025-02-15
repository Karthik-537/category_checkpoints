from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.storage_interfaces.dtos import UpdateCategoryCheckpointTextDTO
from typing import List
from exceptions import custom_exceptions
from interactors.mixins.category_mixin import CategoryMixin

class UpdateCategoryCheckPointTextInteractor:

    def __init__(self, storage:StorageInterface):

        self.storage = storage

    @property
    def category_mixin(self):
        return CategoryMixin()

    def update_category_check_point_text(self, update_category_check_point_text_dto: UpdateCategoryCheckpointTextDTO ):

        self.storage.check_if_check_point_exists(
            checkpoint_id=update_category_check_point_text_dto.checkpoint_id
        )

        return self.storage.update_category_check_point_text(
            update_category_check_point_text_dto=update_category_check_point_text_dto
        )
