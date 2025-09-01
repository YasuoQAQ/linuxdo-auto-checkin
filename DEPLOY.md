# 🚀 GitHub Actions 部署指南

## 1️⃣ Fork 仓库

1. 点击本仓库右上角的 **Fork** 按钮
2. 选择你的GitHub账号作为目标
3. 等待Fork完成

## 2️⃣ 设置 Secrets

1. 进入你Fork的仓库
2. 点击 **Settings** 选项卡
3. 在左侧菜单中找到 **Secrets and variables** → **Actions**
4. 点击 **New repository secret** 按钮

### 添加用户名
- **Name**: `LINUXDO_USERNAME`
- **Value**: 你的LinuxDo用户名（例如：`alenlsp`）

### 添加密码
- **Name**: `LINUXDO_PASSWORD`  
- **Value**: 你的LinuxDo密码

## 3️⃣ 启用 Actions

1. 点击 **Actions** 选项卡
2. 如果看到提示，点击 **"I understand my workflows, go ahead and enable them"**
3. 找到 **LinuxDo Auto Check-in** 工作流

## 4️⃣ 测试运行

### 手动触发
1. 在 Actions 页面点击 **LinuxDo Auto Check-in**
2. 点击 **Run workflow** 按钮
3. 选择分支（通常是 main）
4. 点击绿色的 **Run workflow** 按钮

### 查看结果
1. 等待工作流开始运行（可能需要几秒钟）
2. 点击运行中的工作流查看实时日志
3. 展开 **Run LinuxDo check-in** 步骤查看详细输出

## 5️⃣ 自动运行

配置完成后，工作流将自动在以下时间运行：
- **每天上午 8:00**（北京时间）
- **每天晚上 8:00**（北京时间）

## 🔧 自定义配置

如果需要修改运行时间或添加其他配置，编辑 `.github/workflows/auto-checkin.yml` 文件：

```yaml
on:
  schedule:
    # 修改运行时间（使用UTC时间）
    - cron: '0 0,12 * * *'  # 对应北京时间8:00和20:00
```

## 📊 监控和维护

### 查看运行历史
- Actions 页面显示所有运行历史
- 绿色 ✅ 表示成功，红色 ❌ 表示失败

### 常见问题
1. **Secret 未设置**：检查用户名密码是否正确添加
2. **登录失败**：可能是密码错误或网络问题
3. **Actions 被禁用**：GitHub会自动禁用长期未使用的仓库的Actions

### 保持活跃
- 定期（至少每60天）访问一次仓库
- 或者定期手动触发一次工作流
- 这样可以防止GitHub自动禁用Actions

## ✅ 完成！

现在你的LinuxDo自动签到已经设置完成，将会自动运行！

🎉 **恭喜，享受自动签到的便利吧！**
