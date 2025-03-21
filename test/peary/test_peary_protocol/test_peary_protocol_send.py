from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable


def test_peary_protocol_send_okay(patch_socket: Callable) -> None:
    # pylint: disable-next=unnecessary-lambda
    with patch_socket(mock_send=lambda _: len(_)) as socket_class:
        PearyProtocol(socket_class(), checks=PearyProtocol.Checks.CHECK_NONE).request(
            ""
        )


def test_peary_protocol_send_error(patch_socket: Callable) -> None:
    with patch_socket(mock_send=lambda _: len(_) - 1) as socket_class:
        with pytest.raises(
            PearyProtocol.RequestSendError, match="Failed to send request:*"
        ):
            PearyProtocol(
                socket_class(), checks=PearyProtocol.Checks.CHECK_NONE
            ).request("")
