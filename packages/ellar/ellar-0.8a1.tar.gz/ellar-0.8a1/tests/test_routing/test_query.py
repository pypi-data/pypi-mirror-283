from ellar.testing import TestClient

from ..main import app
from ..utils import pydantic_error_url

client = TestClient(app)


def test_query():
    response = client.get("/query")
    assert response.status_code == 422
    assert response.json() == (
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "query"],
                    "msg": "Field required",
                    "input": None,
                    "url": pydantic_error_url("missing"),
                }
            ]
        }
    )


def test_query_query_baz():
    response = client.get("/query?query=baz")
    assert response.status_code == 200
    assert response.json() == "foo bar baz"


def test_query_not_declared_baz():
    response = client.get("/query?not_declared=baz")
    assert response.status_code == 422
    assert response.json() == (
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "query"],
                    "msg": "Field required",
                    "input": None,
                    "url": pydantic_error_url("missing"),
                }
            ]
        }
    )


def test_query_optional():
    response = client.get("/query/optional")
    assert response.status_code == 200
    assert response.json() == "foo bar"


def test_query_optional_query_baz():
    response = client.get("/query/optional?query=baz")
    assert response.status_code == 200
    assert response.json() == "foo bar baz"


def test_query_optional_not_declared_baz():
    response = client.get("/query/optional?not_declared=baz")
    assert response.status_code == 200
    assert response.json() == "foo bar"


def test_query_int():
    response = client.get("/query/int")
    assert response.status_code == 422
    assert response.json() == (
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "query"],
                    "msg": "Field required",
                    "input": None,
                    "url": pydantic_error_url("missing"),
                }
            ]
        }
    )


def test_query_int_query_42():
    response = client.get("/query/int?query=42")
    assert response.status_code == 200
    assert response.json() == "foo bar 42"


def test_query_int_query_42_5():
    response = client.get("/query/int?query=42.5")
    assert response.status_code == 422
    assert response.json() == (
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["query", "query"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "42.5",
                    "url": pydantic_error_url("int_parsing"),
                }
            ]
        }
    )


def test_query_int_query_baz():
    response = client.get("/query/int?query=baz")
    assert response.status_code == 422
    assert response.json() == (
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["query", "query"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "baz",
                    "url": pydantic_error_url("int_parsing"),
                }
            ]
        }
    )


def test_query_int_not_declared_baz():
    response = client.get("/query/int?not_declared=baz")
    assert response.status_code == 422
    assert response.json() == (
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "query"],
                    "msg": "Field required",
                    "input": None,
                    "url": pydantic_error_url("missing"),
                }
            ]
        }
    )


def test_query_int_optional():
    response = client.get("/query/int/optional")
    assert response.status_code == 200
    assert response.json() == "foo bar"


def test_query_int_optional_query_50():
    response = client.get("/query/int/optional?query=50")
    assert response.status_code == 200
    assert response.json() == "foo bar 50"


def test_query_int_optional_query_foo():
    response = client.get("/query/int/optional?query=foo")
    assert response.status_code == 422
    assert response.json() == (
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["query", "query"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "foo",
                    "url": pydantic_error_url("int_parsing"),
                }
            ]
        }
    )


def test_query_int_default():
    response = client.get("/query/int/default")
    assert response.status_code == 200
    assert response.json() == "foo bar 10"


def test_query_int_default_query_50():
    response = client.get("/query/int/default?query=50")
    assert response.status_code == 200
    assert response.json() == "foo bar 50"


def test_query_int_default_query_foo():
    response = client.get("/query/int/default?query=foo")
    assert response.status_code == 422
    assert response.json() == (
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["query", "query"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "foo",
                    "url": pydantic_error_url("int_parsing"),
                }
            ]
        }
    )


def test_query_param():
    response = client.get("/query/param")
    assert response.status_code == 200
    assert response.json() == "foo bar"


def test_query_param_query_50():
    response = client.get("/query/param?query=50")
    assert response.status_code == 200
    assert response.json() == "foo bar 50"


def test_query_param_required():
    response = client.get("/query/param-required")
    assert response.status_code == 422
    assert response.json() == (
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "query"],
                    "msg": "Field required",
                    "input": None,
                    "url": pydantic_error_url("missing"),
                }
            ]
        }
    )


def test_query_param_required_query_50():
    response = client.get("/query/param-required?query=50")
    assert response.status_code == 200
    assert response.json() == "foo bar 50"


def test_query_param_required_int():
    response = client.get("/query/param-required/int")
    assert response.status_code == 422
    assert response.json() == (
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "query"],
                    "msg": "Field required",
                    "input": None,
                    "url": pydantic_error_url("missing"),
                }
            ]
        }
    )


def test_query_param_required_int_query_50():
    response = client.get("/query/param-required/int?query=50")
    assert response.status_code == 200
    assert response.json() == "foo bar 50"


def test_query_param_required_int_query_foo():
    response = client.get("/query/param-required/int?query=foo")
    assert response.status_code == 422
    assert response.json() == (
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["query", "query"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "foo",
                    "url": pydantic_error_url("int_parsing"),
                }
            ]
        }
    )


def test_query_frozenset_query_1_query_1_query_2():
    response = client.get("/query/frozenset?query=1&query=1&query=2")
    assert response.status_code == 200
    assert response.json() == "1,2"
