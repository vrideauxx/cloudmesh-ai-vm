import importlib
from unittest.mock import Mock
from types import SimpleNamespace

import pytest

manager = importlib.import_module(
    "cloudmesh.ai.vm.openstack.ChameleonManager"
)


@pytest.mark.parametrize("server_id, expected", [
    (None, False),
    ("test-server-id", True),
])
def test_vm_exists(monkeypatch, server_id, expected):
    provider = SimpleNamespace(_setup_chi_context=Mock())
    lookup = Mock(return_value=server_id)

    monkeypatch.setattr(
        manager, "chi",
        SimpleNamespace(
            server=SimpleNamespace(get_server_id=lookup)
        ),
    )

    assert manager.Provider._vm_exists(
        provider, "test-vm"
    ) is expected

    lookup.assert_called_once_with("test-vm")


def test_vm_exists_api_failure(monkeypatch):
    provider = SimpleNamespace(_setup_chi_context=Mock())
    lookup = Mock(side_effect=RuntimeError("API unavailable"))

    monkeypatch.setattr(
        manager, "chi",
        SimpleNamespace(
            server=SimpleNamespace(get_server_id=lookup)
        ),
    )

    with pytest.raises(manager.VMProviderError):
        manager.Provider._vm_exists(provider, "test-vm")
