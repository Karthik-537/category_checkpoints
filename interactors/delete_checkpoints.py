from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.mixins.category_mixin import CategoryMixin
from typing import List


class DeleteCheckPoints:

    def __init__(
            self,
            storage: StorageInterface
    ):
        self.storage = storage

    def category_mixin(self):
        return CategoryMixin()

    def delete_checkpoints(
            self,
            checkpoint_ids: List[str]
    ):
        self.category_mixin().validate_checkpoint_ids(
            checkpoint_ids=checkpoint_ids,
            storage=self.storage
        )

        self.storage.delete_checkpoints(
            checkpoint_ids=checkpoint_ids
        )