from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from .conftest import MockSocket


def test_peary_protocol_version_request_message(mock_socket: type[MockSocket]) -> None:

    class MockPearyProtocol(PearyProtocol):

        def request(
            self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
        ) -> bytes:
            assert msg == "protocol_version"
            return b"1"

    MockPearyProtocol(mock_socket())


def test_peary_protocol_init_version_supported(mock_socket: type[MockSocket]) -> None:

    class MockPearyProtocol(PearyProtocol):

        def request(
            self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
        ) -> bytes:
            return b"1"

    MockPearyProtocol(mock_socket())


def test_peary_protocol_init_version_unsupported(mock_socket: type[MockSocket]) -> None:

    class MockPearyProtocol(PearyProtocol):

        def request(
            self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
        ) -> bytes:
            return b"0"

    with pytest.raises(
        PearyProtocol.IncompatibleProtocolError,
        match="Unsupported protocol version: b'0'",
    ):
        MockPearyProtocol(mock_socket())
