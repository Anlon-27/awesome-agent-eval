# -*- coding: utf-8 -*-
from typing import Dict, Any
from agent_eval.schema import EvalReport
from tabulate import tabulate


class ReportGenerator:
    """
    Generates terminal summary tables, JSON payloads, and GitHub Flavored Markdown reports.
    """

    @staticmethod
    def to_terminal(report: EvalReport) -> str:
        headers = ["Task ID", "Layer", "Status", "Metrics Summary"]
        rows = []
        for c in report.case_evaluations:
            status = "✅ PASS" if c.passed else "❌ FAIL"
            metrics_str = ", ".join([f"{m.metric_name}: {m.score:.2f}" for m in c.metric_results])
            rows.append([c.test_case.task_id, c.test_case.layer, status, metrics_str])

        table = tabulate(rows, headers=headers, tablefmt="github")
        summary = (
            f"\n📊 === Eval Suite: {report.suite_name} ===\n"
            f"Total: {report.total_cases} | Passed: {report.passed_cases} | "
            f"Pass Rate: {report.pass_rate * 100:.1f}% | Duration: {report.duration_sec:.2f}s\n\n"
        )
        return summary + table

    @staticmethod
    def to_markdown(report: EvalReport) -> str:
        lines = [
            f"# 📊 Evaluation Report: {report.suite_name}",
            "",
            f"- **Pass Rate**: {report.pass_rate * 100:.1f}% ({report.passed_cases}/{report.total_cases})",
            f"- **Total Duration**: {report.duration_sec:.2f}s",
            "",
            "## Case Breakdown",
            "",
            "| Task ID | Layer | Status | Metric Scores | Details |",
            "| :--- | :---: | :---: | :--- | :--- |",
        ]

        for c in report.case_evaluations:
            status = "✅ PASS" if c.passed else "❌ FAIL"
            scores = ", ".join([f"`{m.metric_name}`: {m.score:.2f}" for m in c.metric_results])
            reasons = "; ".join([m.reason for m in c.metric_results if m.reason])
            lines.append(f"| `{c.test_case.task_id}` | `{c.test_case.layer}` | {status} | {scores} | {reasons} |")

        return "\n".join(lines) + "\n"
