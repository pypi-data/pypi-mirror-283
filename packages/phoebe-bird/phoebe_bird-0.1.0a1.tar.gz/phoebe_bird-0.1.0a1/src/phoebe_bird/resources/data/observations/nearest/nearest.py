# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ....._compat import cached_property
from .geo_species import (
    GeoSpeciesResource,
    AsyncGeoSpeciesResource,
    GeoSpeciesResourceWithRawResponse,
    AsyncGeoSpeciesResourceWithRawResponse,
    GeoSpeciesResourceWithStreamingResponse,
    AsyncGeoSpeciesResourceWithStreamingResponse,
)
from ....._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["NearestResource", "AsyncNearestResource"]


class NearestResource(SyncAPIResource):
    @cached_property
    def geo_species(self) -> GeoSpeciesResource:
        return GeoSpeciesResource(self._client)

    @cached_property
    def with_raw_response(self) -> NearestResourceWithRawResponse:
        return NearestResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NearestResourceWithStreamingResponse:
        return NearestResourceWithStreamingResponse(self)


class AsyncNearestResource(AsyncAPIResource):
    @cached_property
    def geo_species(self) -> AsyncGeoSpeciesResource:
        return AsyncGeoSpeciesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncNearestResourceWithRawResponse:
        return AsyncNearestResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNearestResourceWithStreamingResponse:
        return AsyncNearestResourceWithStreamingResponse(self)


class NearestResourceWithRawResponse:
    def __init__(self, nearest: NearestResource) -> None:
        self._nearest = nearest

    @cached_property
    def geo_species(self) -> GeoSpeciesResourceWithRawResponse:
        return GeoSpeciesResourceWithRawResponse(self._nearest.geo_species)


class AsyncNearestResourceWithRawResponse:
    def __init__(self, nearest: AsyncNearestResource) -> None:
        self._nearest = nearest

    @cached_property
    def geo_species(self) -> AsyncGeoSpeciesResourceWithRawResponse:
        return AsyncGeoSpeciesResourceWithRawResponse(self._nearest.geo_species)


class NearestResourceWithStreamingResponse:
    def __init__(self, nearest: NearestResource) -> None:
        self._nearest = nearest

    @cached_property
    def geo_species(self) -> GeoSpeciesResourceWithStreamingResponse:
        return GeoSpeciesResourceWithStreamingResponse(self._nearest.geo_species)


class AsyncNearestResourceWithStreamingResponse:
    def __init__(self, nearest: AsyncNearestResource) -> None:
        self._nearest = nearest

    @cached_property
    def geo_species(self) -> AsyncGeoSpeciesResourceWithStreamingResponse:
        return AsyncGeoSpeciesResourceWithStreamingResponse(self._nearest.geo_species)
