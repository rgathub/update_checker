"""Tests for the update_checker package."""

from unittest import mock

import pytest
import requests

from update_checker import UpdateChecker, update_check

PACKAGE = "praw"


def mock_response(*, latest_version: str = "5.0.0", response: mock.MagicMock) -> None:
    response.json = mock.Mock(
        return_value={"releases": {"0.0.1": [], latest_version: []}},
    )
    response.status_code = 200


@mock.patch("requests.get")
def test_checker_check__no_update_to_beta_version(mock_get: mock.MagicMock) -> None:
    mock_response(latest_version="3.7.0b1", response=mock_get.return_value)
    checker = UpdateChecker(bypass_cache=True)
    assert checker.check(package_name=PACKAGE, package_version="3.6") is None


@mock.patch("requests.get")
def test_checker_check__successful(mock_get: mock.MagicMock) -> None:
    mock_response(response=mock_get.return_value)
    checker = UpdateChecker(bypass_cache=True)
    result = checker.check(package_name=PACKAGE, package_version="1.0.0")
    assert result.available_version == "5.0.0"


@mock.patch("requests.get")
def test_checker_check__unsuccessful(mock_get: mock.MagicMock) -> None:
    mock_get.side_effect = requests.exceptions.RequestException
    checker = UpdateChecker(bypass_cache=True)
    assert checker.check(package_name=PACKAGE, package_version="1.0.0") is None


@mock.patch("requests.get")
def test_checker_check__update_to_beta_version_from_beta_version(
    mock_get: mock.MagicMock,
) -> None:
    mock_response(latest_version="4.0.0b5", response=mock_get.return_value)
    checker = UpdateChecker(bypass_cache=True)
    result = checker.check(package_name=PACKAGE, package_version="4.0.0b4")
    assert result.available_version == "4.0.0b5"


@mock.patch("requests.get")
def test_checker_check__update_to_rc_version_from_beta_version(
    mock_get: mock.MagicMock,
) -> None:
    mock_response(latest_version="4.0.0rc1", response=mock_get.return_value)
    checker = UpdateChecker(bypass_cache=True)
    result = checker.check(package_name=PACKAGE, package_version="4.0.0b4")
    assert result.available_version == "4.0.0rc1"


@mock.patch("requests.get")
def test_update_check__successful__has_no_update(
    mock_get: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_response(latest_version="0.0.2", response=mock_get.return_value)
    update_check(PACKAGE, "0.0.2", bypass_cache=True)
    assert not capsys.readouterr().err


@mock.patch("requests.get")
def test_update_check__successful__has_update(
    mock_get: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_response(response=mock_get.return_value)
    update_check(PACKAGE, "0.0.1", bypass_cache=True)
    assert (
        capsys.readouterr().err
        == "Version 0.0.1 of praw is outdated. Version 5.0.0 is available.\n"
    )


@mock.patch("requests.get")
def test_update_check__unsuccessful(
    mock_get: mock.MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_get.side_effect = requests.exceptions.RequestException
    update_check(PACKAGE, "0.0.1", bypass_cache=True)
    assert not capsys.readouterr().err
