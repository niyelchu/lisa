from pathlib import Path

from lisa import TestCaseMetadata, TestSuite, TestSuiteMetadata
from lisa.executable import CustomScript, CustomScriptBuilder


@TestSuiteMetadata(
    area="demo",
    category="simple",
    description="""
    This test suite run a script
    """,
    tags=["demo"],
)
class WithScript(TestSuite):
    @property
    def skiprun(self) -> bool:
        node = self.environment.default_node
        return not node.is_linux

    def before_suite(self) -> None:
        self._echo_script = CustomScriptBuilder(
            Path(__file__).parent.joinpath("scripts"), ["echo.sh"]
        )

    @TestCaseMetadata(
        description="""
        this test case run script on test node.
        """,
        priority=1,
    )
    def script(self) -> None:
        node = self.environment.default_node
        script: CustomScript = node.tools[self._echo_script]
        result = script.run()
        self._log.info(f"result1 stdout: {result}")
        # the second time should be faster, without uploading
        result = script.run()
        self._log.info(f"result2 stdout: {result}")
