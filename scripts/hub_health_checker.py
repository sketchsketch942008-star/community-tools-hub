#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenTools Hub - 自主健康巡检与工具质量检查引擎
由“美国洛杉矶专线DEDI-小泡狐”与 GitHub 管理助手（Coordinator）联合调度使用。
自主检查工具功能完整性、DOM/HTML规范、资源链接与版本状态。
"""

import os
import sys
import json
import re
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
DOCS_DIR = REPO_ROOT / "docs"
REPORT_FILE = DOCS_DIR / "health_report.json"

def inspect_html_tool(tool_dir: Path) -> dict:
    index_file = tool_dir / "index.html"
    result = {
        "tool_id": tool_dir.name,
        "entry_point": "index.html",
        "exists": index_file.exists(),
        "status": "PASS",
        "errors": [],
        "warnings": [],
        "version": "unknown",
        "title": "unknown",
        "size_bytes": 0
    }

    if not index_file.exists():
        result["status"] = "FAIL"
        result["errors"].append("Missing index.html entrypoint")
        return result

    try:
        content = index_file.read_text(encoding="utf-8")
        result["size_bytes"] = len(content)

        # 1. 基础规范检查
        if "<!DOCTYPE html>" not in content and "<!doctype html>" not in content:
            result["warnings"].append("Missing <!DOCTYPE html> declaration")
        if "<html" not in content or "</html>" not in content:
            result["errors"].append("Malformed HTML structure")
        if "<script" in content and "</script>" not in content:
            result["errors"].append("Unclosed <script> tag detected")

        # 2. 提取页面 Title 与 Version
        title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
        if title_match:
            result["title"] = title_match.group(1).strip()
        else:
            result["warnings"].append("Missing <title> tag")

        ver_match = re.search(r'v(\d+\.\d+\.\d+)', content)
        if ver_match:
            result["version"] = ver_match.group(0)

        # 3. 检查是否存在未处理的外链破坏 (避免依赖容易被墙或失效的第三方重型库)
        external_scripts = re.findall(r'<script[^>]+src=["\'](http[^"\']+)["\']', content, re.IGNORECASE)
        if external_scripts:
            result["warnings"].append(f"External script dependencies found: {len(external_scripts)}")

        if result["errors"]:
            result["status"] = "FAIL"
        elif result["warnings"]:
            result["status"] = "WARN"
        else:
            result["status"] = "PASS"

    except Exception as e:
        result["status"] = "FAIL"
        result["errors"].append(f"Exception reading tool: {str(e)}")

    return result

def run_health_check() -> dict:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    tools = []
    
    if not TOOLS_DIR.exists():
        print(f"[!] Tools directory not found: {TOOLS_DIR}")
        return {"overall": "FAIL", "tools": []}

    for item in sorted(TOOLS_DIR.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            report = inspect_html_tool(item)
            tools.append(report)

    overall_status = "PASS"
    for t in tools:
        if t["status"] == "FAIL":
            overall_status = "FAIL"
            break
        elif t["status"] == "WARN" and overall_status == "PASS":
            overall_status = "WARN"

    final_report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "overall_status": overall_status,
        "tools_count": len(tools),
        "tools": tools
    }

    REPORT_FILE.write_text(json.dumps(final_report, ensure_ascii=False, indent=2), encoding="utf-8")
    return final_report

def print_summary(report: dict):
    print("=" * 60)
    print(" OpenTools Hub - 自动化巡检与质量评估报告")
    print("=" * 60)
    print(f" 巡检时间: {report['timestamp']}")
    print(f" 总体状态: [{'PASS' if report['overall_status']=='PASS' else report['overall_status']}]")
    print(f" 工具总数: {report['tools_count']}")
    print("-" * 60)
    for tool in report["tools"]:
        icon = "✅" if tool["status"] == "PASS" else ("⚠️" if tool["status"] == "WARN" else "❌")
        print(f" {icon} {tool['tool_id']:<25} | 版本: {tool['version']:<8} | 状态: {tool['status']}")
        if tool["errors"]:
            for err in tool["errors"]:
                print(f"    └── [ERR] {err}")
        if tool["warnings"]:
            for warn in tool["warnings"]:
                print(f"    └── [WARN] {warn}")
    print("=" * 60)
    print(f" 巡检详细数据已落盘至: {REPORT_FILE}")

if __name__ == "__main__":
    rep = run_health_check()
    print_summary(rep)
    if rep["overall_status"] == "FAIL":
        sys.exit(1)
    sys.exit(0)
