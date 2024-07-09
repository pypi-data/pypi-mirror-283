# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for functions to save image from data url.

"""
import base64
import re
from pathlib import Path

import pytest

from qbraid_core.services.environments.create import save_image_from_data_url


def test_save_image_from_data_url(tmp_path):
    # Create a simple 1x1 pixel image in PNG format
    image_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xdac`\x00\x00\x00\x02\x00\x01\xe2!\xbc\x33\x00\x00\x00\x00IEND\xaeB`\x82"
    data_url = f"data:image/png;base64,{base64.b64encode(image_data).decode('utf-8')}"

    # Define the output path
    output_path = tmp_path / "output_image.png"

    # Call the function
    save_image_from_data_url(data_url, str(output_path))

    # Check that the file was created
    assert output_path.exists()

    # Check that the content is correct
    with open(output_path, "rb") as file:
        assert file.read() == image_data


def test_save_image_from_data_url_invalid_data_url():
    invalid_data_url = "data:image/png;base64,invalidbase64data"

    with pytest.raises(ValueError) as exc_info:
        save_image_from_data_url(invalid_data_url, "output_image.png")

    # Check if the error message is exactly "Invalid Data URL"
    assert str(exc_info.value) == "Invalid Data URL"


def test_save_image_from_data_url_creates_directory(tmp_path):
    # Create a simple 1x1 pixel image in PNG format
    image_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xdac`\x00\x00\x00\x02\x00\x01\xe2!\xbc\x33\x00\x00\x00\x00IEND\xaeB`\x82"
    data_url = f"data:image/png;base64,{base64.b64encode(image_data).decode('utf-8')}"

    # Define the output path
    nested_output_path = tmp_path / "nested_dir" / "output_image.png"

    # Call the function
    save_image_from_data_url(data_url, str(nested_output_path))

    # Check that the nested directory and file were created
    assert nested_output_path.exists()

    # Check that the content is correct
    with open(nested_output_path, "rb") as file:
        assert file.read() == image_data
