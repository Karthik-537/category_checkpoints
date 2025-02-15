from dataclasses import dataclass
from typing import Optional, List

@dataclass
class UpdateCategoryCheckPointStatusDTO:
    user_id: str
    entity_id: str
    entity_type: str
    checked_checkpoint_ids: Optional[List[str]]
    unchecked_checkpoint_ids: Optional[List[str]]


@dataclass
class EntityCustomCheckPointDTO:
    entity_id:str
    entity_type:str
    category_id:str
    text:str


@dataclass
class CategoryCheckpointDTO:
    checkpoint_id: str
    text: str
    order: int
    category_id: str
    checkpoint_type: str
    entity_id: Optional[str]
    entity_type: Optional[str]


@dataclass
class EntityCategoryCheckpointDTO:
    checkpoint_id: str
    entity_id: str
    entity_type: str
    checked_by: str
    is_checked: bool
    text: Optional[str]


@dataclass
class UpdateCategoryCheckpointTextDTO:
    checkpoint_id: str
    text: str
    user_id: str
    entity_id: str
    entity_type: str


# TODO: CheckpointDTO -> CheckpointResponseDTO
@dataclass
class CheckpointResponseDTO:
    category_id: str
    checkpoint_id: str  # TODO: checkpoint_id
    text: str
    order: int
    is_checked: bool


@dataclass
class CategoryDTO:
    category_id: str
    name: str
    order: int
    category_type: str
    description: Optional[str]
    parent_category_id: Optional[str]
