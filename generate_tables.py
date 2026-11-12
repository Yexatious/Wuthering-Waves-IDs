"""Regenerate the GitHub tables from data/*.json with Python 3."""
import argparse
from collections import defaultdict
import json
from pathlib import Path


NAV = "[Home](README.md) · [Characters](characters.md) · [Monsters](monsters.md) · [Weapons](weapons.md)"
WEAPON_TYPES = ("Broadblades", "Swords", "Pistols", "Gauntlets", "Rectifiers")


def table(columns, rows):
    return "\n".join("| " + " | ".join(c.replace("|", r"\|") for c in row) + " |"
                     for row in (columns, ("---",) * len(columns), *rows))


def code(value):
    return f"{chr(96)}{value}{chr(96)}" if value else "—"


def display_name(record):
    name = record["name"] or "Name unavailable"
    return name + " (tentative)" if record["verification"] == "tentative" else name


def portrait(record):
    path = record["thumbnail"]
    return f"![{record['name'] or 'Portrait'}]({path})" if path else "—"


def versions(records):
    return ", ".join(dict.fromkeys(record["verified_against"] for record in records))


def characters(records):
    rows = [(portrait(r), display_name(r), code(r["codename"]), ", ".join(map(code, r["role_ids"])) or "—")
            for r in records]
    return ("Role IDs may be shared across Rover variants.\n\n"
            + table(("Portrait", "In-game name", "Code name", "Role IDs"), rows))


def monsters(records):
    groups = defaultdict(list)
    for r in records:
        key = (r["name"], r["head_icon"], r["thumbnail"]) if r["name"] and r["head_icon"] else (r["monster_id"],)
        groups[key].append(r)
    rows = []
    for group in groups.values():
        r = group[0]
        rows.append((portrait(r), display_name(r), ", ".join(code(e["monster_id"]) for e in group), code(r["head_icon"])))
    return ("Every game record retains its ID. Entries with the same name and portrait are grouped here.\n\n"
            + table(("Portrait", "In-game name", "Monster IDs", "Head icon"), rows)
            + "\n\n## Verified artwork paths\n\n"
            + table(("In-game name", "Export path"), [
                ("Fleurdelys", code("Aki/UI/UIResources/Common/Image/ImgBoss/T_Boss_34012")),
                ("Fractsidus Ripper", code("Aki/UI/UIResources/Common/Image/IconMonsterHead/T_IconMonsterHead_31085_UI")),
            ]))


def weapons(records):
    sections = []
    for weapon_type in WEAPON_TYPES:
        rows = [(portrait(r), display_name(r), code(r["item_id"]), code(r["model_id"]), code(r["icon"]))
                for r in records if r["weapon_type"] == weapon_type]
        sections.append(f"## {weapon_type}\n\n"
                        + table(("Portrait", "In-game name", "Item ID", "Model ID", "UI texture"), rows))
    return "\n\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if any table differs from the registry.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    for render, title in ((characters, "Characters"), (monsters, "Monsters"), (weapons, "Weapons")):
        name = title.lower()
        records = json.loads((root / "data" / f"{name}.json").read_text(encoding="utf-8"))
        for record in records:
            if record["thumbnail"] and not (root / record["thumbnail"]).is_file():
                raise SystemExit(f"Missing thumbnail: {record['thumbnail']}")
        logo = '<img src="wuwa-wordmark.png" width="240" alt="Wuthering Waves">\n\n' if name == "characters" else ""
        content = (f"{NAV}\n\n{logo}# {title}\n\nVerified against **{versions(records)}**. "
                   f"[Sources and verification](SOURCES.md)\n\n{render(records)}\n")
        path = root / f"{name}.md"
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"{path.name} is out of date. Run python generate_tables.py.")
        else:
            path.write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
