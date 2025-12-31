#!/usr/bin/env python3
"""
MCP Parameter Validation Script for howie_skills

Validates all MCP tool calls in SKILL.md files against:
- ai_workflow PARAMETER_TRAPS.md
- Known parameter naming patterns
- airis-exec calling conventions

Exit codes:
  0 - All validations passed
  1 - Parameter errors found
  2 - Configuration error

Usage:
  python validate_mcp_params.py --all
  python validate_mcp_params.py skills/airis-web-research/SKILL.md
  python validate_mcp_params.py --all --format markdown > VALIDATION.md
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class ParameterError:
    """Represents a parameter validation error"""
    file_path: str
    line_number: int
    tool_name: str
    wrong_param: str
    correct_param: str
    code_snippet: str
    error_type: str  # "wrong_name", "missing_required", "unknown_tool"


@dataclass
class ValidationReport:
    """Validation report for a single SKILL.md file"""
    file_path: str
    total_calls: int = 0
    errors: List[ParameterError] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    @property
    def accuracy(self) -> float:
        if self.total_calls == 0:
            return 100.0
        return ((self.total_calls - len(self.errors)) / self.total_calls) * 100


class MCPParameterValidator:
    """
    Validates MCP tool calls across all skills

    Features:
    - Cross-reference with PARAMETER_TRAPS.md
    - Extract code blocks from SKILL.md
    - Validate against known patterns
    - Generate detailed error reports
    """

    # Known parameter traps from ai_workflow/PARAMETER_TRAPS.md
    KNOWN_TRAPS = {
        # Serena MCP
        "serena:read_memory": {
            "correct": ["memory_file_name"],
            "wrong": ["path", "name", "filename"],
            "required": ["memory_file_name"]
        },
        "serena:write_memory": {
            "correct": ["memory_file_name", "content"],
            "wrong": ["filename", "path", "text", "data"],
            "required": ["memory_file_name", "content"]
        },
        "serena:find_file": {
            "correct": ["file_mask", "relative_path"],
            "wrong": ["filename", "path", "name", "directory"],
            "required": ["file_mask", "relative_path"]
        },
        "serena:find_symbol": {
            "correct": ["name_path_pattern"],
            "wrong": ["name", "symbol_name", "class_name"],
            "required": ["name_path_pattern"]
        },

        # Magic MCP
        "magic:generate_ui": {
            "correct": ["absolutePathToCurrentFile", "content", "prompt"],
            "wrong": ["path", "currentFile", "file", "filepath"],
            "required": ["absolutePathToCurrentFile", "content", "prompt"]
        },

        # MorphLLM MCP
        "morphllm:query_codebase": {
            "correct": ["repo_path", "query"],
            "wrong": ["path", "project_path", "directory"],
            "required": ["repo_path", "query"]
        },
        "morphllm:get_file_content": {
            "correct": ["repo_path", "file_path"],
            "wrong": ["path", "project_path", "directory"],
            "required": ["repo_path", "file_path"]
        },

        # Memory MCP
        "memory:create_entities": {
            "correct": ["entities"],
            "wrong": ["entity_list", "items"],
            "required": ["entities"]
        },
        "memory:observe": {
            "correct": ["observations"],
            "wrong": ["content", "text", "data"],
            "required": ["observations"]
        },

        # Tavily MCP
        "tavily:search": {
            "correct": ["query", "search_depth", "max_results"],
            "wrong": ["q", "depth", "limit", "count"],
            "required": ["query"]
        },
        "tavily:extract": {
            "correct": ["urls"],
            "wrong": ["url_list", "links"],
            "required": ["urls"]
        },

        # Fetch MCP
        "fetch:fetch": {
            "correct": ["url", "max_length", "start_index", "raw"],
            "wrong": ["link", "uri", "max_size"],
            "required": ["url"]
        },

        # Playwright MCP
        "playwright:browser_navigate": {
            "correct": ["url"],
            "wrong": ["link", "uri"],
            "required": ["url"]
        },
        "playwright:snapshot": {
            "correct": ["name"],
            "wrong": ["filename", "path"],
            "required": ["name"]
        },
        "playwright:screenshot": {
            "correct": ["name"],
            "wrong": ["filename", "path"],
            "required": ["name"]
        },

        # Context7 MCP
        "context7:resolve-library-id": {
            "correct": ["library_name"],
            "wrong": ["name", "lib", "package"],
            "required": ["library_name"]
        },
        "context7:query-docs": {
            "correct": ["library_id", "query"],
            "wrong": ["id", "lib_id", "q"],
            "required": ["library_id", "query"]
        },
    }

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.skills_dir = project_root / "skills"
        self.ai_workflow_root = project_root.parent / "ai_workflow"

    def extract_code_blocks(self, content: str) -> List[Tuple[str, int]]:
        """
        Extract TypeScript code blocks from SKILL.md

        Returns: List of (code_block, line_number) tuples
        """
        code_blocks = []
        lines = content.split('\n')
        in_code_block = False
        current_block = []
        block_start_line = 0

        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```typescript') or line.strip().startswith('```ts'):
                in_code_block = True
                block_start_line = i + 1
                current_block = []
            elif line.strip() == '```' and in_code_block:
                if current_block:
                    code_blocks.append(('\n'.join(current_block), block_start_line))
                in_code_block = False
                current_block = []
            elif in_code_block:
                current_block.append(line)

        return code_blocks

    def parse_airis_exec_call(self, code: str) -> Optional[Tuple[str, Dict[str, any]]]:
        """
        Parse airis-exec() call to extract tool name and arguments

        Returns: (tool_name, arguments_dict) or None
        """
        # Pattern: await airis-exec({ tool: "server:tool", arguments: {...} })
        pattern = r'airis-exec\s*\(\s*\{\s*tool:\s*["\']([^"\']+)["\']\s*,\s*arguments:\s*(\{[^}]*\})'
        match = re.search(pattern, code, re.DOTALL)

        if not match:
            return None

        tool_name = match.group(1)
        args_str = match.group(2)

        # Extract parameter names from arguments object
        param_pattern = r'(\w+):\s*'
        params = re.findall(param_pattern, args_str)

        return tool_name, {param: None for param in params}

    def validate_parameters(self, tool_name: str, params: List[str]) -> List[Tuple[str, str]]:
        """
        Validate parameters against known traps

        Returns: List of (wrong_param, correct_param) tuples
        """
        if tool_name not in self.KNOWN_TRAPS:
            return []  # Unknown tool, skip validation

        trap = self.KNOWN_TRAPS[tool_name]
        errors = []

        for param in params:
            # Check if parameter is in wrong list
            if param in trap["wrong"]:
                # Find corresponding correct parameter
                # For now, return all correct parameters as suggestions
                correct = ', '.join(trap["correct"])
                errors.append((param, correct))

        return errors

    def check_missing_required(self, tool_name: str, params: List[str]) -> List[str]:
        """Check for missing required parameters"""
        if tool_name not in self.KNOWN_TRAPS:
            return []

        trap = self.KNOWN_TRAPS[tool_name]
        required = set(trap["required"])
        provided = set(params)

        return list(required - provided)

    def validate_skill(self, skill_path: Path) -> ValidationReport:
        """Validate a single SKILL.md file"""
        report = ValidationReport(file_path=str(skill_path.relative_to(self.project_root)))

        try:
            content = skill_path.read_text(encoding='utf-8')
        except Exception as e:
            report.warnings.append(f"Failed to read file: {e}")
            return report

        code_blocks = self.extract_code_blocks(content)

        for code, line_num in code_blocks:
            parsed = self.parse_airis_exec_call(code)
            if not parsed:
                continue  # No airis-exec call in this block

            tool_name, args_dict = parsed
            params = list(args_dict.keys())
            report.total_calls += 1

            # Validate parameters
            param_errors = self.validate_parameters(tool_name, params)
            for wrong_param, correct_param in param_errors:
                error = ParameterError(
                    file_path=report.file_path,
                    line_number=line_num,
                    tool_name=tool_name,
                    wrong_param=wrong_param,
                    correct_param=correct_param,
                    code_snippet=code[:200],  # First 200 chars
                    error_type="wrong_name"
                )
                report.errors.append(error)

            # Check missing required
            missing = self.check_missing_required(tool_name, params)
            for param in missing:
                error = ParameterError(
                    file_path=report.file_path,
                    line_number=line_num,
                    tool_name=tool_name,
                    wrong_param="",
                    correct_param=param,
                    code_snippet=code[:200],
                    error_type="missing_required"
                )
                report.errors.append(error)

        return report

    def validate_all_skills(self) -> Dict[str, ValidationReport]:
        """Validate all skills in the project"""
        reports = {}

        if not self.skills_dir.exists():
            print(f"Error: Skills directory not found: {self.skills_dir}")
            return reports

        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue

            report = self.validate_skill(skill_md)
            reports[skill_dir.name] = report

        return reports

    def generate_report(self, reports: Dict[str, ValidationReport], format: str = "text") -> str:
        """Generate validation report"""
        if format == "json":
            return self._generate_json_report(reports)
        elif format == "markdown":
            return self._generate_markdown_report(reports)
        else:
            return self._generate_text_report(reports)

    def _generate_text_report(self, reports: Dict[str, ValidationReport]) -> str:
        """Generate text format report"""
        lines = []
        lines.append("=" * 80)
        lines.append("MCP Parameter Validation Report")
        lines.append("=" * 80)
        lines.append("")

        total_calls = sum(r.total_calls for r in reports.values())
        total_errors = sum(len(r.errors) for r in reports.values())
        overall_accuracy = ((total_calls - total_errors) / total_calls * 100) if total_calls > 0 else 100.0

        lines.append(f"Overall Statistics:")
        lines.append(f"  Total airis-exec calls: {total_calls}")
        lines.append(f"  Total errors found: {total_errors}")
        lines.append(f"  Accuracy: {overall_accuracy:.1f}%")
        lines.append("")

        for skill_name, report in sorted(reports.items()):
            lines.append("-" * 80)
            lines.append(f"Skill: {skill_name}")
            lines.append(f"  File: {report.file_path}")
            lines.append(f"  Calls: {report.total_calls}")
            lines.append(f"  Errors: {len(report.errors)}")
            lines.append(f"  Accuracy: {report.accuracy:.1f}%")

            if report.errors:
                lines.append("")
                lines.append("  Errors:")
                for error in report.errors:
                    if error.error_type == "wrong_name":
                        lines.append(f"    Line {error.line_number}: {error.tool_name}")
                        lines.append(f"      ❌ Wrong parameter: {error.wrong_param}")
                        lines.append(f"      ✅ Correct parameter: {error.correct_param}")
                    elif error.error_type == "missing_required":
                        lines.append(f"    Line {error.line_number}: {error.tool_name}")
                        lines.append(f"      ⚠️  Missing required: {error.correct_param}")

            lines.append("")

        lines.append("=" * 80)
        return '\n'.join(lines)

    def _generate_markdown_report(self, reports: Dict[str, ValidationReport]) -> str:
        """Generate markdown format report"""
        lines = []
        lines.append("# MCP Parameter Validation Report")
        lines.append("")

        total_calls = sum(r.total_calls for r in reports.values())
        total_errors = sum(len(r.errors) for r in reports.values())
        overall_accuracy = ((total_calls - total_errors) / total_calls * 100) if total_calls > 0 else 100.0

        lines.append("## Overall Statistics")
        lines.append("")
        lines.append(f"- **Total airis-exec calls**: {total_calls}")
        lines.append(f"- **Total errors found**: {total_errors}")
        lines.append(f"- **Accuracy**: {overall_accuracy:.1f}%")
        lines.append("")

        lines.append("## Per-Skill Results")
        lines.append("")
        lines.append("| Skill | Calls | Errors | Accuracy | Status |")
        lines.append("|-------|-------|--------|----------|--------|")

        for skill_name, report in sorted(reports.items()):
            status = "✅" if report.is_valid else "❌"
            lines.append(f"| {skill_name} | {report.total_calls} | {len(report.errors)} | {report.accuracy:.1f}% | {status} |")

        lines.append("")

        # Detailed errors
        for skill_name, report in sorted(reports.items()):
            if report.errors:
                lines.append(f"### {skill_name}")
                lines.append("")
                lines.append(f"**File**: `{report.file_path}`")
                lines.append("")

                for error in report.errors:
                    if error.error_type == "wrong_name":
                        lines.append(f"**Line {error.line_number}**: `{error.tool_name}`")
                        lines.append(f"- ❌ Wrong parameter: `{error.wrong_param}`")
                        lines.append(f"- ✅ Correct parameter: `{error.correct_param}`")
                        lines.append("")
                    elif error.error_type == "missing_required":
                        lines.append(f"**Line {error.line_number}**: `{error.tool_name}`")
                        lines.append(f"- ⚠️ Missing required: `{error.correct_param}`")
                        lines.append("")

        return '\n'.join(lines)

    def _generate_json_report(self, reports: Dict[str, ValidationReport]) -> str:
        """Generate JSON format report"""
        output = {
            "overall": {
                "total_calls": sum(r.total_calls for r in reports.values()),
                "total_errors": sum(len(r.errors) for r in reports.values()),
                "accuracy": 0.0
            },
            "skills": {}
        }

        if output["overall"]["total_calls"] > 0:
            output["overall"]["accuracy"] = (
                (output["overall"]["total_calls"] - output["overall"]["total_errors"])
                / output["overall"]["total_calls"] * 100
            )
        else:
            output["overall"]["accuracy"] = 100.0

        for skill_name, report in reports.items():
            output["skills"][skill_name] = {
                "file_path": report.file_path,
                "total_calls": report.total_calls,
                "errors": [
                    {
                        "line": e.line_number,
                        "tool": e.tool_name,
                        "wrong_param": e.wrong_param,
                        "correct_param": e.correct_param,
                        "error_type": e.error_type
                    }
                    for e in report.errors
                ],
                "accuracy": report.accuracy
            }

        return json.dumps(output, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Validate MCP parameters in SKILL.md files")
    parser.add_argument("path", nargs="?", help="Path to SKILL.md file or skills directory")
    parser.add_argument("--all", action="store_true", help="Validate all skills")
    parser.add_argument("--format", choices=["text", "markdown", "json"], default="text",
                        help="Output format (default: text)")

    args = parser.parse_args()

    # Determine project root
    project_root = Path(__file__).parent.parent

    validator = MCPParameterValidator(project_root)

    if args.all:
        reports = validator.validate_all_skills()
    elif args.path:
        skill_path = Path(args.path)
        if not skill_path.exists():
            print(f"Error: File not found: {skill_path}")
            return 2

        report = validator.validate_skill(skill_path)
        reports = {skill_path.stem: report}
    else:
        parser.print_help()
        return 2

    # Generate and print report
    output = validator.generate_report(reports, format=args.format)
    print(output)

    # Return exit code
    total_errors = sum(len(r.errors) for r in reports.values())
    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    exit(main())
