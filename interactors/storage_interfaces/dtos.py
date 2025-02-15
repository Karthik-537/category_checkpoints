from dataclasses import dataclass
from typing import Optional, List
from constants.enums import CategoryEntityType, CategoryType, CategoryCheckpointType

@dataclass
class UpdateCategoryCheckPointStatusDTO:
    user_id: str
    entity_id: str
    entity_type: CategoryEntityType
    checked_checkpoint_ids: List[str]
    unchecked_checkpoint_ids: List[str]


@dataclass
class EntityCustomCheckPointDTO:
    entity_id:str
    entity_type: CategoryEntityType
    category_id:str
    text:str


@dataclass
class CategoryCheckpointDTO:
    checkpoint_id: str
    text: str
    category_id: str
    checkpoint_type: CategoryCheckpointType
    entity_id: Optional[str]
    entity_type: Optional[CategoryEntityType]


@dataclass
class EntityCategoryCheckpointDTO:
    checkpoint_id: str
    entity_id: str
    entity_type: CategoryEntityType
    checked_by: str
    is_checked: bool
    order: int
    text: Optional[str]


@dataclass
class UpdateCategoryCheckpointTextDTO:
    checkpoint_id: str
    text: str
    user_id: str
    entity_id: str
    entity_type: CategoryEntityType


@dataclass
class CheckpointResponseDTO:
    category_id: str
    checkpoint_id: str
    text: str
    order: Optional[int]
    is_checked: bool


@dataclass
class CategoryDTO:
    category_id: str
    name: str
    order: int
    category_type: CategoryType
    description: Optional[str]
    parent_category_id: Optional[str]

@dataclass
class CreateEntityCustomCheckpointDTO:
    entity_id: str
    entity_type: CategoryEntityType
    category_id: str
    text: str
