from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.mixins.category_mixin import CategoryMixin
from constants.enums import CategoryEntityType
from typing import List


class ReorderEntityCheckpointsInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    @property
    def category_mixin(self):
        return CategoryMixin()

    def reorder_entity_checkpoints(
            self, entity_id: str,
            entity_type: CategoryEntityType,
            checkpoint_ids: List[str]
    ):
        self.category_mixin.validate_checkpoint_ids(
            checkpoint_ids=checkpoint_ids,
            storage=self.storage
        )

        valid_entity_checkpoint_ids = self.storage.get_entity_checkpoint_ids(
            entity_id=entity_id,
            entity_type=entity_type
        )

        checkpoint_ids = [
            _id for _id in checkpoint_ids
            if _id in valid_entity_checkpoint_ids
        ]

        self.storage.reorder_entity_checkpoints(
            entity_id=entity_id,
            entity_type=entity_type,
            checkpoint_ids=checkpoint_ids
        )
