#!/usr/bin/env python3
"""技术与开发约定：复制模板 → 核对 → 拼出执行会话的 prompt。

  python3 scripts/conventions.py init  <项目目录>
  python3 scripts/conventions.py check <项目目录>
  python3 scripts/conventions.py prompt <项目目录>

init  把 templates/CONVENTIONS.md 原样复制成 <项目目录>/CONVENTIONS.md，之后只用 Edit 改要换的条目。
check 模板里每一句带禁止或限定语气的话（不要、不在、只用……）都必须逐字留在项目的 CONVENTIONS.md 里，
      每个条目的标题也必须在。确实要删的句子（比如老板换了引擎，GDScript 那句不再成立），
      把原句抄进 <项目目录>/CONVENTIONS.waived.md，一句一行，后面写「—— 理由」。
prompt 先 check，通过后把 CONVENTIONS.md + 空行 + GDD.md 全文拼成 prompt，存到 .forge/spawn_prompt.md。
      脚本不开会话：拿这个文件的全文在项目目录开一个独立的顶层会话，怎么开见 SKILL.md 第 7 步。
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "CONVENTIONS.md"
GUARD = ("不要", "不许", "不在", "不留", "别指望", "只有", "只用", "只留", "只加载", "不用")


def norm(s):
    return re.sub(r"\s+", "", s)


def guarded_sentences(text):
    out = []
    for line in text.splitlines():
        for s in re.split(r"(?<=[。；])", line.lstrip("- ")):
            s = s.strip()
            if s and any(g in s for g in GUARD):
                out.append(s)
    return out


def titles(text):
    return [m.group(1) for m in re.finditer(r"^- ([^：\n]{1,20})：", text, re.M)]


def check(proj):
    conv = proj / "CONVENTIONS.md"
    if not conv.exists():
        sys.exit(f"没有 {conv}，先跑 init")
    tpl = TEMPLATE.read_text()
    have = norm(conv.read_text())
    waived_file = proj / "CONVENTIONS.waived.md"
    waived = norm(waived_file.read_text()) if waived_file.exists() else ""
    missing = [s for s in guarded_sentences(tpl) if norm(s) not in have and norm(s) not in waived]
    missing_titles = [t for t in titles(tpl) if norm(t + "：") not in have]
    if missing or missing_titles:
        print("CONVENTIONS.md 和模板对不上：")
        for t in missing_titles:
            print(f"  缺条目：{t}")
        for s in missing:
            print(f"  缺原句：{s}")
        print("把原句逐字放回去；确实不再成立的，抄进 CONVENTIONS.waived.md 并写理由。")
        sys.exit(1)
    print(f"约定核对通过（{len(guarded_sentences(tpl))} 句禁止/限定句，{len(titles(tpl))} 个条目）")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["init", "check", "prompt"])
    ap.add_argument("project")
    a = ap.parse_args()
    proj = Path(a.project).expanduser().resolve()

    if a.cmd == "init":
        dst = proj / "CONVENTIONS.md"
        if dst.exists():
            sys.exit(f"{dst} 已存在，不覆盖")
        shutil.copyfile(TEMPLATE, dst)
        print(f"已复制到 {dst}，只用 Edit 改需要换的条目")
        return

    check(proj)
    if a.cmd == "check":
        return

    gdd = proj / "GDD.md"
    if not gdd.exists():
        sys.exit(f"没有 {gdd}")
    prompt = (proj / "CONVENTIONS.md").read_text().rstrip() + "\n\n" + gdd.read_text()
    out = proj / ".forge" / "spawn_prompt.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(prompt)
    print(f"prompt 已写入 {out}（{len(prompt)} 字符）")
    print("下一步：在项目目录开一个独立的顶层会话，把这个文件的全文原样作为第一条消息，不改写、不只给路径。例如：")
    print(f'  cd {proj} && claude "$(cat .forge/spawn_prompt.md)"')


if __name__ == "__main__":
    main()
