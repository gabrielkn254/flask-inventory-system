import sys
from unittest.mock import patch

import cli


def test_cli_list(capsys):
    with patch("cli.command_list") as mock_command:
        with patch.object(sys, "argv", ["cli.py", "list"]):
            cli.cli()

    mock_command.assert_called_once()

    args = mock_command.call_args[0][0]
    assert hasattr(args, "func")


def test_cli_view():
    with patch("cli.command_view") as mock_command:
        with patch.object(
            sys,
            "argv",
            ["cli.py", "view", "--id", "1"]
        ):
            cli.cli()

    mock_command.assert_called_once()

    args = mock_command.call_args[0][0]
    assert args.id == "1"


def test_cli_add():
    with patch("cli.command_add") as mock_command:
        with patch.object(
            sys,
            "argv",
            [
                "cli.py",
                "add",
                "--name", "Test Product",
                "--price", "100",
                "--quantity", "10"
            ]
        ):
            cli.cli()

    mock_command.assert_called_once()

    args = mock_command.call_args[0][0]

    assert args.name == "Test Product"
    assert args.price == "100"
    assert args.quantity == "10"


def test_cli_update():
    with patch("cli.command_update") as mock_command:
        with patch.object(
            sys,
            "argv",
            [
                "cli.py",
                "update",
                "--id", "1",
                "--barcode", "123456789",
                "--name", "Updated Product",
                "--price", "150",
                "--quantity", "20",
                "--image", "new-image",
                "--categories", "Updated Category",
                "--brands", "Updated Brand",
                "--ingredients", "Water"
            ]
        ):
            cli.cli()

    mock_command.assert_called_once()

    args = mock_command.call_args[0][0]

    assert args.id == "1"
    assert args.barcode == "123456789"
    assert args.name == "Updated Product"
    assert args.price == "150"
    assert args.quantity == "20"
    assert args.image == "new-image"
    assert args.categories == "Updated Category"
    assert args.brands == "Updated Brand"
    assert args.ingredients == "Water"


def test_cli_delete():
    with patch("cli.command_delete") as mock_command:
        with patch.object(
            sys,
            "argv",
            ["cli.py", "delete", "--id", "1"]
        ):
            cli.cli()

    mock_command.assert_called_once()

    args = mock_command.call_args[0][0]
    assert args.id == "1"


def test_cli_search_by_name():
    with patch("cli.command_search") as mock_command:
        with patch.object(
            sys,
            "argv",
            ["cli.py", "search", "--name", "Test Product"]
        ):
            cli.cli()

    mock_command.assert_called_once()

    args = mock_command.call_args[0][0]
    assert args.name == "Test Product"


def test_cli_search_by_barcode():
    with patch("cli.command_search") as mock_command:
        with patch.object(
            sys,
            "argv",
            ["cli.py", "search", "--barcode", "123456789"]
        ):
            cli.cli()

    mock_command.assert_called_once()

    args = mock_command.call_args[0][0]
    assert args.barcode == "123456789"


def test_cli_no_command(capsys):
    with patch.object(sys, "argv", ["cli.py"]):
        cli.cli()

    captured = capsys.readouterr()

    assert "Inventory Management CLI" in captured.out