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

import http.server
import mimetypes
import subprocess
import sys
from pathlib import Path, PurePosixPath
from thoughtwrapper import BuildParams, EXIT_CODE_NOT_FOUND


DEFAULT_INDEX_FILENAMES = ["index.html", "index.htm"]
"""The default filenames that the dev server probes to find an index page."""


def build_dev_server(
    buildscript_path: str | bytes | Path,
    listen_address: tuple[str, int],
    index_filenames: list[str] = None
) -> http.server.ThreadingHTTPServer:
    """Build an HTTP server for local authoring of a thoughtwrapper site."""
    if index_filenames is None:
        index_filenames = DEFAULT_INDEX_FILENAMES.copy()

    server = http.server.ThreadingHTTPServer(listen_address, _DevServerHandler)
    server.thoughtwrapper = {
        "index_filenames": index_filenames,
        "buildscript_path": Path(buildscript_path)
    }
    return server


class _DevServerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # pylint: disable=C0103
        """Handle GET requests for thoughtwrapper dev server."""
        index_filenames = self.server.thoughtwrapper["index_filenames"]
        path = PurePosixPath(self.path.split("?", maxsplit=1)[0])

        routelist = [] if self.path.endswith("/") else [path]
        routelist += [path.joinpath(ifn) for ifn in index_filenames]

        routelist = [str(r).lstrip("/") for r in routelist]

        self._try_serve_route(routelist)

    def _try_serve_route(self, routelist: list[str]):
        buildscript_path = self.server.thoughtwrapper["buildscript_path"]

        # FIXME: Only use content type of accepted route
        content_type, content_encoding = (None, None)
        for route in routelist:
            content_type, content_encoding = mimetypes.guess_type(route)
            if content_type is not None:
                break

        if content_type is None:
            content_type = "application/octet-stream"

        buildparams = BuildParams(single=routelist)

        result = subprocess.run([
            sys.executable, buildscript_path,
            buildparams.to_json()
        ], capture_output=True, check=False, cwd=buildscript_path.parent)

        output = result.stdout
        if len(result.stderr) > 0:
            print(result.stderr.decode("UTF-8"), file=sys.stderr)
        if result.returncode == EXIT_CODE_NOT_FOUND:
            self.send_response(404)
            output = b"Not Found"
        elif result.returncode != 0:
            self.send_response(500)
            output = result.stderr
        else:
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Encoding", content_encoding)
            self.send_header("Content-Length", len(result.stdout))

        self.end_headers()
        self.wfile.write(output)
