import enum
class CategoryEntityType(enum.Enum):
    PIPELINE_ITEM = "PIPELINE_ITEM"


class CategoryCheckpointType(enum.Enum):
    SYSTEM = "SYSTEM"
    CUSTOM = "CUSTOM"


class CategoryType( enum.Enum):
    CATEGORY = "CATEGORY"
    SUB_CATEGORY = "SUB_CATEGORY"