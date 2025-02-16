from interactors.storage_interfaces.storage_interface import StorageInterface
from models.category import Category, CategoryCheckpoint, EntityCategoryCheckpoint
from typing import List
from django.db.models import Q, Max
from interactors.storage_interfaces.dtos import CategoryDTO, CategoryCheckpointDTO, EntityCategoryCheckpointDTO
from constants.enums import CategoryEntityType, CategoryCheckpointType


class StorageImplementation(StorageInterface):

    def get_entity_checkpoint_ids(
            self,
            entity_id: str,
            entity_type: CategoryEntityType
    ) -> List[str]:
        checkpoint_ids = EntityCategoryCheckpoint.objects.filter(
            entity_id=entity_id,
            entity_type=entity_type
        ).values_list("checkpoint_id", flat=True)

        return checkpoint_ids

    def get_valid_category_ids(
            self,
            category_ids: List[str]
    ) -> List[str]:

        category_ids = list(
            Category.objects.filter(
                id__in=category_ids
            ).values_list('id', flat=True)
        )

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
            entity_type: CategoryEntityType,
            category_ids: List[str]
    ) -> List[CategoryCheckpointDTO]:

        checkpoint_dtos = []
        checkpoints = CategoryCheckpoint.objects.filter(
            Q(
                category_id__in=category_ids
            ) & (
                    Q(
                        checkpoint_type=CategoryCheckpointType.SYSTEM
                    ) | Q(
                            entity_id=entity_id,
                            entity_type=entity_type,
                            checkpoint_type=CategoryCheckpointType.CUSTOM
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
            category_id=checkpoint.category_id,
            checkpoint_type=checkpoint.checkpoint_type,
            entity_id=checkpoint.entity_id,
            entity_type=checkpoint.entity_type
        )

    def get_entity_category_checkpoints(
            self,
            entity_id: str,
            entity_type: CategoryEntityType
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
            entity_type=checkpoint.entity_type,
            order=checkpoint.order,
            checked_by=checkpoint.checked_by
        )

    def get_valid_checkpoint_ids(
            self,
            checkpoint_ids: List[str]
    ) -> List[str]:

        checkpoint_ids = list(
            CategoryCheckpoint.objects.filter(
                id__in=checkpoint_ids
            ).values_list('id', flat=True)
        )
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
            entity_type: CategoryEntityType,
            checkpoint_ids: List[str],
            is_checked: bool
    ):
        objs = EntityCategoryCheckpoint.objects.filter(
            entity_id=entity_id,
            entity_type=entity_type,
            checkpoint_id__in=checkpoint_ids,
        )
        for obj in objs:
            obj.is_checked = is_checked

        EntityCategoryCheckpoint.objects.bulk_update(objs)

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
                order=dto.order,
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
            id=category_checkpoint_dto.checkpoint_id,
            text=category_checkpoint_dto.text,
            entity_id=category_checkpoint_dto.entity_id,
            entity_type=category_checkpoint_dto.entity_type,
            checkpoint_type=category_checkpoint_dto.checkpoint_type,
            category_id=category_checkpoint_dto.category_id
        )

        return category_checkpoint_dto

    def validate_checkpoint_id(
            self,
            checkpoint_id: str
    ):
        checkpoint_id_exists = CategoryCheckpoint.objects.filter(id=checkpoint_id).exists()
        checkpoint_id_not_exists = not checkpoint_id_exists
        if checkpoint_id_not_exists:
            return True
        else:
            return False

    def get_checkpoints(
            self,
            checkpoint_ids: List[str]
    ) -> List[CategoryCheckpointDTO]:

        checkpoint_dtos = []
        checkpoints = CategoryCheckpoint.objects.filter(id__in=checkpoint_ids)
        for checkpoint in checkpoints:
            checkpoint_dto = self._convert_category_checkpoint_object_to_dto(
                checkpoint=checkpoint
            )
            checkpoint_dtos.append(checkpoint_dto)

        return checkpoint_dtos

    def update_category_checkpoint_text(
            self,
            checkpoint_id: str,
            text: str
    ):
        checkpoint = CategoryCheckpoint.objects.filter(
            id=checkpoint_id
        ).first()
        if not checkpoint:
            return

        checkpoint.text = text
        checkpoint.save()

    def update_entity_category_checkpoint_text(
        self,
        entity_id: str,
        entity_type: CategoryEntityType,
        checkpoint_id: str,
        text: str
    ):
        checkpoint = EntityCategoryCheckpoint.objects.filter(
            entity_id=entity_id,
            entity_type=entity_type,
            checkpoint_id=checkpoint_id
        ).first()
        if not checkpoint:
            return

        checkpoint.text = text
        checkpoint.save()

    def get_max_order_for_entity_custom_checkpoint(
            self,
            entity_id: str,
            entity_type: CategoryEntityType
    ) -> int:

        max_order_dict = EntityCategoryCheckpoint.objects.filter(
            entity_id=entity_id,
            entity_type=entity_type
        ).aggregate(max_order=Max("order"))

        max_order = max_order_dict["max_order"]

        if max_order:
            return max_order
        else:
            return 0

    def get_category_type(
            self,
            category_id: str
    ) -> str:

        category = Category.objects.get(
            id=category_id
        )

        return category.category_type

    def update_category(
            self,
            category_dto: CategoryDTO
    ):
        category = Category.objects.filter(
            id=category_dto.category_id
        )
        if not category:
            return

        category.category_type = category_dto.category_type
        category.parent_category_id = category_dto.parent_category_id
        category.order = category_dto.order
        category.name = category_dto.name
        category.description = category_dto.description

        category.save()

    def create_category(
            self,
            category_dto: CategoryDTO
    ):
        Category.objects.create(
            id=category_dto.category_id,
            name=category_dto.name,
            order=category_dto.order,
            parent_category_id=category_dto.parent_category_id,
            category_type=category_dto.category_type,
            description=category_dto.description
        )

    def update_category_checkpoints(
            self,
            checkpoint_ids: List[str],
            category_checkpoint_dtos: List[CategoryCheckpointDTO]
    ):
        checkpoints = list(CategoryCheckpoint.objects.filter(id__in=checkpoint_ids))

        dto_map = {dto.checkpoint_id: dto for dto in category_checkpoint_dtos}

        for cp in checkpoints:
            dto = dto_map.get(cp.id)
            if dto:
                cp.text = dto.text
                cp.category_id = dto.category_id
                cp.checkpoint_type = dto.checkpoint_type
                cp.entity_id = dto.entity_id
                cp.entity_type = dto.entity_type

        CategoryCheckpoint.objects.bulk_update(checkpoints)


    def create_category_checkpoints(
            self,
            checkpoint_ids: List[str],
            category_checkpoint_dtos: List[CategoryCheckpointDTO]
    ):
        checkpoints = []
        for dto in category_checkpoint_dtos:
            if dto.checkpoint_id in checkpoint_ids:
                checkpoints.append(
                    CategoryCheckpoint(
                        id=dto.checkpoint_id,
                        text=dto.text,
                        checkpoint_type=dto.checkpoint_type,
                        category_id=dto.category_id,
                        entity_id=dto.entity_id,
                        entity_type=dto.entity_type
                    )
                )

        CategoryCheckpoint.objects.bulk_create(checkpoints)

    def delete_categories(
            self,
            category_ids: List[str]
    ):
        Category.objects.filter(id__in=category_ids).delete()

    def delete_checkpoints(
            self,
            checkpoint_ids: List[str]
    ):
        CategoryCheckpoint.objects.filter(id__in=checkpoint_ids).delete()








