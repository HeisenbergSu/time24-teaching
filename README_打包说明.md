# 快速打包指南（Windows 平台）

## 🚀 一键打包（最简单）

**在 Windows 上双击运行**: `一键打包.bat`

或在命令行运行:
```bash
python build_project.py
```

等待 5-10 分钟，打包完成后会生成：

1. **Windows 版本** - 在 `release/Windows` 文件夹（可直接使用）
2. **macOS 打包工具包** - 在 `release/macOS_打包工具包` 文件夹（需在 macOS 上打包）

---

## 📦 打包结果说明

### Windows 版本（可直接使用）

打包完成后，将 `release/Windows` 文件夹压缩发送给 Windows 用户，包含：
- `TimeTeachingSystem.exe` - 主程序
- `启动系统.bat` - 一键启动脚本（客户双击这个）
- `使用说明.txt` - 使用说明

### macOS 版本（推荐使用 Python 脚本版本）

**方式一：Python 脚本版本（推荐）⭐**
1. 将 `release/macOS_Python版本` 文件夹压缩发送给 macOS 用户
2. 用户只需安装 Python 3（macOS 通常已预装），双击 `启动系统.sh` 即可运行
3. **优点**：无需打包环境，体积小，启动快

**方式二：GitHub Actions 自动打包（开发者）**
1. 将代码推送到 GitHub
2. 在 GitHub Actions 中触发打包工作流
3. 下载打包好的 macOS 可执行文件

**方式三：本地打包工具包（需要 macOS 打包环境）**
1. 将 `release/macOS_打包工具包` 复制到 macOS 系统
2. 运行打包脚本: `./在macOS上打包.sh`

---

## 👥 客户使用方法

### Windows 用户
1. 解压文件到任意位置
2. 双击 `启动系统.bat`
3. 等待浏览器自动打开（约 3 秒）
4. 开始使用

**停止**: 在命令行窗口按 `Ctrl+C`

### macOS 用户
1. 解压文件到任意位置
2. 双击 `启动系统.sh`（或在终端运行 `./启动系统.sh`）
3. 如果提示权限不足，在终端运行: `chmod +x 启动系统.sh`
4. 等待浏览器自动打开（约 3 秒）
5. 开始使用

**停止**: 在终端窗口按 `Ctrl+C`

**注意**: 首次运行时，macOS 可能提示"无法打开，因为来自身份不明的开发者"，请右键选择"打开"。

---

## ⚙️ 打包前检查清单

- [ ] 已安装 Node.js（验证: `node --version`）
- [ ] 已安装 Python（验证: `python --version`）
- [ ] 前端依赖已安装（`cd frontend && npm install`）
- [ ] 后端依赖已安装（`cd backend && pip install -r requirements.txt`）

---

## 🔧 常见问题

**打包失败？**
- 检查 Node.js 和 Python 是否安装
- 确保所有依赖已安装

**macOS 打包工具包如何使用？**
- 将工具包复制到 macOS 系统
- 在 macOS 终端中运行 `./在macOS上打包.sh`
- 详细说明见工具包中的 `README_macOS打包说明.txt`

**客户无法运行（Windows）？**
- 检查是否被杀毒软件拦截
- 尝试以管理员身份运行
- 查看错误提示信息

**客户无法运行（macOS）？**
- 右键点击程序 → 选择"打开" → 点击"打开"确认
- 或在终端运行: `xattr -d com.apple.quarantine TimeTeachingSystem`
- 检查终端脚本权限: `chmod +x 启动系统.sh`

**端口被占用？**
- 关闭占用 5000 端口的程序
- 或修改 `backend/app.py` 中的端口后重新打包

---

## 💡 重要提示

1. **打包平台**: 必须在 Windows 上运行打包脚本
2. **Windows 版本**: 打包后可直接使用
3. **macOS 版本**: 需要将工具包复制到 macOS 系统上打包
4. **前端构建**: 前端文件只需构建一次，Windows 和 macOS 共享

---

详细说明请查看: `打包部署指南.md`
