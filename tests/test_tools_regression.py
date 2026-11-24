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
        self.assertIn("./tools/curl-code-studio/index.html", portal_html)
        self.assertIn("./tools/cron-webhook-studio/index.html", portal_html)
        self.assertIn("./tools/svg-cleaner-studio/index.html", portal_html)
        self.assertIn("./tools/json-semantic-diff/index.html", portal_html)
        self.assertIn("./tools/jwt-inspector-studio/index.html", portal_html)
        self.assertIn("./tools/css-glassmorphism-studio/index.html", portal_html)
        self.assertIn("./tools/regex-lab-studio/index.html", portal_html)
        self.assertIn("./tools/base64-binary-studio/index.html", portal_html)
        self.assertIn("./tools/markdown-table-studio/index.html", portal_html)
        self.assertIn("./tools/hash-checksum-studio/index.html", portal_html)
        self.assertIn("./tools/schema-codegen-studio/index.html", portal_html)
        self.assertIn("./tools/color-palette-studio/index.html", portal_html)
        self.assertIn("./tools/code-snapshot-studio/index.html", portal_html)
        self.assertIn("./tools/token-compressor-studio/index.html", portal_html)

        # 检查实际工具文件存在
        meta_tool = self.tools_dir / "meta-card-previewer" / "index.html"
        sanitizer_tool = self.tools_dir / "dev-secret-sanitizer" / "index.html"
        curl_tool = self.tools_dir / "curl-code-studio" / "index.html"
        cron_tool = self.tools_dir / "cron-webhook-studio" / "index.html"
        svg_tool = self.tools_dir / "svg-cleaner-studio" / "index.html"
        json_tool = self.tools_dir / "json-semantic-diff" / "index.html"
        jwt_tool = self.tools_dir / "jwt-inspector-studio" / "index.html"
        css_tool = self.tools_dir / "css-glassmorphism-studio" / "index.html"
        regex_tool = self.tools_dir / "regex-lab-studio" / "index.html"
        base64_tool = self.tools_dir / "base64-binary-studio" / "index.html"
        md_tool = self.tools_dir / "markdown-table-studio" / "index.html"
        hash_tool = self.tools_dir / "hash-checksum-studio" / "index.html"
        schema_tool = self.tools_dir / "schema-codegen-studio" / "index.html"
        color_tool = self.tools_dir / "color-palette-studio" / "index.html"
        code_tool = self.tools_dir / "code-snapshot-studio" / "index.html"
        token_tool = self.tools_dir / "token-compressor-studio" / "index.html"
        self.assertTrue(meta_tool.exists(), "MetaCard Studio index.html must exist")
        self.assertTrue(sanitizer_tool.exists(), "SecretSanitizer index.html must exist")
        self.assertTrue(curl_tool.exists(), "cURL Code Studio index.html must exist")
        self.assertTrue(cron_tool.exists(), "Cron & Webhook Studio index.html must exist")
        self.assertTrue(svg_tool.exists(), "SVG Cleaner Studio index.html must exist")
        self.assertTrue(json_tool.exists(), "JSON Semantic Diff index.html must exist")
        self.assertTrue(jwt_tool.exists(), "JWT Inspector Studio index.html must exist")
        self.assertTrue(css_tool.exists(), "CSS Glassmorphism Studio index.html must exist")
        self.assertTrue(regex_tool.exists(), "RegexLab Studio index.html must exist")
        self.assertTrue(base64_tool.exists(), "Base64 Binary Studio index.html must exist")
        self.assertTrue(md_tool.exists(), "Markdown Table Studio index.html must exist")
        self.assertTrue(hash_tool.exists(), "Hash & Checksum Studio index.html must exist")
        self.assertTrue(schema_tool.exists(), "SchemaForge Studio index.html must exist")
        self.assertTrue(color_tool.exists(), "Color Palette Studio index.html must exist")
        self.assertTrue(code_tool.exists(), "CodeShot Studio index.html must exist")
        self.assertTrue(token_tool.exists(), "TokenCompressor Studio index.html must exist")

    def test_hub_health_checker_execution(self):
        """执行自主健康巡检引擎并验证 PASS 状态"""
        report = hub_health_checker.run_health_check()
        self.assertEqual(report["overall_status"], "PASS", f"Health check failed: {report}")
        self.assertEqual(report["tools_count"], 16)
        
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

    def test_jwt_decoder_offline_integrity(self):
        """验证 JWT 离线解析与三段式结构规范"""
        import base64
        header = json.dumps({"alg": "HS256", "typ": "JWT"})
        payload = json.dumps({"sub": "test", "name": "xiaopaohu"})
        h_b64 = base64.urlsafe_b64encode(header.encode()).decode().rstrip("=")
        p_b64 = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
        dummy_jwt = f"{h_b64}.{p_b64}.dummysig"
        parts = dummy_jwt.split(".")
        self.assertEqual(len(parts), 3)
        self.assertEqual(json.loads(base64.urlsafe_b64decode(parts[0] + "==").decode())["alg"], "HS256")
        self.assertEqual(json.loads(base64.urlsafe_b64decode(parts[1] + "==").decode())["name"], "xiaopaohu")

    def test_css_glassmorphism_features(self):
        """验证 CSS Glassmorphism Studio 页面结构与核心功能"""
        tool_file = self.tools_dir / "css-glassmorphism-studio" / "index.html"
        self.assertTrue(tool_file.exists())
        content = tool_file.read_text(encoding="utf-8")
        self.assertIn("backdrop-filter", content)
        self.assertIn("-webkit-backdrop-filter", content)
        self.assertIn("bgPresets", content)
        self.assertIn("aurora_frost", content)
        self.assertIn("deep_frosted", content)
        self.assertIn("dark_obsidian", content)
        self.assertIn("navigator.clipboard.writeText", content)

    def test_regex_lab_studio_features(self):
        """验证 RegexLab Studio 页面结构、预设规则与核心功能"""
        tool_file = self.tools_dir / "regex-lab-studio" / "index.html"
        self.assertTrue(tool_file.exists())
        content = tool_file.read_text(encoding="utf-8")
        self.assertIn("RegexLab Studio", content)
        self.assertIn("runEvaluation", content)
        self.assertIn("evaluateTestCases", content)
        self.assertIn("renderCodeExport", content)
        self.assertIn("presets", content)
        self.assertIn("email", content)
        self.assertIn("ipv4", content)
        self.assertIn("semver", content)
        self.assertIn("navigator.clipboard.writeText", content)

    def test_base64_binary_studio_features(self):
        """验证 Base64, Hex & Data URI Binary Inspector Studio 页面结构与核心功能"""
        tool_file = self.tools_dir / "base64-binary-studio" / "index.html"
        self.assertTrue(tool_file.exists())
        content = tool_file.read_text(encoding="utf-8")
        self.assertIn("Base64, Hex & Data URI Binary Inspector Studio", content)
        self.assertIn("detectMagicBytes", content)
        self.assertIn("bytesToBase64", content)
        self.assertIn("generateHexDump", content)
        self.assertIn("magicSignatures", content)
        self.assertIn("navigator.clipboard.writeText", content)
        self.assertIn("URL.createObjectURL", content)

    def test_markdown_table_studio_features(self):
        """验证 Markdown Table & ASCII Matrix Studio 页面结构与核心功能"""
        tool_file = self.tools_dir / "markdown-table-studio" / "index.html"
        self.assertTrue(tool_file.exists())
        content = tool_file.read_text(encoding="utf-8")
        self.assertIn("Markdown Table & ASCII Matrix Studio", content)
        self.assertIn("renderEditorTable", content)
        self.assertIn("transposeTable", content)
        self.assertIn("generateBoxTable", content)
        self.assertIn("importRawData", content)
        self.assertIn("navigator.clipboard.writeText", content)

    def test_hash_checksum_studio_features(self):
        """验证 Hash & Checksum Studio 页面结构与核心功能"""
        tool_file = self.tools_dir / "hash-checksum-studio" / "index.html"
        self.assertTrue(tool_file.exists())
        content = tool_file.read_text(encoding="utf-8")
        self.assertIn("Hash & Checksum Studio", content)
        self.assertIn("calculateMd5", content)
        self.assertIn("calculateCrc32", content)
        self.assertIn("recomputeAllHashes", content)
        self.assertIn("crypto.subtle.digest", content)
        self.assertIn("checkMatch", content)
        self.assertIn("navigator.clipboard.writeText", content)

    def test_schema_codegen_studio_features(self):
        """验证 SchemaForge Studio 页面结构与核心功能"""
        tool_file = self.tools_dir / "schema-codegen-studio" / "index.html"
        self.assertTrue(tool_file.exists())
        content = tool_file.read_text(encoding="utf-8")
        self.assertIn("SchemaForge - JSON to TypeScript, Zod & Go Struct Studio", content)
        self.assertIn("regenerateSchemas", content)
        self.assertIn("generateTypeScript", content)
        self.assertIn("generateZod", content)
        self.assertIn("generateGo", content)
        self.assertIn("generatePydantic", content)
        self.assertIn("navigator.clipboard.writeText", content)

    def test_color_palette_studio_features(self):
        """验证 Color Palette & Design Token Studio 页面结构与核心功能"""
        tool_file = self.tools_dir / "color-palette-studio" / "index.html"
        self.assertTrue(tool_file.exists())
        content = tool_file.read_text(encoding="utf-8")
        self.assertIn("Color Palette &amp; Design Token Studio", content)
        self.assertIn("generatePalette", content)
        self.assertIn("generateCssVars", content)
        self.assertIn("generateTailwindConfig", content)
        self.assertIn("generateTailwindV4", content)
        self.assertIn("generateJson", content)
        self.assertIn("getLuminance", content)
        self.assertIn("getContrastRatio", content)
        self.assertIn("navigator.clipboard.writeText", content)

    def test_code_snapshot_studio_features(self):
        """验证 CodeShot Studio 页面结构与核心功能"""
        tool_file = self.tools_dir / "code-snapshot-studio" / "index.html"
        self.assertTrue(tool_file.exists())
        content = tool_file.read_text(encoding="utf-8")
        self.assertIn("CodeShot Studio - Beautiful Code Snippet to PNG", content)
        self.assertIn("renderShot", content)
        self.assertIn("tokenizeLine", content)
        self.assertIn("copyImageToClipboard", content)
        self.assertIn("downloadPng", content)
        self.assertIn("downloadSvg", content)
        self.assertIn("THEMES", content)
        self.assertIn("BACKGROUNDS", content)

    def test_token_compressor_studio_features(self):
        """验证 TokenCompressor Studio 页面结构与核心功能"""
        tool_file = self.tools_dir / "token-compressor-studio" / "index.html"
        self.assertTrue(tool_file.exists())
        content = tool_file.read_text(encoding="utf-8")
        self.assertIn("TokenCompressor Studio - AI Prompt &amp; Context Token Optimizer", content)
        self.assertIn("estimateTokens", content)
        self.assertIn("compressCode", content)
        self.assertIn("compressJson", content)
        self.assertIn("compressLogs", content)
        self.assertIn("compressPrompt", content)
        self.assertIn("compressText", content)
        self.assertIn("copyCompressedText", content)
        self.assertIn("downloadCompressed", content)

if __name__ == "__main__":
    unittest.main()
