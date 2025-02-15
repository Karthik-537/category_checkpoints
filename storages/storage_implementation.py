from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.storage_interfaces.dtos import UpdateCategoryCheckPointDTO
from models.category_checkpoint import CategoryCheckpoint
from models.entity_category_checkpoint import EntityCategoryCheckpoint
from models.category import Category
from typing import List
from django.db.models import Q
from interactors.storage_interfaces.dtos import CategoryDTO, CategoryCheckpointDTO, EntityCategoryCheckpointDTO
from exceptions import custom_exceptions


class StorageImplementation(StorageInterface):

    def validate_checkpoint_ids(self, checkpoint_dto: UpdateCategoryCheckPointDTO):

        checkpoint_ids = checkpoint_dto.checked_checkpoint_ids + checkpoint_dto.unchecked_checkpoint_ids

        for checkpoint_id in checkpoint_dto.checked_checkpoint_ids:
            checkpoint_id_exists = EntityCategoryCheckpoint.objects.filter(id=checkpoint_id).exists()
            checkpoint_id_not_exists = not checkpoint_id_exists
            if checkpoint_id_not_exists:
                EntityCategoryCheckpoint.objects.create(
                    entity_id=checkpoint_dto.entity_id,
                    entity_type=checkpoint_dto.entity_type,
                    user_id=checkpoint_dto.user_id,
                    checkpoint_id=checkpoint_id
                )

        for checkpoint_id in checkpoint_dto.unchecked_checkpoint_ids:
            checkpoint_id_exists = EntityCategoryCheckpoint.objects.filter(id=checkpoint_id).exists()
            checkpoint_id_not_exists = not checkpoint_id_exists
            if checkpoint_id_not_exists:
                EntityCategoryCheckpoint.objects.create(
                    entity_id=checkpoint_dto.entity_id,
                    entity_type=checkpoint_dto.entity_type,
                    user_id=checkpoint_dto.user_id,
                    checkpoint_id=checkpoint_id
                )

    def get_checkpoint_ids(
            self,
            entity_id:str,
            entity_type:str
    ) -> List[str]:

        checkpoint_ids = EntityCategoryCheckpoint.objects.all(
            entity_id=entity_id,
            entity_type=entity_type
        ).values_list("checkpoint_id", flat=True)

        return checkpoint_ids


    def get_valid_category_ids(
            self,
            category_ids: List[str]
    ) -> List[str]:

        category_ids = Category.objects.all().values_list('id', flat=True)

        return category_ids

    def get_subcategory_ids_for_category_ids(
            self,
            category_ids: List[str]
    ) -> List[str]:

        category_ids = Category.objects.filter(parent_category_id__in=category_ids).values_list('id', flat=True)

        return category_ids

    def get_categories(
            self,
            category_ids: List[str]
    ) -> List[CategoryDTO]:
        category_dtos = []

        categories = Category.objects.filter(id__in=category_ids)
        for category in categories:
            category_dto = self._convert_category_object_to_dto(category=category)

            category_dtos.append(category_dto)

        return category_dtos

    @staticmethod
    def _convert_category_object_to_dto(category):

        return CategoryDTO(
            category_id=category.id,
            name=category.name,
            order=category.order,
            category_type=category.category_type,
            description=category.description,
            parent_category_id=category.parent_category
        )

    def get_category_checkpoints(
            self,
            entity_id: str,
            entity_type: str,
            category_ids: List[str]
    ) -> List[CategoryCheckpointDTO]:

        checkpoint_dtos = []
        checkpoints = CategoryCheckpoint.objects.filter(
            Q(
                category_id__in=category_ids
            ) & (
                    Q(
                        checkpoint_type="SYSTEM"
                    ) | Q(
                entity_id=entity_id,
                entity_type=entity_type,
                checkpoint_type="CUSTOM"
            )
            )
        )
        for checkpoint in checkpoints:
            checkpoint_dto = self._convert_category_checkpoint_object_to_dto(
                checkpoint=checkpoint
            )
            checkpoint_dtos.append(checkpoint_dto)

        return checkpoint_dtos

    @staticmethod
    def _convert_category_checkpoint_object_to_dto(checkpoint):

        return CategoryCheckpointDTO(
            checkpoint_id=checkpoint.id,
            text=checkpoint.text,
            order=checkpoint.order,
            category_id=checkpoint.category_id,
            checkpoint_type=checkpoint.checkpoint_type,
            entity_id=checkpoint.entity_id,
            entity_type=checkpoint.entity_type
        )

    def get_entity_category_checkpoints(
            self,
            entity_id: str,
            entity_type: str
    ) -> List[EntityCategoryCheckpointDTO]:

        checkpoint_dtos = []

        checkpoints = EntityCategoryCheckpoint.objects.filter(
            entity_id=entity_id, entity_type=entity_type
        )

        for checkpoint in checkpoints:
            checkpoint_dto = self._convert_entity_category_checkpoint_object_to_dto(
                checkpoint=checkpoint
            )
            checkpoint_dtos.append(checkpoint_dto)

        return checkpoint_dtos

    @staticmethod
    def _convert_entity_category_checkpoint_object_to_dto(checkpoint):

        return EntityCategoryCheckpointDTO(
            checkpoint_id=checkpoint.checkpoint_id,
            text=checkpoint.text,
            is_checked=checkpoint.is_checked,
            entity_id=checkpoint.entity_id,
            entity_type=checkpoint.entity_type
        )

    def get_valid_checkpoints(
            self,
            checkpoint_ids: List[str]
    ) -> List[str]:

        checkpoint_ids = CategoryCheckpoint.objects.all().values_list('id', flat=True)
        return checkpoint_ids

    def validate_category_id(
            self,
            category_id: str
    ):
        category_id_exists = Category.objects.filter(id=category_id).exists()
        category_id_not_exists = not category_id_exists
        if category_id_not_exists:
            return True
        else:
            return False

    def update_category_checkpoint_status(
            self,
            entity_id: str,
            entity_type: str,
            checkpoint_ids: List[str],
            is_checked: bool
    ):
        EntityCategoryCheckpoint.objects.filter(
            entity_id=entity_id,
            entity_type=entity_type,
            checkpoint_id__in=checkpoint_ids,
        ).update(is_checked=is_checked)

    def create_entity_custom_checkpoints(
            self,
            entity_checkpoint_dtos: List[EntityCategoryCheckpointDTO]
    ):
        new_entities = [
            EntityCategoryCheckpoint(
                entity_id=dto.entity_id,
                entity_type=dto.entity_type,
                user_id=dto.checked_by,
                checkpoint_id=dto.checkpoint_id,
                is_checked=dto.is_checked,
                text=dto.text
            )
            for dto in entity_checkpoint_dtos
        ]

        EntityCategoryCheckpoint.objects.bulk_create(new_entities)

    def create_custom_check_point(
            self,
            category_checkpoint_dto: CategoryCheckpointDTO
    ):
        CategoryCheckpoint.objects.create(
            category_checkpoint_dto.text,
            category_checkpoint_dto.entity_id,
            category_checkpoint_dto.entity_type,
            category_checkpoint_dto.checkpoint_type,
            category_checkpoint_dto.category_id,
            category_checkpoint_dto.order
        )

        return category_checkpoint_dto

    def validate_checkpoint_id(
            self,
            checkpoint_id: str
    ):
        category_id_exists = CategoryCheckpoint.objects.filter(id=checkpoint_id).exists()
        category_id_not_exists = not category_id_exists
        if category_id_not_exists:
            return True
        else:
            return False


