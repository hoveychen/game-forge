#!/usr/bin/env python3
"""Stop hook：收工前强制检查接力纪律。

检查两件事：
1. 代码在上一次主线通关之后有没有改动（有改动就必须重跑）；
2. HANDOFF.md 是否在主线通关之后更新过，顶部条目是否写了「主线通关：」。

主线通关命令必须把输出写到 .game-forge/golden-path.log（例如 `npm run golden 2>&1 | tee .game-forge/golden-path.log`）。

本会话没有改动代码（纯咨询）时直接放行：SessionStart 时记录基线，Stop 时对比。
注意 Stop 在每个回合结束时都会触发：改了代码之后想停下来问老板，也得先重跑主线、写交接——这是有意的，
不许在红色状态下把球交回给老板。连续拦截 3 次后放行并提示，检查一旦通过就清零。

注册方式（项目的 .claude/settings.json）：
{
  "hooks": {
    "SessionStart": [
      {"hooks": [{"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.game-forge/check-relay.py\" start"}]}
    ],
    "Stop": [
      {"hooks": [{"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.game-forge/check-relay.py\" stop"}]}
    ]
  }
}
"""
import json
import os
import subprocess
import sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
LOG = os.path.join(ROOT, ".game-forge", "golden-path.log")
HANDOFF = os.path.join(ROOT, "HANDOFF.md")
MAX_BLOCKS = 3  # 同一会话最多拦 3 次，防止死循环
IGNORED = ("HANDOFF.md", "BUGLOG.md", ".game-forge/")


def git(*args):
    # 不要 strip：porcelain 格式的行首空格是状态位的一部分
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def latest_change_time():
    """工作区里未提交改动的最新 mtime，与 HEAD 提交时间，两者取大。"""
    times = []
    head = git("log", "-1", "--format=%ct").strip()
    if head:
        times.append(int(head))
    changed = git("status", "--porcelain").splitlines()
    for line in changed:
        path = line[3:].split(" -> ")[-1]
        if path.startswith(IGNORED):
            continue
        full = os.path.join(ROOT, path)
        if os.path.exists(full):
            times.append(int(os.path.getmtime(full)))
    return max(times) if times else 0


def counter_path(session_id):
    return os.path.join(ROOT, ".game-forge", f".blocks-{session_id}")


def block(reason, session_id):
    """连续拦截计数；检查通过时清零（见 main 末尾）。"""
    counter = counter_path(session_id)
    n = int(open(counter).read()) if os.path.exists(counter) else 0
    if n >= MAX_BLOCKS:
        os.remove(counter)
        msg = f"[game-forge] 连续拦截 {n} 次仍未满足接力纪律，放行。未满足项：{reason}"
        print(json.dumps({"systemMessage": msg}, ensure_ascii=False))
        return
    os.makedirs(os.path.dirname(counter), exist_ok=True)
    with open(counter, "w") as f:
        f.write(str(n + 1))
    print(json.dumps({"decision": "block", "reason": f"[game-forge 接力纪律] {reason}"}, ensure_ascii=False))


def passed(session_id):
    if os.path.exists(counter_path(session_id)):
        os.remove(counter_path(session_id))


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    session_id = payload.get("session_id", "unknown")
    mode = sys.argv[1] if len(sys.argv) > 1 else "stop"
    baseline_file = os.path.join(ROOT, ".game-forge", f".baseline-{session_id}")

    change_t = latest_change_time()

    if mode == "start":
        os.makedirs(os.path.dirname(baseline_file), exist_ok=True)
        with open(baseline_file, "w") as f:
            f.write(str(change_t))
        return

    baseline = int(open(baseline_file).read()) if os.path.exists(baseline_file) else 0
    if change_t <= baseline:
        passed(session_id)
        return  # 本会话没有改动代码，放行

    log_t = int(os.path.getmtime(LOG)) if os.path.exists(LOG) else 0

    if change_t > log_t:
        block("代码在上一次主线通关之后有改动。收工前必须重跑主线通关脚本（输出写到 .game-forge/golden-path.log），再更新 HANDOFF.md。", session_id)
        return

    if not os.path.exists(HANDOFF) or int(os.path.getmtime(HANDOFF)) < log_t:
        block("跑过主线通关之后还没有更新 HANDOFF.md。按 RELAY.md 的格式在顶部追加本棒记录。", session_id)
        return

    with open(HANDOFF, encoding="utf-8") as f:
        head = f.read(2000)
    if "主线通关：" not in head:
        block("HANDOFF.md 顶部条目缺少「主线通关：」一行。第一行永远是主线通关状态。", session_id)
        return

    passed(session_id)


if __name__ == "__main__":
    main()
