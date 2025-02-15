from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.storage_interfaces.dtos import CategoryCheckpointDTO
from interactors.mixins.category_mixin import CategoryMixin

class CreateEntityCustomCheckPointInteractor:

    def __init__(self, storage:StorageInterface):

        self.storage = storage

    @property
    def category_mixin(self):
        return CategoryMixin()

    def create_entity_custom_checkpoint(
            self, category_checkpoint_dto: CategoryCheckpointDTO
    ):

        self.category_mixin.validate_category_id(
            category_id=category_checkpoint_dto.category_id,
            storage=self.storage
        )

        return self.storage.create_custom_check_point(
            category_checkpoint_dto=category_checkpoint_dto
        )

