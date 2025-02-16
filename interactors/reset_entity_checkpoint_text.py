from interactors.storage_interfaces.storage_interface import StorageInterface
from interactors.mixins.category_mixin import CategoryMixin
from constants.enums import CategoryCheckpointType, CategoryEntityType
from exceptions import custom_exceptions
from typing import Dict
import re


class ResetEntityCheckpointTextInteractor:

    def __init__(
            self,
            storage: StorageInterface
    ):
        self.storage = storage

    @property
    def category_mixin(self):
        return CategoryMixin()

    def reset_entity_checkpoint_text(
            self,
            entity_id: str,
            entity_type: CategoryEntityType,
            checkpoint_id: str
    ) -> str:

        self.category_mixin.validate_checkpoint_id(
            checkpoint_id=checkpoint_id,
            storage=self.storage
        )

        self._validate_checkpoint_type(
            checkpoint_id=checkpoint_id
        )

        checkpoint_dtos = self.storage.get_checkpoints(
            checkpoint_ids=[checkpoint_id]
        )

        valid_entity_checkpoints = self.storage.get_entity_checkpoint_ids(
            entity_id=entity_id,
            entity_type=entity_type
        )
        if checkpoint_id in valid_entity_checkpoints:
            self.storage.update_entity_category_checkpoint_text(
                entity_id=entity_id,
                entity_type=entity_type,
                checkpoint_id=checkpoint_id,
                text=None
            )
        updated_text = checkpoint_dtos[0].text
        placeholder_data = self._get_placeholder_data(
            entity_id=entity_id
        )
        updated_text = self._format_checkpoint_text(
            checkpoint_text=updated_text,
            variables=placeholder_data
        )

        return updated_text

    def _validate_checkpoint_type(
            self,
            checkpoint_id: str
    ):
        checkpoint_dtos = self.storage.get_checkpoints(
            checkpoint_ids=[checkpoint_id]
        )
        if checkpoint_dtos[0].checkpoint_type != CategoryCheckpointType.SYSTEM.value:
            raise custom_exceptions.NotSupportedCheckpointType(
                checkpoint_id=checkpoint_id
            )

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
