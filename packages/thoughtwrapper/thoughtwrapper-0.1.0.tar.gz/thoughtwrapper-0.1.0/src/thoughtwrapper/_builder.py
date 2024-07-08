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
import json
import logging
import os
import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import BinaryIO, Optional
from ._pipeline import Pipeline
from ._source import FileSource, Source

_BUILDPARAM_KEY_OUTPUT = "output"
_BUILDPARAM_KEY_SINGLE = "single"

EXIT_CODE_NOT_FOUND = 2
"""An exit code that indicates that a route was not found."""


class RouteNotFound(Exception):
    """RouteNotFound indicates that a Builder could not find a route."""


class Builder:
    """Holder of config, logic and CLI for the build process.

    The Builder class is the core component of a build.py file for
    thoughtwrapper. It will hold all configured routes, how to build
    each route and the process logic for executing a build, plus the CLI
    implementation for build.py.

    For the overall thoughtwrapper CLI, look at the thoughtwrapper._cli
    module.
    """

    def __init__(self):
        """Create a new Builder."""
        self._routes = {}

    def add_route(
        self,
        pipeline: Pipeline, url_path: str, source: Source | str | os.PathLike
    ):
        """Add a new route to the build configuration.

        If route points to an existing route, that existing route will
        be overwritten.

        :param pipeline: The pipeline that shall be executed for this
            route.
        :param route: The URL path of the new route. Leading and
            trailing slashes are ignored.
        :param source: The source of the content that is to be rendered
            to the given route. If a string or PathLike is given, it will be
            used to initialize a new :class:`FileSource`.
        """
        if isinstance(source, (os.PathLike, str)):
            source = FileSource(source)

        self._routes[url_path] = _Route(url_path, pipeline, source)

    def add_routes(
        self, pipeline: Pipeline, routes: dict[str, Source | str | os.PathLike]
    ):
        """Add multiple routes to the build configuration.

        :param pipeline: The pipeline that shall be executed for all
            given routes.
        :param routes: A dictionary of sources, keyed by route URL path.
            For more details, refer to the documentation of
            :meth:`add_route`.
        """
        for route, source in routes.items():
            self.add_route(pipeline, route, source)

    def build(self, output_path: str | os.PathLike):
        """Build the entire site to output_path."""
        output_path = Path(output_path)

        for url_path, route in self._routes.items():
            route_output_path = output_path.joinpath(url_path)
            with _open_output(route_output_path) as output:
                output.write(route.build())

    def build_single(self, route_urlpath: str, output: BinaryIO):
        """Build a single route and write to the given output."""
        try:
            entry = self._routes[route_urlpath]
        except KeyError as e:
            raise RouteNotFound(f"Route not found: {route_urlpath}") from e

        output.write(entry.build())

    def build_single_fallback(self, routes: list[str], output: BinaryIO):
        """Build a single route based on a list of possible paths."""
        for route in routes:
            try:
                self.build_single(route, output)
                return
            except RouteNotFound:
                pass

        routes_joined = ', '.join(routes)
        raise RouteNotFound(
            f"Route and fallback(s) not found: {routes_joined}"
        )

    def run(self, argv=None):
        """Run the build CLI.

        This should be the last call in your build.py file, after
        setting up your Builder.

        If no value is given for argv, the arguments to the current
        process (excluding binary path) will be used.
        """
        if argv is None:
            argv = sys.argv[1:]

        arg_parser = argparse.ArgumentParser(
            prog="thoughtwrapper build script",
            usage="Please use the thoughtwrapper CLI instead of directly "
                  "calling the build script"
        )
        arg_parser.add_argument(
            "params_json",
            help="build parameters, as encoded by the thoughtwrapper CLI",
            type=str
        )
        args = arg_parser.parse_args(args=argv)

        params = buildparams_from_json(args.params_json)
        params.validate()

        try:
            if params.single is None:
                self.build(params.output)
            else:
                with _open_output(params.output) as output:
                    if isinstance(params.single, list):
                        self.build_single_fallback(params.single, output)
                    else:
                        self.build_single(params.single, output)
        except RouteNotFound as e:
            print(e)
            sys.exit(EXIT_CODE_NOT_FOUND)


