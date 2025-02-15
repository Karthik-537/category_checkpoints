from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.storage_interfaces.dtos import CategoryCheckpointDTO, CreateEntityCustomCheckpointDTO
from interactors.mixins.category_mixin import CategoryMixin
from constants.enums import CategoryCheckpointType
import uuid

class CreateEntityCustomCheckPointInteractor:

    def __init__(self, storage:StorageInterface):

        self.storage = storage

    @property
    def category_mixin(self):
        return CategoryMixin()

    def create_entity_custom_checkpoint(
            self,
            entity_custom_checkpoint_dto: CreateEntityCustomCheckpointDTO
    ):
        category_checkpoint_dto = CategoryCheckpointDTO(
            entity_id=entity_custom_checkpoint_dto.entity_id,
            entity_type=entity_custom_checkpoint_dto.entity_type,
            category_id=entity_custom_checkpoint_dto.category_id,
            text=entity_custom_checkpoint_dto.text,
            checkpoint_type=CategoryCheckpointType.CUSTOM,
            checkpoint_id=self._generate_uuid4_str()
        )

        self.category_mixin.validate_category_id(
            category_id=category_checkpoint_dto.category_id,
            storage=self.storage
        )

        return self.storage.create_custom_check_point(
            category_checkpoint_dto=category_checkpoint_dto
        )

    def _generate_uuid4_str() -> str:

        return str(uuid.uuid4())



