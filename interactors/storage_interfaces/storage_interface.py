from abc import abstractmethod
from typing import List
from interactors.storage_interfaces.dtos import UpdateCategoryCheckPointStatusDTO, CategoryDTO, \
    CategoryCheckpointDTO, EntityCategoryCheckpointDTO
from constants.enums import CategoryEntityType


class StorageInterface:

    @abstractmethod
    def get_valid_category_ids(
            self,
            category_ids: List[str]
    ) -> List[str]:
        pass

    @abstractmethod
    def get_subcategory_ids_for_category_ids(
            self,
            category_ids: List[str]
    ) -> List[str]:
        pass

    @abstractmethod
    def validate_checkpoint_ids(
            self,
            checkpoint_dto: UpdateCategoryCheckPointStatusDTO
    ):
        pass

    @abstractmethod
    def get_entity_checkpoint_ids(
            self,
            entity_id: str,
            entity_type: CategoryEntityType
    ):
        pass

    @abstractmethod
    def update_category_checkpoint_status(
            self,
            entity_id: str,
            entity_type: CategoryEntityType,
            checkpoint_ids: List[str],
            is_checked: bool
    ):
        pass

    @abstractmethod
    def get_categories(
            self,
            category_ids: List[str]
    ) -> List[CategoryDTO]:
        pass

    @abstractmethod
    def create_custom_check_point(
            self,
            category_checkpoint_dto: CategoryCheckpointDTO
    ):
        pass

    @abstractmethod
    def validate_checkpoint_id(
            self,
            checkpoint_id: str
    ):
        pass

    @abstractmethod
    def update_category_check_point_text(
            self,
            checkpoint_id: str,
            text: str
    ):
        pass

    @abstractmethod
    def get_category_checkpoints(
            self,
            entity_id: str,
            entity_type: CategoryEntityType,
            category_ids: List[str]
    ) -> List[CategoryCheckpointDTO]:
        pass

    @abstractmethod
    def get_entity_category_checkpoints(
            self,
            entity_id: str,
            entity_type: CategoryEntityType
    ) -> List[EntityCategoryCheckpointDTO]:
        pass

    @abstractmethod
    def get_valid_checkpoint_ids(
            self,
            checkpoint_ids: List[str]
    ) -> List[str]:
        pass

    @abstractmethod
    def create_entity_custom_checkpoints(
            self,
            entity_checkpoint_dtos: List[EntityCategoryCheckpointDTO]
    ):
        pass

    @abstractmethod
    def get_checkpoints(
            self,
            checkpoint_ids: List[str]
    ) -> List[CategoryCheckpointDTO]:
        pass

    @abstractmethod
    def update_entity_category_checkpoint_text(
            self,
            entity_id: str,
            entity_type: CategoryEntityType,
            checkpoint_id: str,
            text: str
    ):
        pass

    @abstractmethod
    def update_category_checkpoint_text(
            self,
            checkpoint_id: str,
            text: str
    ):
        pass

    @abstractmethod
    def get_entity_custom_checkpoints_max_order(
            self,
            entity_id: str,
            entity_type: CategoryEntityType
    ) -> int:
        pass

    @abstractmethod
    def get_category_type(
            self,
            category_id: str
    ) -> str:
        pass

    @abstractmethod
    def update_category(
            self,
            category_dto: CategoryDTO
    ):
        pass

    @abstractmethod
    def create_category(
            self,
            category_dto: CategoryDTO
    ):
        pass

    @abstractmethod
    def update_category_checkpoints(
            self,
            category_checkpoint_dtos: List[CategoryCheckpointDTO]
    ):
        pass

    @abstractmethod
    def create_category_checkpoints(
            self,
            category_checkpoint_dtos: List[CategoryCheckpointDTO]
    ):
        pass

    @abstractmethod
    def delete_categories(
            self,
            category_ids: List[str]
    ):
        pass

    @abstractmethod
    def delete_checkpoints(
            self,
            checkpoint_ids: List[str]
    ):
        pass
