import socket

import peary

from .mock_proxy import MockProxy
from .mock_socket import MockSocket


# pylint: disable=no-member
def test_peary_client_init_host():
    assert peary.PearyClient("alpha").host == "alpha"
    assert peary.PearyClient("beta").host == "beta"


def test_peary_client_init_port():
    assert peary.PearyClient("").port == 12345
    assert peary.PearyClient("", 12345).port == 12345
    assert peary.PearyClient("", 54321).port == 54321


def test_peary_client_init_proxy_class():
    assert peary.PearyClient("").proxy_class is peary.peary_proxy.PearyProxy
    assert peary.PearyClient("", proxy_class=MockProxy).proxy_class is MockProxy


def test_peary_client_init_socket(monkeypatch):
    monkeypatch.setattr("socket.socket", MockSocket)
    assert peary.PearyClient("").socket.family == socket.AF_INET
    assert peary.PearyClient("").socket.type == socket.SOCK_STREAM
    assert peary.PearyClient("").socket.address is None
    assert peary.PearyClient("").socket.is_connected is None
    assert peary.PearyClient("").socket.is_shutdown is None


def test_peary_client_context_manager_runs_statements(monkeypatch):
    monkeypatch.setattr("socket.socket", MockSocket)
    with peary.PearyClient("", proxy_class=MockProxy):
        test_result = True
    assert test_result is True


def test_peary_client_context_manager_enter_proxy_class(monkeypatch):
    monkeypatch.setattr("socket.socket", MockSocket)
    with peary.PearyClient("", proxy_class=MockProxy) as client:
        assert isinstance(client, MockProxy)


def test_peary_client_context_manager_enter_socket_connects(monkeypatch):
    monkeypatch.setattr("socket.socket", MockSocket)
    with peary.PearyClient("", proxy_class=MockProxy) as client:
        assert client.socket.is_connected is True
        assert client.socket.is_shutdown is False


def test_peary_client_context_manager_enter_socket_address(monkeypatch):
    monkeypatch.setattr("socket.socket", MockSocket)
    with peary.PearyClient("alpha", port=0, proxy_class=MockProxy) as client:
        assert client.socket.address == ("alpha", 0)
    with peary.PearyClient("beta", port=1, proxy_class=MockProxy) as client:
        assert client.socket.address == ("beta", 1)


def test_peary_client_context_manager_exit_socket_closes(monkeypatch):
    monkeypatch.setattr("socket.socket", MockSocket)

    mock_socket = MockSocket(socket.AF_INET, socket.SOCK_STREAM)
    with peary.PearyClient("", proxy_class=MockProxy):
        pass
    assert mock_socket.is_connected is False


def test_peary_client_context_manager_exit_socket_shutdown(monkeypatch):
    monkeypatch.setattr("socket.socket", MockSocket)

    mock_socket = MockSocket(socket.AF_INET, socket.SOCK_STREAM)
    with peary.PearyClient("", proxy_class=MockProxy):
        pass
    assert mock_socket.is_shutdown is True
    assert mock_socket.how_shutdown == socket.SHUT_RDWR


def test_peary_client_context_manager_enter_socket_exit_gracefully(monkeypatch):
    monkeypatch.setattr("socket.socket", MockSocket)

    class MockError(Exception):
        """Mock exception for testing purposes."""

    mock_socket = MockSocket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        with peary.PearyClient("", proxy_class=MockProxy):
            raise MockError  # noqa: TRY301
    except MockError:
        assert mock_socket.is_connected is False
        assert mock_socket.is_shutdown is True
        assert mock_socket.how_shutdown == socket.SHUT_RDWR
