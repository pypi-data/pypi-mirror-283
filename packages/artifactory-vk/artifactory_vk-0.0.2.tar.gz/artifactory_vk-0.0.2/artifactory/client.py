import os
from typing import IO, Iterator

import requests
from tusclient.uploader import Uploader as TusUploader

from artifactory.utils.requesters import DefaultRequester
from .client_config import ClientConfig
from .models.resources import ResourceMeta
from .units import MB


class Client:
    """
    Client to Artifactory service.
    Thread-safe.
    """

    def __init__(
        self,
        config: ClientConfig | None = None,
    ):
        self._config = config or ClientConfig()
        self._requester = DefaultRequester()

    def upload_resource(
        self,
        reader: IO[bytes],
        *,
        file_name: str | None = None,
        md5: str | None = None,
        context: dict | None = None,
        soft_ttl_s: int | None = None,
        hard_ttl_s: int | None = None,
    ) -> str:
        """ Uploads resource and returns resource id. """
        byte_size = _get_byte_size(reader)
        body = {
            'file_name': file_name,
            'byte_size': byte_size,
            'checksum_md5': md5,
            'context': context,
            'soft_ttl_s': soft_ttl_s,
            'hard_ttl_s': hard_ttl_s,
        }
        resp = self._requester.post(self._make_url('/v1/resources/drafts'), json=body)
        resp.raise_for_status()
        resp_body = resp.json()
        resource_id = resp_body['resource_id']
        upload_url = resp_body['upload_url']
        
        uploader = TusUploader(
            file_stream=reader,
            url=upload_url,
            chunk_size=self.config.upload_chunk_size,
        )
        uploader.upload()
        
        return resource_id

    def download_resource(
        self,
        resource_id: str,
        *,
        chunk_size: int = 10 * MB,
    ) -> Iterator[bytes]:
        """ Downloads resource. """
        download_url = self.get_download_url(resource_id)
        with requests.get(download_url, stream=True, verify=False) as resp:
            resp.raise_for_status()
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    yield chunk

    def get_resource_meta(
        self,
        resource_id: str,
    ) -> ResourceMeta:
        """ Fetches resource's meta. """
        resp = self._requester.get(self._make_url(f'/v1/resources/{resource_id}'))
        resp.raise_for_status()
        resp_body = resp.json()
        resp_body.pop('download_url')
        return ResourceMeta(**resp_body)

    def copy_resource(
        self,
        resource_id: str,
        *,
        file_name: str | None = None,
        context: dict | None = None,
        soft_ttl_s: int | None = None,
        hard_ttl_s: int | None = None,
    ) -> str:
        """ Copies resource with new meta and returns resource id. """
        body = {
            'file_name': file_name,
            'context': context,
            'soft_ttl_s': soft_ttl_s,
            'hard_ttl_s': hard_ttl_s,
        }
        resp = self._requester.post(self._make_url(f'/v1/resources/{resource_id}/copy'), json=body)
        resp.raise_for_status()
        return resp.json()['resource_id']

    def get_download_url(
        self,
        resource_id: str,
    ) -> str:
        """ Returns url to download given resource. """
        resp = self._requester.get(self._make_url(f'/v1/resources/{resource_id}'))
        resp.raise_for_status()
        download_url = resp.json()['download_url']
        if download_url == '':
            download_url = self._make_url(f'/v1/resources/{resource_id}/content')
        return download_url

    @property
    def config(self) -> ClientConfig:
        return self._config
    
    def _make_url(self, path_and_query: str):
        if not path_and_query.startswith('/'):
            path_and_query = '/' + path_and_query
        return f'{self.config.artifactory_endpoint}{path_and_query}'


def _get_byte_size(reader: IO[bytes]) -> int:
    reader.seek(0, os.SEEK_END)
    return reader.tell()
