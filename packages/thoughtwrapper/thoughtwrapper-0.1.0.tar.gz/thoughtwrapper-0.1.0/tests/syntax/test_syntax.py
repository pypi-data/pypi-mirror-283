# Copyright (C) 2024 Lucas Hinderberger
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
from pathlib import Path

import pytest
import thoughtwrapper
from thoughtwrapper.extras import template

dirpath = Path(__file__).parent.resolve()

with open(dirpath.joinpath("hello-expected.html"), "rb") as f:
    hello_expected = f.read()
with open(dirpath.joinpath("nolang-expected.html"), "rb") as f:
    nolang_expected = f.read()

routes = [
    {
        "path": "hello.html",
        "content": hello_expected
    },
    {
        "path": "nolang.html",
        "content": nolang_expected
    },
]


@pytest.mark.parametrize("route", routes)
def test_build(route):
    result = subprocess.run(
        [
            "thoughtwrapper",
            "-b", dirpath.joinpath("build.py"),
            "build",
            "-s", route["path"]
        ],
        capture_output=True
    )

    assert result.returncode == 0
    assert result.stdout == route["content"]
