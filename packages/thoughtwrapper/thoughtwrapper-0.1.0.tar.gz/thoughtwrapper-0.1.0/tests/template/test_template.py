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
from thoughtwrapper.extras import frontmatter, template

dirpath = Path(__file__).parent.resolve()

routes = [
    {
        "path": "autoescape.html",
        "sourcepath": dirpath.joinpath("templates/autoescape.jinja"),
        "content": b"This checks if &lt;b&gt;auto-escaping&lt;/b&gt; is "
                   b"enabled.",
        "dependencies": [dirpath.joinpath("templates/autoescape.jinja")]
    },
    {
        "path": "basic.txt",
        "sourcepath": dirpath.joinpath("templates/basic.jinja"),
        "content": b"This is a very simple template in the Jinja templating "
                   b"language.",
        "dependencies": [dirpath.joinpath("templates/basic.jinja")]
    },
    {
        "path": "include.txt",
        "sourcepath": dirpath.joinpath("templates/include.jinja"),
        "content": b"Including: This is a very simple template in the Jinja "
                   b"templating language. End.",
        "dependencies": [
            dirpath.joinpath("templates/include.jinja"),
            dirpath.joinpath("templates/basic.jinja")
        ]
    },
    {
        "path": "include_indirect.txt",
        "sourcepath": dirpath.joinpath("templates/include_indirect.jinja"),
        "content": b"Indirect: Including: This is a very simple template in "
                   b"the Jinja templating language. End. End indirect.",
        "dependencies": [
            dirpath.joinpath("templates/include_indirect.jinja"),
            dirpath.joinpath("templates/include.jinja"),
            dirpath.joinpath("templates/basic.jinja")
        ]
    },
    {
        "path": "layout.txt",
        "sourcepath": dirpath.joinpath("templates/layout_child.jinja"),
        "content": b"This is a layout. Content from layout child. End.",
        "dependencies": [
            dirpath.joinpath("templates/layout_child.jinja"),
            dirpath.joinpath("templates/layout_parent.jinja")
        ]
    },
    {
        "path": "metadata.txt",
        "sourcepath": dirpath.joinpath("templates/metadata.jinja"),
        "content": b"The value of foo is: bar",
        "dependencies": [dirpath.joinpath("templates/metadata.jinja")]
    },
    {
        "path": "no-autoescape.html",
        "sourcepath": dirpath.joinpath("templates/autoescape.jinja"),
        "content": b"This checks if <b>auto-escaping</b> is enabled.",
        "dependencies": [dirpath.joinpath("templates/autoescape.jinja")]
    },
    {
        "path": "wrap-all-defaults.txt",
        "sourcepath": dirpath.joinpath("wrap-all-defaults.txt"),
        "content":
            b"This is a layout. Wrapped content.\n Some other placeholder. "
            b"End.",
        "dependencies": [
            dirpath.joinpath("wrap-all-defaults.txt"),
            dirpath.joinpath("templates/wrap_layout.jinja")
        ]
    },
    {
        "path": "wrap-block-override.txt",
        "sourcepath": dirpath.joinpath("wrap-block-override.txt"),
        "content": b"This is a layout. A placeholder. Wrapped content.\n End.",
        "dependencies": [
            dirpath.joinpath("wrap-block-override.txt"),
            dirpath.joinpath("templates/wrap_layout.jinja")
        ]
    },
    {
        "path": "wrap-key-overrides.txt",
        "content": b"This is a layout. A placeholder. Wrapped content.\n End.",
    },

    # note that Jinja trims the trailing line break by default.
    {
        "path": "wrap-passthrough.txt",
        "content": b"Wrapped content.",
    },
    {
        "path": "wrap-disabled.txt",
        "content": b"Wrapped content.",
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


@pytest.mark.parametrize("route", [x for x in routes if "sourcepath" in x])
def test_dependencies(route):
    template_dir = dirpath.joinpath("templates")

    pipeline = thoughtwrapper.Pipeline()
    pipeline.add_filter(frontmatter.Loader())
    pipeline.add_filter(template.Engine(
        {
            "loader": jinja2.FileSystemLoader(str(template_dir)),
        },
        layout_wrapper_enabled=True,
    ))

    source = thoughtwrapper.FileSource(route["sourcepath"])
    _, dependencies = pipeline.run(source)

    expected_deps = [
        str(Path(x).resolve()) for x in route["dependencies"]
    ]

    assert dependencies == thoughtwrapper.Dependencies(*expected_deps)
