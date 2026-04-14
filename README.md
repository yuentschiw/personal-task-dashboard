**English** | [中文](README.zh-CN.md)

# 🌸 Personal Task Dashboard

An AI-managed task dashboard hosted on **GitHub Pages**, with **JSONBin** as the cross-device cloud backend. Your AI agent (Raika / OpenClaw) reads and writes tasks directly — you just talk to it.

> Built for people who want a lightweight, always-synced task board without installing anything. Works on phone, laptop, or any browser.

## What You Get

A personal Kanban-style task board at a public GitHub Pages URL, with:

- **Priority-sorted task cards** — P0 (High) / P1 (Medium) / P2 (Low), sorted by added date within each level
- **Cross-device sync** — edit on your laptop, see updates on your phone instantly (powered by JSONBin)
- **Agent-managed** — add, complete, delete, and archive tasks just by talking to your AI
- **Scheduled cron jobs** — morning kickoff, status updates every 2h, evening report, midnight archive, weekly maintenance
- **Fully customisable** — title, emoji, colours all editable in the HTML template

## How It Works

```
You ──talk──► Agent (Raika)
                  │
          reads / writes
                  │
              JSONBin  ◄──── browser auto-loads on open
(source of truth)
                  │
          (agent pushes)
                  │
           GitHub Pages ──► you (phone / laptop / any browser)
```

**Why JSONBin?**
GitHub Pages is static — it can't store data. JSONBin provides a tiny cloud JSON store that both the browser and the agent can read/write via a simple REST API. The browser fetches your tasks on every page load; the agent pushes changes whenever you ask. This gives you real-time cross-device sync without any server or database to maintain.

The JSONBin key embedded in the HTML is scoped to a single bin — it cannot access your account or other bins. Your GitHub token (used by the agent to push HTML updates) is stored separately in `dashboard-config.json` and **never** put in the public HTML.

## Quick Start

### 1. Create a JSONBin

1. Sign up at [jsonbin.io](https://jsonbin.io)
2. Create a new **private** bin with this initial value:
   ```json
   {"activeTasks":[],"completedTasks":[],"archivedDates":[]}
   ```
3. Copy your **Bin ID** and **Master Key** (from the bin settings)

### 2. Set up the dashboard

1. Fork or clone this repo
2. Open `assets/task-dashboard.html` — find these two lines near the top of the `<script>` section:
   ```js
   const BIN_ID  = 'REPLACE_BIN_ID';
   const BIN_KEY = 'REPLACE_BIN_KEY';
   ```
   Replace with your actual Bin ID and Master Key.

3. Customise your dashboard (see [Customisation](#customisation) below)

4. Enable GitHub Pages on your repo (Settings → Pages → Branch: `main`, folder: `/ (root)`)

5. Push your `task-dashboard.html` — your dashboard is live at:
   `https://<your-github-username>.github.io/<repo-name>/task-dashboard.html`

### 3. Configure your agent

Create `dashboard-config.json` in your agent workspace (this file stays **off** GitHub):

```json
{
  "github_token": "ghp_your_token_here",
  "repo_owner": "your-github-username",
  "repo_name": "your-repo-name",
  "file_path": "task-dashboard.html",
  "dashboard_url": "https://your-github-username.github.io/your-repo-name/task-dashboard.html"
}
```

Generate a GitHub token at Settings → Developer settings → Personal access tokens → Fine-grained, with `Contents: Read and write` on your repo.

### 4. Install the skill

```bash
# OpenClaw
clawhub install personal-task-dashboard

# Or manually — place this folder in your skills directory
```

Tell your agent: **"add today's tasks to dashboard"** — and you're done.

## Customisation

Open `assets/task-dashboard.html` and find the `<!-- CUSTOMISE -->` section near the top of `<body>`:

| What | Where in HTML | Example |
|------|--------------|---------|
| Page title (browser tab) | `<title>` tag | `<title>🌸 My Workspace</title>` |
| Dashboard heading | `<h1>` inside `#header` | `<h1>🌸 YQ's Workstation</h1>` |
| Subtitle text | `.subtitle` div | `渠道策略中台 · Daily Focus` |
| Background colour | `body { background-color: ... }` | `#faf9f5` → any hex |
| Card accent colour | `.task-card` border styles | adjust `border-left` colour |
| Scale (zoom level) | `body { transform: scale(...) }` | `0.8` → `1.0` for full size |

## Scheduled Automation

Five cron jobs run automatically if you've set them up with your agent:

| Time (CST) | Job | What it does |
|------------|-----|-------------|
| 07:30 daily | Morning Kickoff | Lists yesterday's pending tasks, asks what you're adding today |
| 09/11/13/15/17:00 | Status Update | Checks active tasks, flags blockers |
| 19:00 daily | Evening Report | Today's completed / incomplete / tomorrow's plan |
| 00:00 daily | Midnight Archive | Moves completed tasks to archive, grouped by date |
| Sat 09:00 | Weekly Maintenance | Cleans stale tasks, generates weekly summary |

To set these up, tell your agent: **"set up dashboard cron jobs"**.

## Talking to Your Agent

You can manage everything through conversation:

- `"Add P0 task: finish the proposal"`
- `"Mark 'finish the proposal' as done"`
- `"What are my P0 tasks today?"`
- `"Delete the Vlog task"`
- `"Show me the dashboard link"`
- `"Set up the morning kickoff cron"`

## Privacy

- Your task data lives in your own JSONBin (a private bin — only you and your agent can access it)
- The JSONBin Master Key in the HTML controls only that one bin
- Your GitHub token is stored locally in `dashboard-config.json`, never pushed to GitHub
- No third-party tracking or analytics

## License

MIT
