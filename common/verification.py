"""
Verification framework for reproducing results from PMU placement papers.

Each paper defines expected results (from tables/figures) and a solver function.
The framework runs the solver on standard test systems and compares outputs
against the published values, producing a structured report.
"""

import datetime
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .test_systems import ALL_SYSTEMS


@dataclass
class ExpectedResult:
    """A single expected result from a published paper.

    Attributes
    ----------
    system_name : str
        Name of the test system (must match a key in ALL_SYSTEMS).
    metric : str
        What is being compared: 'min_pmus', 'pmu_locations', 'ratio', etc.
    expected_value : Any
        The value reported in the paper.
    table_ref : str or None
        Reference to the table in the paper (e.g., "Table 1").
    figure_ref : str or None
        Reference to the figure in the paper.
    tolerance : float
        Acceptable deviation for numeric comparisons.
    actual_value : Any
        Populated after verification.
    passed : bool or None
        Populated after verification.
    """
    system_name: str
    metric: str
    expected_value: Any
    table_ref: Optional[str] = None
    figure_ref: Optional[str] = None
    tolerance: float = 0
    actual_value: Any = None
    passed: Optional[bool] = None


class PaperVerification:
    """Framework for verifying reproducibility of a single paper's results.

    Usage
    -----
    >>> v = PaperVerification('paper1', 'Baldwin et al.', 1993)
    >>> v.add_expected_result('IEEE 14-Bus', 'min_pmus', 3, table_ref='Table 1')
    >>> v.run_verification(solve_bisecting_search_baldwin)
    >>> v.generate_report()
    >>> v.assert_all_pass()
    """

    def __init__(self, paper_id: str, paper_title: str, paper_year: int):
        self.paper_id = paper_id
        self.paper_title = paper_title
        self.paper_year = paper_year
        self.expected_results: List[ExpectedResult] = []
        self.solver_results: Dict[str, Dict] = {}  # system_name -> solver output
        self._report: Optional[str] = None

    def add_expected_result(
        self,
        system_name: str,
        metric: str,
        expected_value: Any,
        table_ref: Optional[str] = None,
        figure_ref: Optional[str] = None,
        tolerance: float = 0,
    ) -> None:
        """Register an expected result from the paper."""
        self.expected_results.append(
            ExpectedResult(
                system_name=system_name,
                metric=metric,
                expected_value=expected_value,
                table_ref=table_ref,
                figure_ref=figure_ref,
                tolerance=tolerance,
            )
        )

    def run_verification(
        self,
        solver_func: Callable,
        systems: Optional[Dict[str, Dict]] = None,
    ) -> None:
        """Run solver on all required test systems and compare with expected results.

        Parameters
        ----------
        solver_func : callable
            Function with signature (n_buses, branches, zero_injection_buses) -> dict.
            The returned dict must have at least 'n_pmus', 'pmu_buses', and optionally
            'ratio'.
        systems : dict or None
            Override test systems. Defaults to ALL_SYSTEMS.
        """
        if systems is None:
            systems = ALL_SYSTEMS

        # Determine which systems we need to run
        needed_systems = {er.system_name for er in self.expected_results}

        for sys_name in needed_systems:
            if sys_name not in systems:
                print(f"WARNING: System '{sys_name}' not found in test systems.")
                continue
            if sys_name in self.solver_results:
                continue  # already solved

            sys = systems[sys_name]
            print(f"Running solver on {sys_name}...")
            result = solver_func(
                n_buses=len(sys["buses"]),
                branches=sys["branches"],
                zero_injection_buses=sys.get("zero_injection_buses", []),
            )
            # Compute ratio if not present
            if "ratio" not in result and result.get("n_pmus") is not None:
                result["ratio"] = result["n_pmus"] / len(sys["buses"])
            self.solver_results[sys_name] = result

        # Compare expected vs actual
        for er in self.expected_results:
            if er.system_name not in self.solver_results:
                er.passed = False
                er.actual_value = "SYSTEM NOT FOUND"
                continue

            result = self.solver_results[er.system_name]

            if er.metric == "min_pmus":
                er.actual_value = result.get("n_pmus")
            elif er.metric == "pmu_locations":
                er.actual_value = result.get("pmu_buses")
            elif er.metric == "ratio":
                er.actual_value = result.get("ratio")
            else:
                er.actual_value = result.get(er.metric)

            # Comparison
            if er.actual_value is None:
                er.passed = False
            elif isinstance(er.expected_value, (int, float)):
                if er.tolerance > 0:
                    er.passed = abs(er.actual_value - er.expected_value) <= er.tolerance
                else:
                    er.passed = er.actual_value == er.expected_value
            elif isinstance(er.expected_value, list):
                er.passed = sorted(er.actual_value) == sorted(er.expected_value)
            else:
                er.passed = er.actual_value == er.expected_value

    def generate_report(self) -> str:
        """Generate a markdown verification report.

        Returns
        -------
        report : str
            Markdown-formatted report.
        """
        lines = [
            f"# Verification Report: {self.paper_title} ({self.paper_year})",
            f"Paper ID: `{self.paper_id}`",
            f"Generated: {datetime.datetime.now().isoformat(timespec='seconds')}",
            "",
            "## Results",
            "",
            "| System | Metric | Expected | Actual | Ref | Status |",
            "|--------|--------|----------|--------|-----|--------|",
        ]

        n_pass = 0
        n_fail = 0
        for er in self.expected_results:
            status = "PASS" if er.passed else "FAIL"
            if er.passed:
                n_pass += 1
            else:
                n_fail += 1

            ref = er.table_ref or er.figure_ref or ""
            exp_str = self._fmt(er.expected_value)
            act_str = self._fmt(er.actual_value)
            lines.append(
                f"| {er.system_name} | {er.metric} | {exp_str} | {act_str} "
                f"| {ref} | {'✓' if er.passed else '✗'} {status} |"
            )

        lines.extend([
            "",
            f"## Summary: {n_pass} passed, {n_fail} failed, "
            f"{len(self.expected_results)} total",
        ])

        # Solver details
        lines.extend(["", "## Solver Details", ""])
        for sys_name, result in self.solver_results.items():
            lines.append(f"### {sys_name}")
            lines.append(f"- PMUs: {result.get('n_pmus')}")
            pmu_str = ", ".join(str(b) for b in result.get("pmu_buses", []))
            lines.append(f"- Locations: [{pmu_str}]")
            if "ratio" in result:
                lines.append(f"- Ratio: {result['ratio']:.4f}")
            lines.append("")

        self._report = "\n".join(lines)
        print(self._report)
        return self._report

    def assert_all_pass(self) -> None:
        """Raise AssertionError if any verification failed."""
        failed = [er for er in self.expected_results if not er.passed]
        if failed:
            msgs = []
            for er in failed:
                msgs.append(
                    f"  {er.system_name}/{er.metric}: "
                    f"expected={er.expected_value}, actual={er.actual_value}"
                )
            raise AssertionError(
                f"{len(failed)} verification(s) failed for "
                f"'{self.paper_title}':\n" + "\n".join(msgs)
            )
        print(f"All {len(self.expected_results)} verifications passed.")

    @staticmethod
    def _fmt(value: Any) -> str:
        if isinstance(value, float):
            return f"{value:.4f}"
        if isinstance(value, list):
            return str(value)
        return str(value)
