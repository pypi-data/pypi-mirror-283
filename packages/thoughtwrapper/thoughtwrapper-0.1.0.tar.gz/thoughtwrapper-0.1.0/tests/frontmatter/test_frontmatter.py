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

import jinja2
import pytest
import thoughtwrapper
from thoughtwrapper.extras import template

dirpath = Path(__file__).parent.resolve()

routes = [
    {
        "path": "dash.txt",
        "content": b"Hello World! foo.bar: baz"
    },
    {
        "path": "plus.txt",
        "content": b"Hallo Welt! der.die: das"
    },
    {
        "path": "passthrough.txt",
        "content": b"passthrough\nbar: \nend."
    },
    {
        "path": "empty.txt",
        "content": b"empty\nfoo: \nend.",
    },
    {
        "path": "merge.txt",
        "content": b"foo: hello\nbar.baz: 123\nbar.extra: \nend."
    },
    {
        "path": "multi.txt",
        "content": b"multiple\n---\nfoo: hello\nbar.baz: world"
    }
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
