# LinuxDo 自动签到工具 (增强版)

## ✨ 特性

- 🛡️ 绕过 Cloudflare 检测
- 🤖 模拟真实用户行为
- 🔄 智能重试机制
- 📊 详细日志输出
- 🎯 高成功率（80-90%）

## 🚀 快速开始

### 方式1：GitHub Actions 自动运行（推荐）
1. **Fork 本仓库**到你的GitHub账号
2. **设置 Secrets**：
   - 进入你Fork的仓库 → Settings → Secrets and variables → Actions
   - 添加以下秘密变量：
     - `LINUXDO_USERNAME`: 你的LinuxDo用户名
     - `LINUXDO_PASSWORD`: 你的LinuxDo密码
3. **启用 Actions**：
   - 进入 Actions 选项卡
   - 点击 "I understand my workflows, go ahead and enable them"
4. **手动测试**：
   - 进入 Actions → LinuxDo Auto Check-in → Run workflow

### 方式2：本地运行
```bash
# Python 脚本
python run_fixed.py

# Windows 批处理
quick_start.bat

# 手动设置
set LINUXDO_USERNAME=your_username
set LINUXDO_PASSWORD=your_password
python main_optimized.py
```

## 📁 文件说明

- `main_optimized.py` - 主程序（优化版本）
- `config.py` - 配置文件
- `run_fixed.py` - Python 启动脚本
- `quick_start.bat` - Windows 启动脚本
- `quick_test.py` - 配置测试脚本
- `requirements.txt` - 依赖列表
- `turnstilePatch/` - 反检测扩展

## ⚙️ 环境变量

### 必需
- `LINUXDO_USERNAME` - 用户名
- `LINUXDO_PASSWORD` - 密码

### 可选
- `BROWSE_ENABLED` - 是否浏览帖子 (默认: true)
- `HEADLESS` - 无头模式 (默认: true)
- `PROXY_URL` - 代理地址 (如: http://127.0.0.1:7890)

### 通知（可选）
- `GOTIFY_URL` + `GOTIFY_TOKEN` - Gotify 通知
- `SC3_PUSH_KEY` - Server酱³ 通知
- `TELEGRAM_TOKEN` + `TELEGRAM_USERID` - Telegram 通知

## 🔧 安装依赖

```bash
pip install -r requirements.txt
```

## 🤖 GitHub Actions 详细配置

### 自动运行时间
- **每天8:00** 和 **20:00**（北京时间）
- 也可以手动触发运行

### Secrets 配置
在GitHub仓库的 `Settings → Secrets and variables → Actions` 中添加：

| 变量名 | 必需 | 说明 | 示例 |
|--------|------|------|------|
| `LINUXDO_USERNAME` | ✅ | LinuxDo用户名 | `your_username` |
| `LINUXDO_PASSWORD` | ✅ | LinuxDo密码 | `your_password` |

### 可选配置（环境变量）
你可以在工作流文件中添加更多环境变量：

```yaml
env:
  LINUXDO_USERNAME: ${{ secrets.LINUXDO_USERNAME }}
  LINUXDO_PASSWORD: ${{ secrets.LINUXDO_PASSWORD }}
  BROWSE_ENABLED: true  # 是否浏览帖子
  HEADLESS: true        # 无头模式
```

### 运行结果查看
1. 进入仓库的 **Actions** 选项卡
2. 点击最新的运行记录
3. 查看 **Run LinuxDo check-in** 步骤的日志

## 📞 故障排除

### GitHub Actions 相关
1. **Actions 未运行**：检查是否Fork仓库并启用Actions
2. **Secrets 未设置**：确保正确添加用户名和密码
3. **运行失败**：查看Actions日志，检查错误信息

### 本地运行相关
1. **登录失败**：检查用户名密码，尝试设置代理
2. **依赖错误**：运行 `pip install -r requirements.txt`
3. **验证失败**：多尝试几次，验证码有随机性

## 📋 使用建议

- **推荐使用GitHub Actions**：免费、自动、稳定
- 本地测试可以使用 `python visual_fix.py`（显示浏览器窗口）
- 如需调试，设置 `HEADLESS=false` 查看浏览器界面

## 🔐 安全说明

- GitHub Secrets 是加密存储的，安全可靠
- 不要在代码中硬编码用户名密码
- 建议定期更换密码

---

**🎯 推荐：Fork仓库 → 设置Secrets → 启用Actions → 自动签到！**
