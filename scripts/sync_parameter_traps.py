#!/usr/bin/env python3
"""
Parameter Traps Synchronization Script

Synchronizes MCP parameter documentation between:
- ai_workflow/PARAMETER_TRAPS.md (source of truth)
- howie_skills documentation

Features:
- Parse ai_workflow PARAMETER_TRAPS.md
- Extract parameter patterns for all MCP servers
- Compare with howie_skills documentation
- Generate sync report

Usage:
  python sync_parameter_traps.py > docs/PARAMETER_SYNC_REPORT.md
  python sync_parameter_traps.py --update
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, field


@dataclass
class MCPToolInfo:
    """Information about an MCP tool"""
    server: str
    tool: str
    correct_params: List[str] = field(default_factory=list)
    wrong_params: List[str] = field(default_factory=list)
    required_params: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)


class ParameterTrapSync:
    """
    Synchronize parameter documentation with ai_workflow

    Workflow:
    1. Load ai_workflow/PARAMETER_TRAPS.md
    2. Parse server -> tool -> params structure
    3. Compare with howie_skills validate_mcp_params.py
    4. Generate sync report
    """

    def __init__(self, howie_root: Path, ai_workflow_root: Path):
        self.howie_root = howie_root
        self.ai_workflow_root = ai_workflow_root
        self.parameter_traps_path = (
            ai_workflow_root / "docs" / "airis-mcp-gateway" / "PARAMETER_TRAPS.md"
        )

    def load_ai_workflow_traps(self) -> Dict[str, List[MCPToolInfo]]:
        """
        Load and parse ai_workflow/PARAMETER_TRAPS.md

        Returns: Dict[server_name, List[MCPToolInfo]]
        """
        if not self.parameter_traps_path.exists():
            print(f"Warning: PARAMETER_TRAPS.md not found at {self.parameter_traps_path}")
            return {}

        content = self.parameter_traps_path.read_text(encoding='utf-8')

        # Parse structure:
        # ### ServerName MCP 服务器
        # #### 1. tool_name
        # **常见错误**: - `param1` ❌
        # **正确参数**: - `param2` ✅ (必需)

        servers = {}
        current_server = None
        current_tool = None

        lines = content.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Server header: ### Serena MCP 服务器
            if line.startswith('### ') and 'MCP' in line:
                server_match = re.search(r'###\s+(\w+)\s+MCP', line)
                if server_match:
                    current_server = server_match.group(1).lower()
                    if current_server not in servers:
                        servers[current_server] = []

            # Tool header: #### 1. tool_name
            elif line.startswith('#### ') and current_server:
                tool_match = re.search(r'####\s+\d+\.\s+(\S+)', line)
                if tool_match:
                    tool_name = tool_match.group(1)
                    current_tool = MCPToolInfo(server=current_server, tool=tool_name)
                    servers[current_server].append(current_tool)

            # Wrong params: - `param` ❌
            elif line.startswith('**常见错误**') and current_tool:
                # Parse following lines for wrong params
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith('- `'):
                    param_match = re.search(r'- `(\w+)` ❌', lines[j])
                    if param_match:
                        current_tool.wrong_params.append(param_match.group(1))
                    j += 1

            # Correct params: - `param` ✅ (必需)
            elif line.startswith('**正确参数**') and current_tool:
                # Parse following lines for correct params
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith('- `'):
                    param_match = re.search(r'- `(\w+)` ✅', lines[j])
                    if param_match:
                        param = param_match.group(1)
                        current_tool.correct_params.append(param)
                        # Check if required
                        if '必需' in lines[j] or 'required' in lines[j].lower():
                            current_tool.required_params.append(param)
                    j += 1

            i += 1

        return servers

    def load_howie_traps(self) -> Dict[str, Dict]:
        """
        Load traps from howie_skills/scripts/validate_mcp_params.py

        Returns: KNOWN_TRAPS dict structure
        """
        validate_script = self.howie_root / "scripts" / "validate_mcp_params.py"
        if not validate_script.exists():
            return {}

        content = validate_script.read_text(encoding='utf-8')

        # Extract KNOWN_TRAPS dictionary
        # This is a simplified extraction - in real scenario would use ast module
        traps = {}

        # Find KNOWN_TRAPS = { ... }
        match = re.search(r'KNOWN_TRAPS\s*=\s*\{(.*?)\n    \}', content, re.DOTALL)
        if match:
            traps_content = match.group(1)

            # Parse each tool entry
            tool_pattern = r'"(\w+):(\w+)":\s*\{([^}]+)\}'
            for tool_match in re.finditer(tool_pattern, traps_content):
                server = tool_match.group(1)
                tool = tool_match.group(2)
                params_block = tool_match.group(3)

                tool_key = f"{server}:{tool}"
                traps[tool_key] = {}

                # Extract correct params
                correct_match = re.search(r'"correct":\s*\[(.*?)\]', params_block)
                if correct_match:
                    correct_str = correct_match.group(1)
                    traps[tool_key]['correct'] = [
                        p.strip(' "') for p in correct_str.split(',') if p.strip()
                    ]

                # Extract wrong params
                wrong_match = re.search(r'"wrong":\s*\[(.*?)\]', params_block)
                if wrong_match:
                    wrong_str = wrong_match.group(1)
                    traps[tool_key]['wrong'] = [
                        p.strip(' "') for p in wrong_str.split(',') if p.strip()
                    ]

                # Extract required params
                required_match = re.search(r'"required":\s*\[(.*?)\]', params_block)
                if required_match:
                    required_str = required_match.group(1)
                    traps[tool_key]['required'] = [
                        p.strip(' "') for p in required_str.split(',') if p.strip()
                    ]

        return traps

    def compare_coverage(self) -> Dict:
        """
        Compare coverage between ai_workflow and howie_skills

        Returns: Comparison report
        """
        ai_traps = self.load_ai_workflow_traps()
        howie_traps = self.load_howie_traps()

        report = {
            'ai_workflow_servers': len(ai_traps),
            'ai_workflow_tools': sum(len(tools) for tools in ai_traps.values()),
            'howie_tools': len(howie_traps),
            'missing_in_howie': [],
            'extra_in_howie': [],
            'param_mismatches': []
        }

        # Find tools in ai_workflow but not in howie
        for server, tools in ai_traps.items():
            for tool_info in tools:
                tool_key = f"{server}:{tool_info.tool}"
                if tool_key not in howie_traps:
                    report['missing_in_howie'].append(tool_key)

        # Find tools in howie but not in ai_workflow
        all_ai_tools = set()
        for server, tools in ai_traps.items():
            for tool_info in tools:
                all_ai_tools.add(f"{server}:{tool_info.tool}")

        for tool_key in howie_traps.keys():
            if tool_key not in all_ai_tools:
                report['extra_in_howie'].append(tool_key)

        # Compare parameters for matching tools
        for server, tools in ai_traps.items():
            for tool_info in tools:
                tool_key = f"{server}:{tool_info.tool}"
                if tool_key in howie_traps:
                    howie_tool = howie_traps[tool_key]

                    # Compare correct params
                    ai_correct = set(tool_info.correct_params)
                    howie_correct = set(howie_tool.get('correct', []))

                    if ai_correct != howie_correct:
                        report['param_mismatches'].append({
                            'tool': tool_key,
                            'ai_correct': list(ai_correct),
                            'howie_correct': list(howie_correct),
                            'missing': list(ai_correct - howie_correct),
                            'extra': list(howie_correct - ai_correct)
                        })

        return report

    def generate_sync_report(self) -> str:
        """Generate markdown sync report"""
        ai_traps = self.load_ai_workflow_traps()
        comparison = self.compare_coverage()

        lines = []
        lines.append("# MCP Parameter Synchronization Report")
        lines.append("")
        lines.append(f"**Generated**: 2025-12-31")
        lines.append(f"**Source**: ai_workflow/docs/airis-mcp-gateway/PARAMETER_TRAPS.md")
        lines.append("")

        lines.append("## Coverage Summary")
        lines.append("")
        lines.append(f"- **ai_workflow servers**: {comparison['ai_workflow_servers']}")
        lines.append(f"- **ai_workflow tools**: {comparison['ai_workflow_tools']}")
        lines.append(f"- **howie_skills tools**: {comparison['howie_tools']}")
        lines.append("")

        # Missing tools
        if comparison['missing_in_howie']:
            lines.append("## Tools in ai_workflow but NOT in howie_skills")
            lines.append("")
            lines.append("These tools should be added to `validate_mcp_params.py`:")
            lines.append("")
            for tool in sorted(comparison['missing_in_howie']):
                lines.append(f"- `{tool}`")
            lines.append("")

        # Extra tools
        if comparison['extra_in_howie']:
            lines.append("## Tools in howie_skills but NOT in ai_workflow")
            lines.append("")
            lines.append("These tools may be outdated or custom:")
            lines.append("")
            for tool in sorted(comparison['extra_in_howie']):
                lines.append(f"- `{tool}`")
            lines.append("")

        # Parameter mismatches
        if comparison['param_mismatches']:
            lines.append("## Parameter Mismatches")
            lines.append("")
            lines.append("Tools with different parameter definitions:")
            lines.append("")

            for mismatch in comparison['param_mismatches']:
                lines.append(f"### `{mismatch['tool']}`")
                lines.append("")

                if mismatch['missing']:
                    lines.append("**Missing in howie_skills**:")
                    for param in mismatch['missing']:
                        lines.append(f"- `{param}`")
                    lines.append("")

                if mismatch['extra']:
                    lines.append("**Extra in howie_skills**:")
                    for param in mismatch['extra']:
                        lines.append(f"- `{param}`")
                    lines.append("")

        # Detailed ai_workflow reference
        lines.append("## ai_workflow Parameter Reference")
        lines.append("")
        lines.append("Complete parameter reference from ai_workflow:")
        lines.append("")

        for server in sorted(ai_traps.keys()):
            tools = ai_traps[server]
            lines.append(f"### {server.capitalize()} MCP")
            lines.append("")

            for tool_info in tools:
                lines.append(f"#### `{server}:{tool_info.tool}`")
                lines.append("")

                if tool_info.correct_params:
                    lines.append("**Correct parameters**:")
                    for param in tool_info.correct_params:
                        required = " (required)" if param in tool_info.required_params else ""
                        lines.append(f"- `{param}`{required}")
                    lines.append("")

                if tool_info.wrong_params:
                    lines.append("**Common errors**:")
                    for param in tool_info.wrong_params:
                        lines.append(f"- `{param}` ❌")
                    lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("**Next Steps**:")
        lines.append("")
        lines.append("1. Add missing tools to `validate_mcp_params.py`")
        lines.append("2. Fix parameter mismatches")
        lines.append("3. Re-run validation: `python validate_mcp_params.py --all`")

        return '\n'.join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Sync parameter traps with ai_workflow")
    parser.add_argument("--update", action="store_true", help="Update howie_skills documentation")
    args = parser.parse_args()

    # Determine paths
    howie_root = Path(__file__).parent.parent
    ai_workflow_root = howie_root.parent / "ai_workflow"

    if not ai_workflow_root.exists():
        print(f"Error: ai_workflow not found at {ai_workflow_root}")
        print("Please ensure ai_workflow and howie_skills are sibling directories")
        return 1

    sync = ParameterTrapSync(howie_root, ai_workflow_root)

    # Generate report
    report = sync.generate_sync_report()
    print(report)

    if args.update:
        print("\n" + "=" * 80)
        print("Note: --update not yet implemented")
        print("Please manually update validate_mcp_params.py based on the report above")
        print("=" * 80)

    return 0


if __name__ == "__main__":
    exit(main())
