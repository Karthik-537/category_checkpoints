from typing import List

class InvalidCategoryId(Exception):
    def __init__(
            self,
            invalid_ids: List[str]
    ):
        self.invalid_ids=invalid_ids

    def __str__(self):
        return f"{self.invalid_ids}"


class InvalidCheckpointId(Exception):
    def __init__(
            self,
            invalid_ids: List[str]
    ):
        self.invalid_ids=invalid_ids

    def __str__(self):
        return f"{self.invalid_ids}"


class InvalidParentCategoryId(Exception):
    def __init__(
            self,
            parent_category_id: str
    ):
        self.parent_category_id = parent_category_id

    def __str__(self):

        return f"{self.parent_category_id}"


class NotSupportedParentCategoryType(Exception):

    def __init__(
            self,
            parent_category_id: str
    ):
        self.parent_category_id = parent_category_id

    def __str__(self):

        return f"not supported category_type for {self.parent_category_id}"

class NotSupportedCheckpointType(Exception):

    def __init__(
            self,
            checkpoint_id: str
    ):
        self.checkpoint_id = checkpoint_id

    def __str__(self):
        return f"not supported checkpoint type for {self.checkpoint_id}"