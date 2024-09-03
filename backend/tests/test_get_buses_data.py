import pytest
import requests
from unittest.mock import patch
from temp.utils.get_buses_data import get_buses_data


@patch("requests.get")
def test_get_buses_data_success(mock_get):
    # mock response data
    mock_get.return_value.json.return_value = [
        {"ordem": "1001", "linha": "A", "datahora": "2024-09-01T08:30:00"},
        {"ordem": "1002", "linha": "B", "datahora": "2024-09-01T09:00:00"},
    ]
    start_time = "08:00:00"
    end_time = "09:00:00"
    result = get_buses_data(start_time, end_time)

    # expected result
    expected_result = [
        {"ordem": "1001", "linha": "A", "datahora": "2024-09-01T08:30:00"},
        {"ordem": "1002", "linha": "B", "datahora": "2024-09-01T09:00:00"},
    ]
    assert result == expected_result


@patch("requests.get")
def test_get_buses_data_empty(mock_get):
    mock_get.return_value.json.return_value = []

    start_time = "08:00:00"
    end_time = "09:00:00"
    result = get_buses_data(start_time, end_time)

    assert result == []


@patch("requests.get")
def test_get_buses_data_failure(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException

    start_time = "08:00:00"
    end_time = "09:00:00"
    with pytest.raises(requests.exceptions.RequestException):
        get_buses_data(start_time, end_time)


def test_get_buses_data_invalid_date_format():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = [
            {"ordem": "1001", "linha": "A", "datahora": "2024-09-01T08:30:00"}
        ]

        start_time = "08:00:00"
        end_time = "09:00:00"
        result = get_buses_data(start_time, end_time)
        assert isinstance(result, list)
