from typing import List, Tuple, Dict
import re
from exceptions import custom_exceptions
from interactors.storage_interfaces.dtos import CategoryDTO, CategoryCheckpointDTO, EntityCategoryCheckpointDTO, \
    CheckpointResponseDTO
from interactors.storage_interfaces.storage_interface import StorageInterface
from constants.enums import CategoryEntityType


class GetEntityCategoryCheckpointsInteractor:
    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_entity_category_checkpoints(
            self,
            entity_id: str,
            entity_type: CategoryEntityType,
            category_ids: List[str]
    ) -> Tuple[List[CategoryDTO], List[CheckpointResponseDTO]]:
        self._validate_category_ids(
            category_ids=category_ids
        )

        subcategory_ids = self.storage.get_subcategory_ids_for_category_ids(
            category_ids=category_ids
        )
        category_ids = category_ids + subcategory_ids

        category_dtos = self.storage.get_categories(
            category_ids=category_ids
        )
        category_checkpoint_dtos = self.storage.get_category_checkpoints(
            entity_id=entity_id,
            entity_type=entity_type,
            category_ids=category_ids
        )
        entity_checkpoint_dtos = self.storage.get_entity_category_checkpoints(
            entity_id=entity_id,
            entity_type=entity_type
        )

        checkpoint_response_dtos = self._prepare_checkpoint_response_dtos(
            category_checkpoint_dtos=category_checkpoint_dtos,
            entity_checkpoint_dtos=entity_checkpoint_dtos
        )

        placeholder_data = self._get_placeholder_data(
            entity_id=entity_id
        )
        checkpoint_response_dtos = self._formatted_checkpoint_dtos(
            checkpoint_dtos=checkpoint_response_dtos,
            placeholder_data=placeholder_data
        )

        return category_dtos, checkpoint_response_dtos

    def _validate_category_ids(
            self,
            category_ids: List[str]
    ):
        valid_category_ids = self.storage.get_valid_category_ids(category_ids=category_ids)

        invalid_ids = [_id for _id in category_ids if _id not in valid_category_ids]
        if invalid_ids:
            raise custom_exceptions.InvalidCategoryId

    @staticmethod
    def _prepare_checkpoint_response_dtos(
            category_checkpoint_dtos: List[CategoryCheckpointDTO],
            entity_checkpoint_dtos: List[EntityCategoryCheckpointDTO]
    ) -> List[CheckpointResponseDTO]:

        entity_checkpoint_map = {cp.checkpoint_id: cp for cp in entity_checkpoint_dtos}

        updated_checkpoints_dtos = []
        for cat_cp in category_checkpoint_dtos:
            entity_checkpoint_dto = entity_checkpoint_map.get(cat_cp.checkpoint_id)
            if entity_checkpoint_dto:
                entity_cp = entity_checkpoint_map[cat_cp.checkpoint_id]
                new_text = entity_cp.text if entity_cp.text is not None else cat_cp.text
                updated_cp = CheckpointResponseDTO(
                    checkpoint_id=cat_cp.checkpoint_id,
                    text=new_text,
                    order=entity_cp.order,
                    category_id=cat_cp.category_id,
                    is_checked=entity_cp.is_checked
                )
                updated_checkpoints_dtos.append(updated_cp)
            else:
                updated_cp = CheckpointResponseDTO(
                    checkpoint_id=cat_cp.checkpoint_id,
                    text=cat_cp.text,
                    category_id=cat_cp.category_id,
                    is_checked=False,
                    order=None
                )
                updated_checkpoints_dtos.append(updated_cp)

        return updated_checkpoints_dtos

    def _get_placeholder_data(
            self,
            entity_id: str
    ) -> Dict:
        pass

    @staticmethod
    def _format_checkpoint_text(
            checkpoint_text: str,
            variables: Dict
    ) -> str:

        def replacer(match):
            key = match.group(1).strip()
            value = variables.get(key, "")
            if value:
                return f"**{{{value}}}**"
            else:
                return ""

        return re.sub(r'<<([^<>]+)>>', replacer, checkpoint_text)

    def _formatted_checkpoint_dtos(
            self,
            checkpoint_dtos: List[CheckpointResponseDTO],
            placeholder_data: Dict
    ) -> List[CheckpointResponseDTO]:

        for checkpoint_dto in checkpoint_dtos:
            checkpoint_text = checkpoint_dto.text
            formatted_text = self._format_checkpoint_text(
                checkpoint_text=checkpoint_text,
                variables=placeholder_data
            )
            checkpoint_dto.text = formatted_text

        return checkpoint_dtos





