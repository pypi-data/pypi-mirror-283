from typing import Annotated, Any, Literal, Optional

from pydantic import BaseModel
from pydantic.main import ModelMetaclass

from dropbase.models.category import PropertyCategory


class ChartContextProperty(BaseModel):
    data: Optional[Any]
    message: Optional[str]
    message_type: Optional[str]


class ChartProperty(BaseModel):
    block_type: Literal["chart"]

    # general
    label: Annotated[str, PropertyCategory.default]
    name: Annotated[str, PropertyCategory.default]
    description: Annotated[Optional[str], PropertyCategory.default]

    refetch_interval: Annotated[Optional[int], PropertyCategory.default]

    # position
    w: Annotated[Optional[int], PropertyCategory.internal] = 9
    h: Annotated[Optional[int], PropertyCategory.internal] = 3
    x: Annotated[Optional[int], PropertyCategory.internal] = 0
    y: Annotated[Optional[int], PropertyCategory.internal] = 0

    # internal
    context: ModelMetaclass = ChartContextProperty
