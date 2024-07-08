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

import argparse
import os
import subprocess
import sys
from pathlib import Path
from thoughtwrapper import \
    __version__ as version, \
    DEFAULT_INDEX_FILENAMES, BuildParams, build_dev_server


def main():
    """Run the thoughtwrapper CLI."""
    arg_parser = argparse.ArgumentParser(
        prog="thoughtwrapper",
        description="A Static Site Generator for Tinkerers",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    arg_parser.add_argument(
        "-b", "--builder",
        help="where to find the builder script for your site",
        default=os.path.join(os.getcwd(), "build.py")
    )

    subparsers = arg_parser.add_subparsers(
        title="COMMAND",
        dest="command",
        required=True
    )

    build_parser = subparsers.add_parser(
        "build",
        help="builds your site (or parts thereof)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    build_parser.add_argument(
        "-o", "--output",
        help='output directory (or file, if --single is set), defaults '
             'to the "target" subdirectory of the current working '
             'directory (or stdout if --single is set)'
    )
    build_parser.add_argument(
        "-s", "--single",
        help="only build a single page, with the given URL path, or - "
             "if multiple comma-separated paths are given - with the "
             "first URL path in that list that points to an existing "
             "route (outputs to stdout by default, override with "
             "--output)",
        default=argparse.SUPPRESS
    )

    serve_parser = subparsers.add_parser(
        "serve",
        help="runs a development server for your site",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    serve_parser.add_argument(
        "--host",
        default="localhost",
        help="the host to listen to"
    )
    serve_parser.add_argument(
        "--index-filenames",
        help="the filenames that the dev server probes to find an index page",
        default=",".join(DEFAULT_INDEX_FILENAMES)
    )
    serve_parser.add_argument(
        "-p", "--port",
        type=int,
        default=8080,
        help="the port to listen to"
    )

    subparsers.add_parser(
        "version",
        help="outputs the version of thoughtwrapper you're currently running",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    args = arg_parser.parse_args()

    if args.command == "version":
        print(version)
        sys.exit(0)

    buildscript_path = _determine_buildscript_path(args)
    if not buildscript_path.exists():
        raise RuntimeError(
            f'buildscript at "{buildscript_path}" does not exist'
        )
    if buildscript_path.is_dir():
        raise RuntimeError(
            f'buildscript path "{buildscript_path}" points to directory'
        )

    match args.command:
        case "build":
            buildparams = _prepare_buildscript_params(args)

            result = subprocess.run([
                sys.executable, buildscript_path,
                buildparams.to_json()
            ], check=False, cwd=buildscript_path.parent)

            sys.exit(result.returncode)
        case "serve":
            server = build_dev_server(
                buildscript_path,
                (args.host, args.port),
                index_filenames=args.index_filenames.split(',')
            )
            print(f"Starting server at http://{args.host}:{args.port}")
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("Closing server")
        case _:
            raise RuntimeError(f"encountered unknown command: {args.command}")


def _determine_buildscript_path(args: argparse.Namespace) -> Path:
    buildscript_path =\
        Path.cwd().joinpath("build.py") if args.builder is None\
        else Path(args.builder)
    return buildscript_path.absolute()


def _prepare_buildscript_params(args: argparse.Namespace) -> BuildParams:
    single = None
    if "single" in args:
        single = args.single.split(',') if ',' in args.single else args.single

    output = args.output
    if output is None and single is None:
        output = Path.cwd().joinpath("target")

    return BuildParams(single=single, output=output)
