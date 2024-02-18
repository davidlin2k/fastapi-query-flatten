from typing import Optional, List
from typing_extensions import Annotated

import pytest
from fastapi.testclient import TestClient

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi.middleware import Middleware

from fastapi_query_flatten.middleware import QueryFlattenMiddleware


@pytest.fixture(scope="module")
def app():
    async def query_endpoint(q: Annotated[Optional[List[str]], Query()] = None):
        return JSONResponse(content=q)

    async def multiple_query_endpoint(
        q: Annotated[Optional[List[str]], Query()] = None,
        r: Annotated[Optional[List[str]], Query()] = None,
    ):
        return JSONResponse(content={"q": q, "r": r})

    routes = [
        APIRoute("/query", endpoint=query_endpoint, methods=["GET"]),
        APIRoute("/multiple_query", endpoint=multiple_query_endpoint, methods=["GET"]),
    ]

    middleware = [
        Middleware(QueryFlattenMiddleware, delimiter=","),
    ]

    app_ = FastAPI(routes=routes, middleware=middleware)

    return app_


@pytest.fixture(scope="module")
def client(app):
    return TestClient(app)


def test_query_flatten_middleware_get(client):
    # Test the middleware with a single query parameter
    response = client.get("/query?q=1,2")
    assert response.status_code == 200
    assert response.text == '["1","2"]'


def test_query_flatten_middleware_get_no_query(client):
    # Test the middleware with no query parameters
    response = client.get("/query")
    assert response.status_code == 200
    assert response.text == "null"


def test_query_flatten_middleware_get_empty_query(client):
    # Test the middleware with an empty query parameter
    response = client.get("/query?q=")
    assert response.status_code == 200
    assert response.text == '[""]'


def test_query_flatten_middleware_get_single_query(client):
    # Test the middleware with a single query parameter
    response = client.get("/query?q=1")
    assert response.status_code == 200
    assert response.text == '["1"]'


def test_query_flatten_middleware_get_multiple_query(client):
    # Test the middleware with multiple query parameters
    response = client.get("/query?q=1&q=2")
    assert response.status_code == 200
    assert response.text == '["1","2"]'


def test_query_flatten_middleware_get_multiple_query_with_empty(client):
    # Test the middleware with multiple query parameters and an empty query parameter
    response = client.get("/query?q=1&q=2&q=")
    assert response.status_code == 200
    assert response.text == '["1","2",""]'


def test_query_flatten_middleware_multiple_query_get(client):
    # Test the middleware with multiple query parameters
    response = client.get("/multiple_query?q=1,2&r=3,4")
    assert response.status_code == 200
    assert response.json() == {"q": ["1", "2"], "r": ["3", "4"]}


def test_query_flatten_middleware_multiple_query_get_no_query(client):
    # Test the middleware with no query parameters
    response = client.get("/multiple_query")
    assert response.status_code == 200
    assert response.json() == {"q": None, "r": None}


def test_query_flatten_middleware_multiple_query_get_empty_query(client):
    # Test the middleware with an empty query parameter
    response = client.get("/multiple_query?q=&r=")
    assert response.status_code == 200
    assert response.json() == {"q": [""], "r": [""]}


def test_query_flatten_middleware_multiple_query_get_single_query(client):
    # Test the middleware with a single query parameter
    response = client.get("/multiple_query?q=1&r=2")
    assert response.status_code == 200
    assert response.json() == {"q": ["1"], "r": ["2"]}


def test_query_flatten_middleware_multiple_query_get_multiple_empty(client):
    # Test the middleware with multiple empty query parameters
    response = client.get("/multiple_query?q=,,&r=,")
    assert response.status_code == 200
    assert response.json() == {"q": ["", "", ""], "r": ["", ""]}
