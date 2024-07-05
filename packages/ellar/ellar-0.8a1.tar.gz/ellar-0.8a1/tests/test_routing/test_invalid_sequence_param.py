from typing import Dict, List, Optional, Tuple

import pytest
from ellar.common import Header, ModuleRouter, Query
from ellar.common.exceptions import ImproperConfiguration
from ellar.core.router_builders import ModuleRouterBuilder
from pydantic import BaseModel

mr = ModuleRouter("")


class Item(BaseModel):
    title: str


class Item2(BaseModel):
    title2: Item


@pytest.mark.parametrize("field_parameter", [Query(None), Header(None)])
def test_invalid_sequence(field_parameter):
    with pytest.raises(ImproperConfiguration):

        @mr.get("/items/")
        def read_items(q: List[Item] = field_parameter):
            pass  # pragma: no cover

        ModuleRouterBuilder.build(mr)


@pytest.mark.parametrize("field_parameter", [Query(None), Header(None)])
def test_invalid_tuple(field_parameter):
    with pytest.raises(ImproperConfiguration):

        @mr.get("/items/")
        def read_items(q: Tuple[Item, Item] = field_parameter):
            pass  # pragma: no cover

        ModuleRouterBuilder.build(mr)


@pytest.mark.parametrize("field_parameter", [Query(None), Header(None)])
def test_invalid_dict(field_parameter):
    with pytest.raises(ImproperConfiguration):

        @mr.get("/items/")
        def read_items(q: Dict[str, Item] = field_parameter):
            pass  # pragma: no cover

        ModuleRouterBuilder.build(mr)


@pytest.mark.parametrize("field_parameter", [Query(None), Header(None)])
def test_invalid_simple_dict(field_parameter):
    with pytest.raises(ImproperConfiguration):

        @mr.get("/items/")
        def read_items(q: Optional[dict] = field_parameter):
            pass  # pragma: no cover

        ModuleRouterBuilder.build(mr)


@pytest.mark.parametrize("field_parameter", [Query(None), Header(None)])
def test_invalid_group_type(field_parameter):
    with pytest.raises(ImproperConfiguration):

        @mr.get("/items/")
        def read_items(q: Item2 = field_parameter):
            pass  # pragma: no cover

        ModuleRouterBuilder.build(mr)
