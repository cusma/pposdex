import pytest

from pposdex.ppos_dex_data import InvalidDataError, validate


@pytest.fixture
def data_point() -> dict:
    return {
        "algo_threshold": 1000,
        "accounts": 42,
        "algo_dynamics": 0.7,
        "ppos_online_stake": 0.5,
        "ppos_online_accounts": 0.1,
        "algo_hhi": 0.01,
        "ppos_gini": 0.9,
        "ppos_theil_l": 3.2,
        "ppos_theil_t": 2.1,
        "ppos_hhi": 0.02,
        "ppos_dex": 0.03,
        "ppos_dex_v2": 0.3,
        "timestamp": "2026-11-03 00:00:00.000000",
    }


def test_valid(data_point: dict) -> None:
    assert validate(data_point) == data_point


@pytest.mark.parametrize("key", ["algo_hhi", "ppos_hhi", "ppos_dex_v2"])
def test_optional_key(data_point: dict, key: str) -> None:
    del data_point[key]
    assert validate(data_point) == data_point


@pytest.mark.parametrize("key", ["algo_threshold", "ppos_gini", "timestamp"])
def test_missing_key(data_point: dict, key: str) -> None:
    del data_point[key]
    with pytest.raises(InvalidDataError):
        validate(data_point)


def test_unknown_key(data_point: dict) -> None:
    data_point["unknown"] = 1
    with pytest.raises(InvalidDataError):
        validate(data_point)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("accounts", -1),
        ("accounts", 1.0),
        ("algo_dynamics", -0.1),
        ("ppos_gini", 1.1),
        ("ppos_dex", 1),
        ("timestamp", 0),
    ],
)
def test_invalid_value(data_point: dict, key: str, value: object) -> None:
    data_point[key] = value
    with pytest.raises(InvalidDataError):
        validate(data_point)


@pytest.mark.parametrize("data", [None, 110, "noise", [1, 2]])
def test_not_a_mapping(data: object) -> None:
    with pytest.raises(InvalidDataError):
        validate(data)
