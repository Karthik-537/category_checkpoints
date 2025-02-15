from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.storage_interfaces.dtos import UpdateCategoryCheckPointStatusDTO,\
    EntityCategoryCheckpointDTO
from interactors.mixins.category_mixin import CategoryMixin


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
        update_category_checkpoint_status_dto: UpdateCategoryCheckPointStatusDTO
    ):
        checkpoint_ids = update_category_checkpoint_status_dto.checked_checkpoint_ids + \
                         update_category_checkpoint_status_dto.unchecked_checkpoint_ids

        self.category_mixin.validate_checkpoint_ids(
            storage=self.storage,
            checkpoint_ids=checkpoint_ids
        )
        checkpoint_ids = self.storage.get_checkpoint_ids(
            entity_id=update_category_checkpoint_status_dto.entity_id,
            entity_type=update_category_checkpoint_status_dto.entity_type
        )
        checkpoint_ids_present = []
        entity_checkpoint_dtos_for_ids_not_present = []
        for checkpoint_id in update_category_checkpoint_status_dto.checked_checkpoint_ids:
            if checkpoint_id in checkpoint_ids:
                checkpoint_ids_present.append(checkpoint_id)
            else:
                entity_checkpoint_dtos_for_ids_not_present.append(
                    EntityCategoryCheckpointDTO(
                        entity_id=update_category_checkpoint_status_dto.entity_id,
                        entity_type=update_category_checkpoint_status_dto.entity_type,
                        checked_by=update_category_checkpoint_status_dto.user_id,
                        checkpoint_id=checkpoint_id,
                        is_checked=True,
                        text=None
                    )
                )

        self.storage.update_category_checkpoint_status(
            entity_id=update_category_checkpoint_status_dto.entity_id,
            entity_type=update_category_checkpoint_status_dto.entity_type,
            checkpoint_ids=checkpoint_ids_present,
            is_checked=True
        )

        checkpoint_ids_present = []
        for checkpoint_id in update_category_checkpoint_status_dto.checked_checkpoint_ids:
            if checkpoint_id in checkpoint_ids:
                checkpoint_ids_present.append(checkpoint_id)
            else:
                entity_checkpoint_dtos_for_ids_not_present.append(
                    EntityCategoryCheckpointDTO(
                        entity_id=update_category_checkpoint_status_dto.entity_id,
                        entity_type=update_category_checkpoint_status_dto.entity_type,
                        checked_by=update_category_checkpoint_status_dto.user_id,
                        checkpoint_id=checkpoint_id,
                        is_checked=False,
                        text=None
                    )
                )

        self.storage.update_category_checkpoint_status(
            entity_id=update_category_checkpoint_status_dto.entity_id,
            entity_type=update_category_checkpoint_status_dto.entity_type,
            checkpoint_ids=checkpoint_ids_present,
            is_checked=False
        )

        self.storage.create_entity_custom_checkpoints(
            entity_checkpoint_dtos=entity_checkpoint_dtos_for_ids_not_present
        )


