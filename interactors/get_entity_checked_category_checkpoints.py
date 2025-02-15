from interactors.storage_interfaces.dtos import CheckpointResponseDTO, CategoryDTO
from typing import List, Tuple
from interactors.get_entity_category_checkpoints import GetEntityCategoryCheckpointsInteractor
from interactors.storage_interfaces.storage_interface import StorageInterface
from constants.enums import CategoryEntityType


class GetEntityCheckedCategoryCheckpointsInteractor:

    def __init__(
            self,
            storage: StorageInterface
    ):
        self.storage = storage

    def get_entity_checked_category_checkpoints(
            self,
            entity_id: str,
            entity_type: CategoryEntityType,
            category_ids: List[str]
    ) -> Tuple[List[CategoryDTO], List[CheckpointResponseDTO]]:
        interactor = GetEntityCategoryCheckpointsInteractor(
            storage=self.storage
        )
        category_dtos, checkpoint_dtos = interactor.get_entity_category_checkpoints(
            entity_id=entity_id,
            entity_type=entity_type,
            category_ids=category_ids
        )
        checkpoint_dtos = [
            dto for dto in checkpoint_dtos if dto.is_checked
        ]

        return category_dtos, checkpoint_dtos
