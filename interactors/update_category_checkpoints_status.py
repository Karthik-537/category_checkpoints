from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.storage_interfaces.dtos import UpdateCategoryCheckPointStatusDTO,\
    EntityCategoryCheckpointDTO
from interactors.mixins.category_mixin import CategoryMixin
from typing import List


class UpdateCategoryCheckPointsStatusInteractor:
    def __init__(
            self,
            storage: StorageInterface
    ):
        self.storage = storage

    @property
    def category_mixin(self):
        return CategoryMixin()

    def update_category_check_points(
            self,
            params_dto: UpdateCategoryCheckPointStatusDTO
    ):
        all_ids = params_dto.checked_checkpoint_ids + params_dto.unchecked_checkpoint_ids
        self._validate_checkpoint_ids(all_ids)

        existing_ids = self.storage.get_entity_checkpoint_ids(
            entity_id=params_dto.entity_id,
            entity_type=params_dto.entity_type
        )

        max_order = self.storage.get_entity_custom_checkpoints_max_order(
            entity_id=params_dto.entity_id,
            entity_type=params_dto.entity_type
        )

        present_checked, missing_checked, order = self._process_checkpoint_ids(
            params_dto.checked_checkpoint_ids, existing_ids, params_dto, is_checked=True,
            order=max_order
        )
        self.storage.update_category_checkpoint_status(
            entity_id=params_dto.entity_id,
            entity_type=params_dto.entity_type,
            checkpoint_ids=present_checked,
            is_checked=True
        )

        present_unchecked, missing_unchecked, order = self._process_checkpoint_ids(
            params_dto.unchecked_checkpoint_ids, existing_ids, params_dto, is_checked=False,
            order=order
        )
        self.storage.update_category_checkpoint_status(
            entity_id=params_dto.entity_id,
            entity_type=params_dto.entity_type,
            checkpoint_ids=present_unchecked,
            is_checked=False
        )

        all_missing = missing_checked + missing_unchecked
        self.storage.create_entity_custom_checkpoints(entity_checkpoint_dtos=all_missing)

    def _validate_checkpoint_ids(
            self,
            checkpoint_ids: List[str]
    ):
        self.category_mixin.validate_checkpoint_ids(
            storage=self.storage,
            checkpoint_ids=checkpoint_ids
        )

    def _process_checkpoint_ids(
            self,
            checkpoint_ids_list: List[str],
            existing_ids: List[str],
            params_dto: UpdateCategoryCheckPointStatusDTO,
            is_checked: bool,
            order: int
    ) -> (List[str], List[EntityCategoryCheckpointDTO]):
        present_ids = []
        missing_dtos = []
        for checkpoint_id in checkpoint_ids_list:
            if checkpoint_id in existing_ids:
                present_ids.append(checkpoint_id)
            else:
                order+= 1
                missing_dtos.append(
                    EntityCategoryCheckpointDTO(
                        entity_id=params_dto.entity_id,
                        entity_type=params_dto.entity_type,
                        checked_by=params_dto.user_id,
                        checkpoint_id=checkpoint_id,
                        is_checked=is_checked,
                        order=order,
                        text=None
                    )
                )
        return present_ids, missing_dtos, order



