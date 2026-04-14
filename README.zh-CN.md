[English](README.md) | **中文**

# 🌸 个人任务看板

一个由 AI 管理、托管在 **GitHub Pages** 上的个人任务看板，以 **JSONBin** 作为跨设备云端数据后端。你的 AI 助手（Raika / OpenClaw）直接读写任务——你只需要开口说话。

> 专为不想安装任何软件、又需要随时同步任务的人设计。手机、电脑、任何浏览器都能用。

## 你会得到什么

一个托管在 GitHub Pages 上的个人看板，包含：

- **按优先级排列的任务卡片** — P0（紧急）/ P1（重要）/ P2（普通），同优先级内按添加时间排列
- **跨设备实时同步** — 电脑上加的任务，手机刷新就能看到（由 JSONBin 支撑）
- **AI 全程管理** — 直接对话就能添加、完成、删除、归档任务
- **定时自动化** — 早安汇报、每2小时状态更新、晚间总结、午夜归档、每周维护
- **完全可自定义** — 标题、emoji、配色都可以在 HTML 模板里改

## 工作原理

```
你 ──开口说──► AI 助手（Raika）
                   │
             读取 / 写入
                   │
               JSONBin  ◄──── 浏览器每次打开自动加载
    （数据唯一来源）
                   │
          （AI 推送 HTML 更新）
                   │
            GitHub Pages ──► 你（手机 / 电脑 / 任何浏览器）
```

**为什么用 JSONBin？**

GitHub Pages 是静态托管，无法存储数据。JSONBin 提供了一个极简的云端 JSON 存储，浏览器和 AI 助手都可以通过 REST API 读写。每次打开页面时浏览器自动拉取最新任务，AI 每次操作后推送变更，实现真正的跨设备实时同步——不需要维护任何服务器或数据库。

嵌入在 HTML 里的 JSONBin Key 只能操作你这一个 Bin，不能访问你的账号或其他数据。用于推送 HTML 的 GitHub Token 单独存放在本地 `dashboard-config.json` 中，**绝对不会**出现在公开的 HTML 里。

## 快速开始

### 第一步：创建 JSONBin

1. 注册 [jsonbin.io](https://jsonbin.io)
2. 创建一个**私有** Bin，初始值填：
   ```json
   {"activeTasks":[],"completedTasks":[],"archivedDates":[]}
   ```
3. 复制 **Bin ID** 和 **Master Key**（在 Bin 设置里）

### 第二步：配置看板

1. Fork 或 clone 这个仓库
2. 打开 `assets/task-dashboard.html`，找到 `<script>` 开头的这两行：
   ```js
   const BIN_ID  = 'REPLACE_BIN_ID';
   const BIN_KEY = 'REPLACE_BIN_KEY';
   ```
   替换成你自己的 Bin ID 和 Master Key。

3. 按需自定义看板（见下方[自定义](#自定义)说明）

4. 在仓库里开启 GitHub Pages（Settings → Pages → Branch: `main`，文件夹：`/ (root)`）

5. 推送 `task-dashboard.html`，你的看板就上线了：
   `https://<你的GitHub用户名>.github.io/<仓库名>/task-dashboard.html`

### 第三步：配置 AI 助手

在 AI 助手的工作目录创建 `dashboard-config.json`（这个文件**不要推送到 GitHub**）：

```json
{
  "github_token": "ghp_你的token",
  "repo_owner": "你的GitHub用户名",
  "repo_name": "仓库名",
  "file_path": "task-dashboard.html",
  "dashboard_url": "https://你的GitHub用户名.github.io/仓库名/task-dashboard.html"
}
```

GitHub Token 在这里生成：Settings → Developer settings → Personal access tokens → Fine-grained，勾选 `Contents: Read and write`。

### 第四步：安装 Skill

```bash
# OpenClaw
clawhub install personal-task-dashboard

# 手动安装——把这个文件夹放到你的 skills 目录里
```

然后告诉 AI 助手：**"今天的任务加进 dashboard"**，就完成了。

## 自定义

打开 `assets/task-dashboard.html`，找到文件开头的可自定义区域：

| 想改什么 | 在 HTML 里的位置 | 示例 |
|---------|----------------|------|
| 页面标题（浏览器标签页） | `<title>` 标签 | `<title>🌸 我的工作台</title>` |
| 看板大标题 | `#header` 里的 `<h1>` | `<h1>🌸 YQ 的工作台</h1>` |
| 副标题 | `.subtitle` div | `渠道策略中台 · 今日专注` |
| 背景颜色 | `body { background-color: ... }` | `#faf9f5` → 任意十六进制颜色 |
| 卡片强调色 | `.task-card` 的 `border-left` | 改颜色值 |
| 整体缩放比例 | `body { transform: scale(...) }` | `0.8` → `1.0` 显示原始大小 |

## 定时自动化

如果你已经让 AI 助手配置了 cron jobs，以下任务会自动执行：

| 时间（北京时间）| 任务 | 内容 |
|--------------|------|------|
| 每天 07:30 | 早安汇报 | 列出昨日未完成任务，询问今天要新增什么 |
| 每天 09/11/13/15/17:00 | 状态更新 | 检查进行中任务，标记 blockers |
| 每天 19:00 | 晚间总结 | 今日完成/未完成/明日计划/阻塞项汇总 |
| 每天 00:00 | 午夜归档 | 把已完成任务归档（按日期分组），清空已完成列 |
| 每周六 09:00 | 每周维护 | 清理重复/过期任务，生成周报 |

告诉 AI 助手：**"帮我配置 dashboard 的定时任务"** 即可。

## 怎么跟 AI 说话管理任务

什么都可以直接说：

- `"加一个 P0 任务：完成提案"`
- `"把'完成提案'标记为完成"`
- `"我今天有哪些 P0 任务？"`
- `"删掉 Vlog 那个任务"`
- `"给我 dashboard 的链接"`
- `"帮我配置早安汇报 cron"`

## 隐私说明

- 你的任务数据存在你自己的 JSONBin（私有 Bin，只有你和你的 AI 能访问）
- HTML 里嵌入的 JSONBin Key 只能操作那一个 Bin
- GitHub Token 只存在本地 `dashboard-config.json`，不会推送到 GitHub
- 没有任何第三方追踪或统计

## 开源协议

MIT
