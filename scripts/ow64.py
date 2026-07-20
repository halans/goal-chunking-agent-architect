#!/usr/bin/env python3
"""
ow64.py — scaffold, validate, and render an Open Window 64 (OW64) mandala chart.

Part of the `harada-agent-architect` skill. Pure Python 3 standard library — no deps.

An OW64 file is JSON of the form:

    {
      "goal": "one-line central goal",
      "pillars": [
        { "theme": "Pillar 1 name", "actions": ["a1", ..., "a8"] },
        ... exactly 8 pillars, each with exactly 8 actions ...
      ]
    }

Commands:
    blank    [--out FILE] [--pillars "A,B,..."]        Emit an empty (or pillar-seeded) OW64 file.
    validate FILE                                      Check 8 pillars x 8 non-empty actions. Exit 1 if incomplete.
    render   FILE [--out FILE] [--format md|html]      Render the 9x9 mandala as Markdown or a styled HTML page.

The render format defaults to Markdown, but is inferred as HTML when --out ends
in .html/.htm. Pass --format to override. HTML output is a single self-contained
page (embedded CSS, no external assets or dependencies).

Examples:
    python3 ow64.py blank --out my.ow64.json
    python3 ow64.py validate my.ow64.json
    python3 ow64.py render my.ow64.json --out my.ow64.md
    python3 ow64.py render my.ow64.json --out my.ow64.html          # HTML (inferred)
    python3 ow64.py render my.ow64.json --format html > my.html     # HTML (explicit)
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from typing import Any, Dict, List, Tuple

DEFAULT_PILLARS = [
    "Goal & Scope Mastery",
    "Context & Knowledge",
    "Planning & Decomposition",
    "Tools & Actions",
    "Execution Quality",
    "Verification & Validation",
    "Error Handling & Resilience",
    "Communication & Handoff",
]


def _load(path: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        sys.exit(f"error: file not found: {path}")
    except json.JSONDecodeError as exc:
        sys.exit(f"error: {path} is not valid JSON: {exc}")


def _check_structure(data: Dict[str, Any]) -> List[str]:
    """Return a list of problems (empty list == valid)."""
    problems: List[str] = []
    if not isinstance(data, dict):
        return ["top level must be a JSON object"]
    if not str(data.get("goal", "")).strip():
        problems.append("missing central 'goal'")
    pillars = data.get("pillars")
    if not isinstance(pillars, list):
        return problems + ["'pillars' must be a list"]
    if len(pillars) != 8:
        problems.append(f"expected 8 pillars, found {len(pillars)}")
    for i, pillar in enumerate(pillars, start=1):
        theme = str(pillar.get("theme", "")).strip() if isinstance(pillar, dict) else ""
        if not theme:
            problems.append(f"pillar {i}: missing 'theme'")
        actions = pillar.get("actions") if isinstance(pillar, dict) else None
        if not isinstance(actions, list):
            problems.append(f"pillar {i} ({theme or '?'}): 'actions' must be a list")
            continue
        if len(actions) != 8:
            problems.append(f"pillar {i} ({theme or '?'}): expected 8 actions, found {len(actions)}")
        for j, action in enumerate(actions, start=1):
            if not str(action).strip():
                problems.append(f"pillar {i} ({theme or '?'}): action {j} is empty")
    return problems


def cmd_blank(args: argparse.Namespace) -> int:
    if args.pillars:
        themes = [p.strip() for p in args.pillars.split(",") if p.strip()]
    else:
        themes = list(DEFAULT_PILLARS)
    if len(themes) != 8:
        sys.exit(f"error: need exactly 8 pillars, got {len(themes)}")
    data = {
        "goal": "",
        "pillars": [{"theme": t, "actions": ["", "", "", "", "", "", "", ""]} for t in themes],
    }
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"wrote blank OW64 scaffold to {args.out}")
    else:
        print(text)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    data = _load(args.file)
    problems = _check_structure(data)
    filled = 0
    pillars = data.get("pillars", []) if isinstance(data, dict) else []
    if isinstance(pillars, list):
        for pillar in pillars:
            if isinstance(pillar, dict) and isinstance(pillar.get("actions"), list):
                filled += sum(1 for a in pillar["actions"] if str(a).strip())
    if problems:
        print(f"INCOMPLETE — {filled}/64 action cells filled. Problems:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"OK — valid OW64: 8 pillars x 8 actions = {filled}/64 cells filled.")
    return 0


def _grid(data: Dict[str, Any]) -> List[List[str]]:
    """Build the 9x9 mandala grid. Center block holds goal + 8 themes; outer blocks hold actions."""
    goal = str(data.get("goal", "")).strip() or "(goal)"
    pillars = data.get("pillars", [])
    # positions of the 8 outer blocks around the center block (block row, block col)
    block_pos = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    # position of each theme cell within the center block (around its center)
    around = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    grid = [["" for _ in range(9)] for _ in range(9)]

    # center block = block (1,1): center cell is the goal, ring cells are the 8 themes
    grid[4][4] = f"**GOAL: {goal}**"
    for idx, (dr, dc) in enumerate(around):
        theme = ""
        if idx < len(pillars) and isinstance(pillars[idx], dict):
            theme = str(pillars[idx].get("theme", "")).strip()
        grid[3 + dr][3 + dc] = f"[{idx + 1}] {theme}"

    # each outer block: center = theme, ring = its 8 actions
    for idx, (br, bc) in enumerate(block_pos):
        base_r, base_c = br * 3, bc * 3
        theme, actions = "", []
        if idx < len(pillars) and isinstance(pillars[idx], dict):
            theme = str(pillars[idx].get("theme", "")).strip()
            actions = pillars[idx].get("actions", []) or []
        grid[base_r + 1][base_c + 1] = f"**[{idx + 1}]** _{theme}_"
        for a_idx, (dr, dc) in enumerate(around):
            val = str(actions[a_idx]).strip() if a_idx < len(actions) else ""
            grid[base_r + dr][base_c + dc] = val
    return grid


def render_markdown(data: Dict[str, Any]) -> str:
    """Render the 9x9 mandala as a Markdown table plus an outline."""
    goal = str(data.get("goal", "")).strip() or "(goal)"
    pillars = data.get("pillars", [])
    grid = _grid(data)

    lines: List[str] = []
    lines.append(f"# Open Window 64 — {goal}\n")
    lines.append("## 9x9 mandala\n")
    lines.append("|" + "|".join(f" {c} " for c in range(1, 10)) + "|")
    lines.append("|" + "|".join([" --- "] * 9) + "|")
    for row in grid:
        cells = [(c or " ").replace("\n", " ").replace("|", "\\|") for c in row]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("\n## Outline\n")
    lines.append(f"**Goal:** {goal}\n")
    for idx, pillar in enumerate(pillars, start=1):
        if not isinstance(pillar, dict):
            continue
        theme = str(pillar.get("theme", "")).strip()
        lines.append(f"\n### {idx}. {theme}")
        for a in pillar.get("actions", []) or []:
            a = str(a).strip()
            lines.append(f"- {a}" if a else "- _(empty)_")
    return "\n".join(lines) + "\n"


# Light background / accent colour for each of the 8 pillars (index 0-7).
PILLAR_COLORS: List[Tuple[str, str]] = [
    ("#fdecec", "#ef4444"),
    ("#fdefe0", "#f97316"),
    ("#fef7d6", "#eab308"),
    ("#e7f8ee", "#22c55e"),
    ("#e0f5f1", "#14b8a6"),
    ("#e6effd", "#3b82f6"),
    ("#eaebfd", "#6366f1"),
    ("#f4e9fd", "#a855f7"),
]


def _normalize_pillars(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return exactly 8 pillars, each with a theme and exactly 8 action strings."""
    raw = data.get("pillars", []) or []
    out: List[Dict[str, Any]] = []
    for i in range(8):
        theme, acts = "", []
        if i < len(raw) and isinstance(raw[i], dict):
            theme = str(raw[i].get("theme", "")).strip()
            acts = raw[i].get("actions", []) or []
        acts = [str(a).strip() for a in acts][:8]
        acts += [""] * (8 - len(acts))
        out.append({"theme": theme, "actions": acts})
    return out


