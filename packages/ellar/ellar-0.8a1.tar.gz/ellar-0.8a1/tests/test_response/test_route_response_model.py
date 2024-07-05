from typing import List, Union

import pytest
from ellar.common import UJSONResponse
from ellar.common.constants import CONTROLLER_CLASS_KEY, RESPONSE_OVERRIDE_KEY
from ellar.common.exceptions import ImproperConfiguration
from ellar.common.responses.models import (
    EmptyAPIResponseModel,
    JSONResponseModel,
    ResponseModel,
    RouteResponseExecution,
    RouteResponseModel,
)
from ellar.core.routing import RouteOperation
from ellar.reflect import reflect

from ..schema import BlogObjectDTO, NoteSchemaDC


def endpoint_sample():
    pass  # pragma: no cover


class JsonApiResponse(UJSONResponse):
    media_type = "application/vnd.api+json"


class JsonApiResponseModel(ResponseModel):
    response_type = JsonApiResponse
    model_field_or_schema = List[Union[NoteSchemaDC, BlogObjectDTO]]
    default_description = "Successful JsonAPI Response"


@pytest.mark.parametrize(
    "route_responses, route_model, status, description, content_type",
    [
        (
            {200: List[Union[NoteSchemaDC, BlogObjectDTO]]},
            JSONResponseModel,
            200,
            "Successful Response",
            "application/json",
        ),
        (
            {200: EmptyAPIResponseModel()},
            EmptyAPIResponseModel,
            200,
            "Successful Response",
            "application/json",
        ),
        (
            {
                201: (Union[NoteSchemaDC, BlogObjectDTO], "Create Note"),
                200: EmptyAPIResponseModel(),
            },
            JSONResponseModel,
            201,
            "Create Note",
            "application/json",
        ),
        (
            {
                201: (Union[NoteSchemaDC, BlogObjectDTO], "Create Note"),
                200: EmptyAPIResponseModel(),
            },
            JSONResponseModel,
            200,
            "Successful Response",
            "application/json",
        ),
        (
            {200: JsonApiResponseModel()},
            JsonApiResponseModel,
            200,
            "Successful JsonAPI Response",
            "application/vnd.api+json",
        ),
        (
            {200: JsonApiResponse},
            ResponseModel,
            200,
            "Successful Response",
            "application/vnd.api+json",
        ),
    ],
)
def test_route_response_model(
    route_responses, route_model, status, description, content_type
):
    route_response_model = RouteResponseModel(route_responses=route_responses)
    assert route_response_model.models[status]
    assert route_response_model.models[status].media_type == content_type
    assert route_response_model.models[status].description == description
    assert isinstance(route_response_model.models[status], route_model)


@pytest.mark.parametrize(
    "inputs",
    [
        [],
        set(),
        (),
        ResponseModel,
        JsonApiResponseModel,
        EmptyAPIResponseModel,
    ],
)
def test_route_response_model_exception(inputs):
    with pytest.raises(RouteResponseExecution):
        RouteResponseModel(route_responses=inputs)


def test_invalid_response_override_definition():
    with reflect.context():
        reflect.define_metadata(
            RESPONSE_OVERRIDE_KEY, {EmptyAPIResponseModel()}, endpoint_sample
        )
        reflect.define_metadata(
            CONTROLLER_CLASS_KEY, type("endpoint_sample_class", (), {}), endpoint_sample
        )
        with pytest.raises(ImproperConfiguration) as ex:
            RouteOperation(
                path="/",
                methods=["get"],
                endpoint=endpoint_sample,
                response={200: EmptyAPIResponseModel()},
            )
    assert "`RESPONSE_OVERRIDE` is must be of type `Dict`" in str(ex)
