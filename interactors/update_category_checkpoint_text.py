from interactors.mixins.category_mixin import CategoryMixin
from interactors.storage_interfaces.dtos import UpdateCategoryCheckpointTextDTO
from interactors.storage_interfaces.storage_interface import StorageInterface
from constants.enums import CategoryCheckpointType

class UpdateCategoryCheckPointTextInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    @property
    def category_mixin(self):
        return CategoryMixin()

    def update_category_check_point_text(
            self,
            update_category_checkpoint_text_dto: UpdateCategoryCheckpointTextDTO
    ):

        self.category_mixin.validate_checkpoint_id(
            checkpoint_id=update_category_checkpoint_text_dto.checkpoint_id,
            storage=self.storage
        )

        checkpoint_dtos = self.storage.get_checkpoints(
            checkpoint_ids=[update_category_checkpoint_text_dto.checkpoint_id]
        )
        checkpoint_dto = checkpoint_dtos[0]

        if checkpoint_dto.checkpoint_type == CategoryCheckpointType.CUSTOM.value:
            self.storage.update_category_checkpoint_text(
                checkpoint_id=update_category_checkpoint_text_dto.checkpoint_id,
                text=update_category_checkpoint_text_dto.text
            )
        else:
            self.storage.update_entity_category_checkpoint_text(
                entity_id=update_category_checkpoint_text_dto.entity_id,
                entity_type=update_category_checkpoint_text_dto.entity_type,
                checkpoint_id=update_category_checkpoint_text_dto.checkpoint_id,
                text=update_category_checkpoint_text_dto.text
            )
