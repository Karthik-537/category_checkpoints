from interactors.storage_interfaces.storage_interface import StorageInterface
from typing import List
from exceptions import custom_exceptions
class CategoryMixin:

    def validate_checkpoint_ids(
            self,
            checkpoint_ids: List[str],
            storage: StorageInterface
    ):

        valid_checkpoint_ids = storage.get_valid_checkpoints(
            checkpoint_ids=checkpoint_ids
        )

        for checkpoint_id in checkpoint_ids:
            if checkpoint_id not in valid_checkpoint_ids:
                raise custom_exceptions.InvalidCheckpointId

    def validate_category_id(
            self,
            category_id: str,
            storage: StorageInterface
    ):
        is_invalid = storage.validate_category_id(
            category_id=category_id
        )
        if is_invalid:
            raise custom_exceptions.InvalidCategoryId


    def validate_checkpoint_id(
            self,
            checkpoint_id: str,
            storage: StorageInterface
    ):
        is_invalid = storage.validate_checkpoint_id(
            checkpoint_id=checkpoint_id
        )
        if is_invalid:
            raise custom_exceptions.InvalidCheckpointId

