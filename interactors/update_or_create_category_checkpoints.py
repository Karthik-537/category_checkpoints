from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.storage_interfaces.dtos import CategoryCheckpointDTO
from interactors.mixins.category_mixin import CategoryMixin
from typing import List


class UpdateOrCreateCategoryCheckPoints:

    def __init__(
            self,
            storage: StorageInterface
    ):
        self.storage = storage

    def category_mixin(self):
        return CategoryMixin()

    def update_or_create_category_checkpoints(
            self,
            category_checkpoint_dtos: List[CategoryCheckpointDTO]
    ):
        category_ids = []
        checkpoint_ids = []
        for dto in category_checkpoint_dtos:
            category_ids.append(dto.category_id)
            checkpoint_ids.append(dto.checkpoint_id)

        self.category_mixin().validate_category_ids(
            category_ids=category_ids,
            storage=self.storage
        )

        valid_ids = self.storage.get_valid_checkpoints(
            checkpoint_ids=checkpoint_ids
        )
        invalid_ids = [_id for _id in checkpoint_ids if _id not in valid_ids]
        if valid_ids:
            self.storage.update_category_checkpoints(
                checkpoint_ids=valid_ids,
                category_checkpoint_dtos=category_checkpoint_dtos
            )
        if invalid_ids:
            self.storage.create_category_checkpoints(
                checkpoint_ids=invalid_ids,
                category_checkpoint_dtos=category_checkpoint_dtos
            )



