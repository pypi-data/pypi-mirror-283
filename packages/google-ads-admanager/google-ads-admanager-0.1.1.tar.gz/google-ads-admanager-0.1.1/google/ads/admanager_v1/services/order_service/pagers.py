# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
)

from google.ads.admanager_v1.types import order_service


class ListOrdersPager:
    """A pager for iterating through ``list_orders`` requests.

    This class thinly wraps an initial
    :class:`google.ads.admanager_v1.types.ListOrdersResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``orders`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListOrders`` requests and continue to iterate
    through the ``orders`` field on the
    corresponding responses.

    All the usual :class:`google.ads.admanager_v1.types.ListOrdersResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[..., order_service.ListOrdersResponse],
        request: order_service.ListOrdersRequest,
        response: order_service.ListOrdersResponse,
        *,
        metadata: Sequence[Tuple[str, str]] = ()
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (google.ads.admanager_v1.types.ListOrdersRequest):
                The initial request object.
            response (google.ads.admanager_v1.types.ListOrdersResponse):
                The initial response object.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        self._method = method
        self._request = order_service.ListOrdersRequest(request)
        self._response = response
        self._metadata = metadata

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterator[order_service.ListOrdersResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request, metadata=self._metadata)
            yield self._response

    def __iter__(self) -> Iterator[order_service.Order]:
        for page in self.pages:
            yield from page.orders

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