class BuildParams:
    """
    BuildParams holds parameters for Builder.

    It also provides functionality for de- and encoding parameters from
    and to JSON and for validating a given set of parameters.
    """

    def __init__(
        self,
        output: Optional[Path] = None,
        single: Optional[str | list[str]] = None
    ):
        """Create new BuildParams.

        The parameters given will be used to initialize instance
        properties with the same name.

        :param output: An absolute path pointing to the desired output
            location. Setting output to a non-None value will turn it
            into an absolute Path.
        :param single: A path that, if set, limits the build to a single
            site. That single site is the one pointed to by this path.
            If multiple paths are given, the first entry shall be treated
            as the preferred path and all further entries as fallbacks
            in descending order of priority.
        """
        self.output = output
        self.single = single

    @property
    def output(self) -> Optional[Path]:
        return self._output

    @output.setter
    def output(self, v: Optional[str | bytes | os.PathLike]):
        if v is not None:
            v = Path(v).absolute()
        self._output = v

    def to_json(self) -> str:
        """Encode the BuildParams to a JSON string."""
        d = {}

        if self.single is not None:
            d[_BUILDPARAM_KEY_SINGLE] = self.single
        if self.output is not None:
            d[_BUILDPARAM_KEY_OUTPUT] = str(self.output)

        return json.dumps(d)

    def validate(self):
        """Raise an error if the given BuildParams are not valid."""
        if self.single is None and self.output is None:
            raise RuntimeError(
                f'"{_BUILDPARAM_KEY_OUTPUT}" must be set if '
                f'"{_BUILDPARAM_KEY_SINGLE}" is not set'
            )


def buildparams_from_json(s: str) -> BuildParams:
    """Decode BuildParams from a JSON string."""
    d = json.loads(s)

    if not isinstance(d, dict):
        raise RuntimeError("build params are not a JSON object")

    p = BuildParams()

    for k, v in d.items():
        if k == _BUILDPARAM_KEY_SINGLE:
            p.single = v
        elif k == _BUILDPARAM_KEY_OUTPUT:
            p.output = v
        else:
            raise RuntimeError(f'unknown build param "{k}"')

    return p


class _Route:  # pylint: disable=too-few-public-methods
    """An entry in Builder's routes dict representing a configured route."""

    def __init__(self, url_path: str, pipeline: Pipeline, source: Source):
        """Create a new _Route."""
        self.url_path = url_path
        self.pipeline = pipeline
        self.source = source

        self.dependencies = None
        self.last_built_at = None

    def build(self) -> bytes:
        """Build this route, update build metadata properties."""
        try:
            # TODO: If dependencies are not dynamic, cache build results.
            #   Invalidate if
            #   modification time of any dependency > last_built_at.

            # last_built_at is set before the build, so that the build cache
            # can be invalidated in case the input files change during the
            # build.
            self.last_built_at = datetime.now()

            logging.info("Building route %s", self.url_path)
            metadata = {"_tw": {"url_path": self.url_path}}
            output, deps = self.pipeline.run(self.source, metadata=metadata)

            self.dependencies = deps

            return output
        except Exception as e:
            raise RuntimeError(f"Could not build route {self.url_path}") from e


@contextmanager
def _open_output(path: str | os.PathLike) -> BinaryIO:
    if path is None:
        yield sys.stdout.buffer
        return

    f = None
    try:
        dirpath = Path(path).parent
        os.makedirs(dirpath, exist_ok=True)
        f = open(path, "wb")
    except Exception as e:
        raise RuntimeError(
            f'Could not open output file at "{path}"'
        ) from e

    yield f

    f.close()
