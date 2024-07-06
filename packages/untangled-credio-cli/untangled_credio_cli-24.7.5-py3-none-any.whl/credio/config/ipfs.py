import ipfshttpclient
import ipfshttpclient.requests_wrapper

from .store import default as store


class IPFSClient:
    _client: ipfshttpclient.Client

    def __init__(self):
        self._client = ipfshttpclient.Client(
            addr=(store.get("IPFS_GATEWAY") or ipfshttpclient.DEFAULT_ADDR),
            session=True,
        )

    def add(self, path: str) -> str:
        return self._client.add(path, pin=True)["Hash"]  # type: ignore

    def cat(self, content_id: str) -> bytes:
        return self._client.cat(content_id)


client = IPFSClient()
