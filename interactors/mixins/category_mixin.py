from interactors.storage_interfaces.storage_interface import StorageInterface
from typing import List
from exceptions import custom_exceptions


class CategoryMixin:

    @staticmethod
    def validate_checkpoint_ids(
            checkpoint_ids: List[str],
            storage: StorageInterface
    ):

        valid_checkpoint_ids = storage.get_valid_checkpoint_ids(
            checkpoint_ids=checkpoint_ids
        )
        invalid_ids = [_id for _id in checkpoint_ids if _id not in valid_checkpoint_ids]

        if invalid_ids:
            raise custom_exceptions.InvalidCheckpointId(
                invalid_ids=invalid_ids
            )

    @staticmethod
    def validate_category_id(
            category_id: str,
            storage: StorageInterface
    ):
        valid_category_ids = storage.get_valid_category_ids(
            category_ids=[category_id]
        )
        if category_id not in valid_category_ids:
            raise custom_exceptions.InvalidCategoryId(
                invalid_ids=[category_id]
            )

    @staticmethod
    def validate_checkpoint_id(
            checkpoint_id: str,
            storage: StorageInterface
    ):
        valid_checkpoint_ids = storage.get_valid_checkpoint_ids(
            checkpoint_ids=[checkpoint_id]
        )

        if checkpoint_id not in valid_checkpoint_ids:
            raise custom_exceptions.InvalidCheckpointId(
                invalid_ids=[checkpoint_id]
            )

    @staticmethod
    def validate_category_ids(
            category_ids: List[str],
            storage: StorageInterface
    ):
        valid_category_ids = storage.get_valid_category_ids(
            category_ids=category_ids
        )
        invalid_ids = [_id for _id in category_ids if _id not in valid_category_ids]

        if invalid_ids:
            custom_exceptions.InvalidCategoryId(
                invalid_ids=invalid_ids
            )
