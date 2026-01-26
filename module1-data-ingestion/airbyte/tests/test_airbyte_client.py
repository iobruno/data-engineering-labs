from os import getenv
from pathlib import Path

import pytest
import vcr
from airbyte_api.errors import SDKError

from app.airbyte_client import AirbyteClient

recorder = vcr.VCR(
    cassette_library_dir=f"{Path(__file__).parent}/cassettes",
    filter_headers=[("Authorization", "Bearer ********")],
    filter_post_data_parameters=[
        ("client_id", "********"),
        ("client_secret", "********"),
    ],
)


@pytest.fixture(scope="session", autouse=True)
def configure_vcr():
    recorder.register_matcher("uri", lambda r1, r2: Path(r1.path).parent == Path(r2.path).parent)


@pytest.fixture
def ab_client() -> AirbyteClient:
    api_url = getenv("AIRBYTE_API_URL", "http://localhost:8000/api/public/v1")
    client_id = getenv("AIRBYTE_CLIENT_ID")
    client_secret = getenv("AIRBYTE_CLIENT_SECRET")

    return AirbyteClient.create(
        api_url=api_url,
        client_id=client_id,
        client_secret=client_secret,
    )


@recorder.use_cassette("airbyte_list_connections.yaml")
def test_list_connections_returns_200(ab_client):
    resp = ab_client.list_connections()
    assert resp.status_code == 200


@recorder.use_cassette("airbyte_list_connections.yaml")
def test_list_connections_has_req_attr(ab_client):
    resp = ab_client.list_connections()
    conn = resp.connections_response.data[0]
    assert set(conn.to_dict().keys()).issuperset({
        "connectionId",
        "name",
        "sourceId",
        "destinationId",
        "configurations",
        "workspaceId",
    })


@recorder.use_cassette("airbyte_get_source_200_rss.yaml", match_on=["method", "uri"])
def test_get_source_with_valid_id_that_exists_returns_200(ab_client):
    resp = ab_client.get_source(id="d73fb160-9fbd-457e-891e-22d5ac5b5aee")
    assert resp.status_code == 200


@recorder.use_cassette("airbyte_get_source_200_rss.yaml", match_on=["method", "uri"])
def test_get_source_with_valid_id_that_exists_has_req_attr(ab_client):
    resp = ab_client.get_source(id="d73fb160-9fbd-457e-891e-22d5ac5b5aee")
    source = resp.source_response
    assert set(source.to_dict().keys()).issuperset({
        "sourceId",
        "name",
        "configuration",
        "workspaceId",
    })


@recorder.use_cassette("airbyte_get_source_404.yaml", match_on=["method", "uri"])
def test_get_source_with_valid_id_that_not_exists_returns_404(ab_client):
    with pytest.raises(SDKError) as err:
        ab_client.get_source(id="d73fb160-9fbd-457e-891e-22d5ac5b5aaa")
    assert err.value.status_code == 404


@recorder.use_cassette("airbyte_get_source_500.yaml", match_on=["method", "uri"])
def test_get_source_with_invalid_id_returns_500(ab_client):
    with pytest.raises(SDKError) as err:
        ab_client.get_source(id="invalid-id")
    assert err.value.status_code == 500


@recorder.use_cassette("airbyte_get_destination_200_bigquery.yaml", match_on=["method", "uri"])
def test_get_destination_with_valid_id_returns_200(ab_client):
    resp = ab_client.get_destination(id="14e21b21-85d5-46b8-916a-df3c087ac4fe")
    assert resp.status_code == 200


@recorder.use_cassette("airbyte_get_destination_200_bigquery.yaml", match_on=["method", "uri"])
def test_get_destination_with_valid_id_has_req_attr(ab_client):
    resp = ab_client.get_destination(id="14e21b21-85d5-46b8-916a-df3c087ac4fe")
    destination = resp.destination_response
    assert set(destination.to_dict().keys()).issuperset({
            "destinationId",
            "name",
            "configuration",
            "workspaceId",
    })


@recorder.use_cassette("airbyte_get_destination_404.yaml", match_on=["method", "uri"])
def test_get_destination_with_valid_id_that_not_exists_returns_404(ab_client):
    with pytest.raises(SDKError) as err:
        ab_client.get_source(id="14e21b21-85d5-46b8-916a-df3c087ac4fa")
    assert err.value.status_code == 404


@recorder.use_cassette("airbyte_get_destination_500.yaml", match_on=["method", "uri"])
def test_get_destination_with_invalid_id_returns_500(ab_client):
    with pytest.raises(SDKError) as err:
        ab_client.get_destination(id="invalid")
    assert err.value.status_code == 500
