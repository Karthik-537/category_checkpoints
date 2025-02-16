from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.mixins.category_mixin import CategoryMixin
from typing import List


class DeleteCheckPointsInteractor:

    def __init__(
            self,
            storage: StorageInterface
    ):
        self.storage = storage

    @property
    def category_mixin(self):
        return CategoryMixin()

    def delete_checkpoints(
            self,
            checkpoint_ids: List[str]
    ):
        self.category_mixin.validate_checkpoint_ids(
            checkpoint_ids=checkpoint_ids,
            storage=self.storage
        )

        self.storage.delete_checkpoints(
            checkpoint_ids=checkpoint_ids
        )
