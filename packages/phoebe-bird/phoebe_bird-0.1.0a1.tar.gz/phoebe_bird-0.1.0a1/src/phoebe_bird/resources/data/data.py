# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .observations import (
    ObservationsResource,
    AsyncObservationsResource,
    ObservationsResourceWithRawResponse,
    AsyncObservationsResourceWithRawResponse,
    ObservationsResourceWithStreamingResponse,
    AsyncObservationsResourceWithStreamingResponse,
)
from .observations.observations import ObservationsResource, AsyncObservationsResource

__all__ = ["DataResource", "AsyncDataResource"]


class DataResource(SyncAPIResource):
    @cached_property
    def observations(self) -> ObservationsResource:
        return ObservationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> DataResourceWithRawResponse:
        return DataResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DataResourceWithStreamingResponse:
        return DataResourceWithStreamingResponse(self)


class AsyncDataResource(AsyncAPIResource):
    @cached_property
    def observations(self) -> AsyncObservationsResource:
        return AsyncObservationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDataResourceWithRawResponse:
        return AsyncDataResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDataResourceWithStreamingResponse:
        return AsyncDataResourceWithStreamingResponse(self)


class DataResourceWithRawResponse:
    def __init__(self, data: DataResource) -> None:
        self._data = data

    @cached_property
    def observations(self) -> ObservationsResourceWithRawResponse:
        return ObservationsResourceWithRawResponse(self._data.observations)


class AsyncDataResourceWithRawResponse:
    def __init__(self, data: AsyncDataResource) -> None:
        self._data = data

    @cached_property
    def observations(self) -> AsyncObservationsResourceWithRawResponse:
        return AsyncObservationsResourceWithRawResponse(self._data.observations)


class DataResourceWithStreamingResponse:
    def __init__(self, data: DataResource) -> None:
        self._data = data

    @cached_property
    def observations(self) -> ObservationsResourceWithStreamingResponse:
        return ObservationsResourceWithStreamingResponse(self._data.observations)


class AsyncDataResourceWithStreamingResponse:
    def __init__(self, data: AsyncDataResource) -> None:
        self._data = data

    @cached_property
    def observations(self) -> AsyncObservationsResourceWithStreamingResponse:
        return AsyncObservationsResourceWithStreamingResponse(self._data.observations)
