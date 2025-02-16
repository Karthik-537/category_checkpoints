from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.storage_interfaces.dtos import CategoryCheckpointDTO
from interactors.mixins.category_mixin import CategoryMixin
from typing import List


class UpdateOrCreateCategoryCheckPointsInteractor:

    def __init__(
            self,
            storage: StorageInterface
    ):
        self.storage = storage

    @property
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

        self.category_mixin.validate_category_ids(
            category_ids=category_ids,
            storage=self.storage
        )

        valid_ids = self.storage.get_valid_checkpoint_ids(
            checkpoint_ids=checkpoint_ids
        )
        invalid_ids = [_id for _id in checkpoint_ids if _id not in valid_ids]
        valid_dtos = []
        invalid_dtos = []
        if valid_ids:
            for dto in category_checkpoint_dtos:
                if dto.checkpoint_id in valid_ids:
                    valid_dtos.append(dto)
        if invalid_ids:
            for dto in category_checkpoint_dtos:
                if dto.checkpoint_id in invalid_ids:
                    invalid_dtos.append(dto)

        if valid_dtos:
            self.storage.update_category_checkpoints(
                category_checkpoint_dtos=valid_dtos
            )
        if invalid_dtos:
            self.storage.create_category_checkpoints(
                category_checkpoint_dtos=invalid_dtos
            )
