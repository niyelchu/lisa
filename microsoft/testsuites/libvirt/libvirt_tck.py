# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
from pathlib import Path
from typing import Any

from lisa import (
    Environment,
    Logger,
    Node,
    TestCaseMetadata,
    TestSuite,
    TestSuiteMetadata,
)
from lisa.operating_system import CBLMariner, Ubuntu
from lisa.testsuite import TestResult
from lisa.tools import Lscpu
from lisa.util import SkippedException
from microsoft.testsuites.libvirt.libvirt_tck_tool import LibvirtTck


@TestSuiteMetadata(
    area="libvirt",
    category="community",
    description="""
    Runs the libvirt TCK (Technology Compatibility Kit) tests. It is a suite
    of functional/integration tests designed to test a libvirt driver's complicance
    with API semantics, distro configuration etc.

    More info: https://gitlab.com/libvirt/libvirt-tck/-/blob/master/README.rst
    """,
)
class LibvirtTckSuite(TestSuite):
    def before_case(self, log: Logger, **kwargs: Any) -> None:
        node = kwargs["node"]
        if not isinstance(node.os, (Ubuntu, CBLMariner)):
            raise SkippedException(
                f"Libvirt TCK suite is not implemented in LISA for {node.os.name}"
            )
        # ensure virtualization is enabled in hardware before running tests
        virtualization_enabled = node.tools[Lscpu].is_virtualization_enabled()
        if not virtualization_enabled:
            raise SkippedException("Virtualization is not enabled in hardware")

    @TestCaseMetadata(
        description="""
        Runs the Libvirt TCK (Technology Compatibility Kit) tests with the default
        configuration i.e. the tests will exercise the qemu driver in libvirt.
        """,
        priority=3,
    )
    def verify_libvirt_tck(
        self,
        log: Logger,
        node: Node,
        environment: Environment,
        log_path: Path,
        result: TestResult,
    ) -> None:
        node.tools[LibvirtTck].run_tests(result, environment, log_path)
