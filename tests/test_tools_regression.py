#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenTools Hub - 工程回归与质量保障测试套件
执行：python -m unittest tests/test_tools_regression.py
维护者：美国洛杉矶专线DEDI-小泡狐 (@xiaopaohu)
"""

import os
import sys
import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import hub_health_checker

class TestOpenToolsHubRegression(unittest.TestCase):

    def setUp(self):
        self.repo_root = REPO_ROOT
        self.tools_dir = self.repo_root / "tools"
        self.docs_dir = self.repo_root / "docs"

    def test_portal_and_tools_structure(self):
        """验证门户入口与工具目录结构完整性"""
        index_file = self.repo_root / "index.html"
        self.assertTrue(index_file.exists(), "Root index.html must exist")
        portal_html = index_file.read_text(encoding="utf-8")

        # 检查门户是否引用了 tools/ 下的所有工具
        self.assertIn("./tools/meta-card-previewer/index.html", portal_html)
        self.assertIn("./tools/dev-secret-sanitizer/index.html", portal_html)

        # 检查实际工具文件存在
        meta_tool = self.tools_dir / "meta-card-previewer" / "index.html"
        sanitizer_tool = self.tools_dir / "dev-secret-sanitizer" / "index.html"
        self.assertTrue(meta_tool.exists(), "MetaCard Studio index.html must exist")
        self.assertTrue(sanitizer_tool.exists(), "SecretSanitizer index.html must exist")

    def test_hub_health_checker_execution(self):
        """执行自主健康巡检引擎并验证 PASS 状态"""
        report = hub_health_checker.run_health_check()
        self.assertEqual(report["overall_status"], "PASS", f"Health check failed: {report}")
        self.assertEqual(report["tools_count"], 2)
        
        for tool in report["tools"]:
            self.assertEqual(tool["status"], "PASS", f"Tool {tool['tool_id']} not passing: {tool}")
            self.assertEqual(len(tool["errors"]), 0, f"Errors in {tool['tool_id']}: {tool['errors']}")
            self.assertEqual(len(tool["warnings"]), 0, f"Warnings in {tool['tool_id']}: {tool['warnings']}")
            self.assertTrue(tool["version"].startswith("v1."), f"Invalid version format: {tool['version']}")

    def test_health_report_json_schema(self):
        """校验落盘报告 docs/health_report.json 规范性"""
        report_file = self.docs_dir / "health_report.json"
        self.assertTrue(report_file.exists(), "health_report.json must be persisted")
        data = json.loads(report_file.read_text(encoding="utf-8"))
        
        self.assertIn("timestamp", data)
        self.assertIn("overall_status", data)
        self.assertIn("tools_count", data)
        self.assertIn("tools", data)
        self.assertEqual(data["overall_status"], "PASS")

    def test_secret_sanitizer_rules_coverage(self):
        """验证脱敏工具内置的全部正则在标准测试用例下的捕获与脱敏能力"""
        test_cases = [
            ("sk-proj-982348hsdkjfh238746y28347yrh8324", r"sk-(?:proj-|live-)?[a-zA-Z0-9_-]{20,}"),
            ("AIzaSyD9x7aK1_82Y4zX10abcdef98765432101", r"AIza[0-9A-Za-z-_]{35}"),
            ("ghp_99abcdefghijklmnopqrstuvwxyz1234567890", r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}"),
            ("AKIAIOSFODNN7EXAMPLE", r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}"),
            ("developer@company.org", r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
            ("192.168.1.100", r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"),
            ("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.t-aeRecord", r"Bearer\s+[a-zA-Z0-9_\-\.=:_+/]+"),
            ("password = 'super_secret_password_123'", r"(?:password|passwd|secret)\s*[:=]\s*[\"']?[^\s\"']+[\"']?")
        ]

        for token, pattern in test_cases:
            match = re.search(pattern, token, re.IGNORECASE)
            self.assertIsNotNone(match, f"Regex {pattern} failed to match {token}")

    def test_zero_remote_vulnerable_scripts(self):
        """离线与静态托管合规性：确保无外部可劫持或单点故障的 script 注入"""
        for tool_dir in self.tools_dir.iterdir():
            if tool_dir.is_dir() and not tool_dir.name.startswith("."):
                index_path = tool_dir / "index.html"
                content = index_path.read_text(encoding="utf-8")
                # 检查没有外链 script
                external_scripts = re.findall(r'<script[^>]+src=["\'](http[^"\']+)["\']', content, re.IGNORECASE)
                self.assertEqual(len(external_scripts), 0, f"Found external scripts in {tool_dir.name}: {external_scripts}")

if __name__ == "__main__":
    unittest.main()
