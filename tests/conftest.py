from pathlib import Path

import pytest

INTEGRATION_DIR = Path(__file__).parent / "integration"


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    # Tests in tests/integration need a running AlgoKit LocalNet
    for item in items:
        if INTEGRATION_DIR in item.path.parents:
            item.add_marker(pytest.mark.integration)