def render_html(data: Dict[str, Any]) -> str:
    """Render the mandala as a single self-contained HTML page (embedded CSS, no deps)."""
    goal = str(data.get("goal", "")).strip() or "(goal)"
    pillars = _normalize_pillars(data)

    # Visual layout: a 3x3 of blocks. The center block (1,1) holds the goal + the
    # 8 themes; each other block holds a pillar's theme (hub) + its 8 actions.
    block_pos = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    around = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    around_index = {pos: k for k, pos in enumerate(around)}
    pillar_at_block = {pos: idx for idx, pos in enumerate(block_pos)}

    def esc(s: Any) -> str:
        return html.escape(str(s), quote=True)

    def cell(text: str, klass: str, style: str = "", badge: str = "") -> str:
        badge_html = f'<span class="badge">{esc(badge)}</span>' if badge else ""
        if str(text).strip():
            return f'<div class="{klass}" style="{style}">{badge_html}<span class="t">{esc(text)}</span></div>'
        return f'<div class="{klass} empty" style="{style}">{badge_html}<span class="t">·</span></div>'

    blocks_html: List[str] = []
    for br in range(3):
        for bc in range(3):
            cells: List[str] = []
            if (br, bc) == (1, 1):
                for r2 in range(3):
                    for c2 in range(3):
                        if (r2, c2) == (1, 1):
                            cells.append(cell(goal, "cell hub goal"))
                        else:
                            k = around_index[(r2, c2)]
                            _, edge = PILLAR_COLORS[k]
                            cells.append(cell(pillars[k]["theme"], "cell theme-mini",
                                              style=f"border-left:4px solid {edge}", badge=str(k + 1)))
                blocks_html.append('<div class="block goal-block" '
                                   'style="background:#fff7e6;border-color:#d4a017">'
                                   + "".join(cells) + "</div>")
            else:
                idx = pillar_at_block[(br, bc)]
                bg, edge = PILLAR_COLORS[idx]
                for r2 in range(3):
                    for c2 in range(3):
                        if (r2, c2) == (1, 1):
                            cells.append(cell(pillars[idx]["theme"], "cell hub theme",
                                              style=f"color:{edge}", badge=str(idx + 1)))
                        else:
                            k = around_index[(r2, c2)]
                            cells.append(cell(pillars[idx]["actions"][k], "cell action"))
                blocks_html.append(f'<div class="block" style="background:{bg};border-color:{edge}">'
                                   + "".join(cells) + "</div>")

    legend_html = '<ul class="legend">' + "".join(
        f'<li><span class="sw" style="background:{PILLAR_COLORS[i][1]}"></span>'
        f'<span><b>{i + 1}.</b> {esc(p["theme"] or "(theme)")}</span></li>'
        for i, p in enumerate(pillars)
    ) + "</ul>"

    outline_html = "".join(
        f'<section class="op"><h3><span class="badge2" style="background:{PILLAR_COLORS[i][1]}">{i + 1}</span>'
        f'{esc(p["theme"] or "(theme)")}</h3><ol>'
        + "".join(f"<li>{esc(a)}</li>" if a else '<li class="empty">(empty)</li>' for a in p["actions"])
        + "</ol></section>"
        for i, p in enumerate(pillars)
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Open Window 64 — {esc(goal)}</title>
<style>
  :root {{ color-scheme: light; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; padding: 32px 20px 56px; background: #f6f7f9; color: #1f2937;
         font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
         -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .wrap {{ max-width: 1120px; margin: 0 auto; }}
  header h1 {{ font-size: 22px; margin: 0 0 4px; letter-spacing: .3px; }}
  header p {{ margin: 0 0 20px; color: #6b7280; font-size: 14px; }}
  .mandala {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
  .block {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px;
           padding: 8px; border: 2px solid #d1d5db; border-radius: 14px; }}
  .cell {{ background: #fff; border: 1px solid rgba(0,0,0,.07); border-radius: 8px;
          min-height: 78px; padding: 7px 8px; font-size: 11.5px; line-height: 1.25; overflow: hidden; }}
  .cell .t {{ display: block; }}
  .hub {{ display: flex; flex-direction: column; align-items: center; justify-content: center;
         text-align: center; font-weight: 700; font-size: 12px; }}
  .goal {{ background: #fffaf0; }}
  .goal.hub {{ font-size: 12.5px; }}
  .theme-mini {{ font-weight: 600; }}
  .action {{ color: #374151; }}
  .empty {{ color: #c4c9d0; }}
  .badge {{ display: inline-block; min-width: 15px; height: 15px; margin-right: 4px; padding: 0 3px;
           border-radius: 4px; background: #eef0f3; color: #4b5563; font-size: 9.5px; font-weight: 700;
           text-align: center; line-height: 15px; }}
  .goal-block .badge {{ background: transparent; }}
  ul.legend {{ list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(230px,1fr));
              gap: 6px 16px; padding: 0; margin: 22px 0 6px; font-size: 13px; }}
  ul.legend li {{ display: flex; align-items: center; gap: 8px; }}
  .sw {{ width: 12px; height: 12px; border-radius: 3px; flex: none; }}
  h2.sec {{ font-size: 15px; margin: 30px 0 10px; padding-bottom: 6px; border-bottom: 1px solid #e5e7eb; }}
  .outline {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px,1fr)); gap: 10px 24px; }}
  .op h3 {{ font-size: 13.5px; margin: 8px 0 6px; display: flex; align-items: center; gap: 8px; }}
  .badge2 {{ color: #fff; font-size: 10px; min-width: 17px; height: 17px; line-height: 17px;
            text-align: center; border-radius: 5px; }}
  .op ol {{ margin: 0 0 6px; padding-left: 20px; font-size: 12.5px; color: #374151; }}
  .op ol li {{ margin: 2px 0; }}
  footer {{ margin-top: 34px; color: #9ca3af; font-size: 11.5px; text-align: center; }}
  @media (max-width: 820px) {{ .cell {{ min-height: 66px; font-size: 10.5px; }} }}
  @media print {{ body {{ background: #fff; padding: 0; }} .block, .op {{ break-inside: avoid; }} }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Open Window 64</h1>
    <p>{esc(goal)}</p>
  </header>
  <div class="mandala">
{"".join(blocks_html)}
  </div>
  {legend_html}
  <h2 class="sec">Outline</h2>
  <div class="outline">{outline_html}</div>
  <footer>Generated by goal-chunking-agent-architect</footer>
</div>
</body>
</html>
"""


def cmd_render(args: argparse.Namespace) -> int:
    data = _load(args.file)
    fmt = args.format
    if fmt is None:
        out = (args.out or "").lower()
        fmt = "html" if out.endswith((".html", ".htm")) else "md"
    text = render_html(data) if fmt == "html" else render_markdown(data)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {fmt} mandala to {args.out}")
    else:
        print(text)
    return 0


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scaffold, validate, and render an OW64 mandala.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_blank = sub.add_parser("blank", help="emit an empty OW64 scaffold")
    p_blank.add_argument("--out", help="write to FILE instead of stdout")
    p_blank.add_argument("--pillars", help="comma-separated list of exactly 8 pillar names")
    p_blank.set_defaults(func=cmd_blank)

    p_val = sub.add_parser("validate", help="check 8x8 completeness")
    p_val.add_argument("file", help="OW64 JSON file")
    p_val.set_defaults(func=cmd_validate)

    p_render = sub.add_parser("render", help="render the 9x9 mandala as Markdown or HTML")
    p_render.add_argument("file", help="OW64 JSON file")
    p_render.add_argument("--out", help="write to FILE instead of stdout")
    p_render.add_argument("--format", choices=["md", "html"], default=None,
                          help="output format (default: md, or html if --out ends in .html/.htm)")
    p_render.set_defaults(func=cmd_render)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())