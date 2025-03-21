from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable


def test_peary_protocol_version_request_message(patch_socket: Callable) -> None:

    class MockProtocol(PearyProtocol):

        def request(
            self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
        ) -> bytes:
            assert msg == "protocol_version"
            return b"1"

    with patch_socket() as socket_class:
        MockProtocol(socket_class())


def test_peary_protocol_version_supported(patch_socket: Callable) -> None:

    class MockProtocol(PearyProtocol):

        def request(
            self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
        ) -> bytes:
            return b"1"

    with patch_socket() as socket_class:
        MockProtocol(socket_class())


def test_peary_protocol_version_unsupported(patch_socket: Callable) -> None:

    class MockProtocol(PearyProtocol):

        def request(
            self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
        ) -> bytes:
            return b"0"

    with patch_socket() as socket_class:
        with pytest.raises(
            PearyProtocol.VersionError, match="Unsupported protocol version: b'0'"
        ):
            MockProtocol(socket_class())
