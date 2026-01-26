import airbyte_api as ab
import structlog
from airbyte_api import api, models
from airbyte_api.utils import BackoffStrategy, RetryConfig

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)

log = structlog.get_logger()


class AirbyteClient:
    def __init__(self, ab_api: ab.AirbyteAPI):
        self.api = ab_api

    def get_source(self, id: str) -> models.SourceResponse:
        response = self.api.sources.get_source(api.GetSourceRequest(id, False))
        return response.source_response

    def get_destination(self, id: str) -> models.DestinationResponse:
        response = self.api.destinations.get_destination(api.GetDestinationRequest(id, False))
        return response.destination_response

    def get_conn(self, id: str) -> models.ConnectionResponse:
        response = self.api.connections.get_connection(api.GetConnectionRequest(id))
        return response.connection_response

    def list_connections(self) -> list[models.ConnectionResponse]:
        response = self.api.connections.list_connections(
            api.ListConnectionsRequest(limit=10, offset=0, include_deleted=False)
        )
        return response.connections_response.data

    # fmt: off
    @classmethod
    def create(cls, api_url: str, client_id: str, client_secret: str) -> "AirbyteClient":
        return AirbyteClient(ab.AirbyteAPI(
            server_url=api_url,
            security=models.Security(
                client_credentials=models.SchemeClientCredentials(
                client_id=client_id,
                client_secret=client_secret,
                token_url=api_url + "/applications/token",
            )),
            retry_config=RetryConfig(
                retry_connection_errors=True,
                strategy="exponential-backoff",
                backoff=BackoffStrategy(
                    initial_interval=3,
                    max_interval=30,
                    max_elapsed_time=600,
                    exponent=2,
            ))
        ))
    # fmt: on
