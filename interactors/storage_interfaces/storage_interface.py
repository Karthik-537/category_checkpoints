from abc import abstractmethod
from typing import List
from interactors.storage_interfaces.dtos import UpdateCategoryCheckPointStatusDTO, EntityCustomCheckPointDTO,\
    CategoryDTO, CategoryCheckpointDTO, EntityCategoryCheckpointDTO, UpdateCategoryCheckpointTextDTO


class StorageInterface:

    @abstractmethod
    def get_valid_category_ids(self, category_ids:List[str]):
        pass

    @abstractmethod
    def get_subcategory_ids_for_category_ids(
            self,
            category_ids:List[str]
    ) -> List[str]:
        pass

    @abstractmethod
    def validate_checkpoint_ids(
            self,
            checkpoint_dto:UpdateCategoryCheckPointStatusDTO
    ):
        pass

    @abstractmethod
    def get_checkpoint_ids(
            self,
            entity_id:str,
            entity_type:str
    ):
        pass

    @abstractmethod
    def update_category_checkpoint_status(
            self,
            entity_id: str,
            entity_type: str,
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
    def update_category_check_point_text(self, update_category_check_point_text_dto: UpdateCategoryCheckpointTextDTO):
        pass

    @abstractmethod
    def get_category_checkpoints(
            self,
            entity_id: str,
            entity_type: str,
            category_ids: List[str]
    ) -> List[CategoryCheckpointDTO]:
        pass

    @abstractmethod
    def get_entity_category_checkpoints(
            self,
            entity_id: str,
            entity_type: str
    ) -> List[EntityCategoryCheckpointDTO]:
        pass

    @abstractmethod
    def get_valid_checkpoints(
            self,
            checkpoint_ids: List[str]
    ) -> List[str]:
        pass

    @abstractmethod
    def validate_category_id(
            self,
            category_id: str
    ):
        pass

    @abstractmethod
    def create_entity_custom_checkpoints(
            self,
            entity_checkpoint_dtos: List[EntityCategoryCheckpointDTO]
    ):
        pass