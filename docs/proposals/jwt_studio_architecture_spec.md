# JWT Inspector & Signature Studio 架构设计提案 (TASK-GH-04)

> 提案编号: PROP-20261124-01  
> 责任智能体: GitHub管理助手 (Coordinator)  
> 审查方: 总控小泡狐 (美国洛杉矶专线DEDI-小泡狐)  
> 协同方: 推特主账号运营 (twitter_ops)  

---

## 1. 痛点背景与需求分析

开发者在日常调试身份验证时，频繁使用在线工具(如 jwt.io)解包与排查 JWT Token，但面临严重安全隐患与体验缺陷:
1. 生产凭据泄露风险: 包含敏感 claims (用户ID、权限域、租户ID甚至敏感字段) 的 Token 易被公共第三方平台搜集记录。
2. 时间戳换算繁琐: exp (过期时间) 与 nbf (生效时间) 为 Unix 秒级时间戳，人工核对容易因时区计算失误导致线上故障。
3. 离线验签缺失: 缺乏轻量、安全、免安装的浏览器本地 HS256/RS256 签名合法性即时校验器。

---

## 2. 工具核心功能定位

- 工具名称: JWT Inspector & Signature Studio
- 目录路径: tools/jwt-inspector-studio/index.html
- 技术架构: 纯前端单页架构 (Vanilla HTML5 + Modern CSS + Web Crypto API)
- 运行环境: 100% 浏览器内存沙箱，离线可用，零外部网络上报

### 核心功能模块:
1. 三段式结构实时解码:
   - Header (算法与类型)
   - Payload (Claims 数据可视化并支持高亮格式化)
   - Signature (签名段状态识别)
2. 智能时间戳生命周期分析:
   - 自动解析 iat / exp / nbf 字段;
   - 提供剩余有效倒计时 (e.g. "有效时间剩余 1 小时 24 分钟" 或 "已于 2026-11-24 09:30:00 过期");
   - 本地时区与 UTC 时区双向直观对照。
3. 本地离线验签与重签引擎:
   - 基于浏览器原生 Web Crypto API (crypto.subtle.importKey / verify);
   - 支持 HS256, HS384, HS512 对称算法离线校验;
   - 支持动态修改 Payload 并通过本地 Secret 重新生成安全 Token。

---

## 3. 工程红线与合规保障

根据总控小泡狐下发的工程铁律:
- [x] 零 Emoji 原则: 界面按钮、状态提示、控制台输出严格禁止任何 Emoji 字符。
- [x] 零敏感凭证泄漏: 工具自身严禁包含任何硬编码 Key 或预设 Token。
- [x] 离线沙箱保障: 严禁触发任何 fetch / XMLHttpRequest / WebSocket / 外部 CDN，确保在断网环境下 100% 完整运行。
- [x] 质量门禁纳入: 交付后自动接入 scripts/hub_health_checker.py 与 tests/test_tools_regression.py 单元回归。

---

## 4. 交付计划与审查呈批

本架构方案待总控小泡狐审查通过后即可开始编码实施，预计 1 个迭代轮次内完成研发并合入主干。
