import airbyte_api as ab
import structlog
from airbyte_api import api, models
from airbyte_api.utils import BackoffStrategy, RetryConfig

structlog.configure(processors=[
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.JSONRenderer(),
])

log = structlog.get_logger()


class AirbyteClient:
    def __init__(self, ab_api: ab.AirbyteAPI):
        self.api = ab_api

    def get_source(self, id: str) -> api.GetSourceResponse:
        return self.api.sources.get_source(api.GetSourceRequest(id, False))

    def get_destination(self, id: str) -> api.GetDestinationResponse:
        return self.api.destinations.get_destination(api.GetDestinationRequest(id, False))

    def list_connections(self) -> api.ListConnectionsResponse:
        return self.api.connections.list_connections(api.ListConnectionsRequest(
            limit=10,
            offset=0,
            include_deleted=False,
        ))

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
