import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREFIX = "final_slide_output_"
OUTPUT_JS = ROOT / "repo_manifest.js"
OUTPUT_JSON = ROOT / "repo_manifest.json"


def discover_manifest(root: Path):
    manifest = {}

    for svg_path in sorted(root.rglob("*.svg")):
        if not svg_path.is_file() or not svg_path.name.startswith(PREFIX):
            continue

        rel_parts = svg_path.relative_to(root).parts
        if len(rel_parts) < 3:
            continue

        subject = rel_parts[0]
        topic = rel_parts[1]
        slide_id = svg_path.stem[len(PREFIX):]

        manifest.setdefault(subject, {}).setdefault(topic, []).append(slide_id)

    for subject in manifest:
        for topic in manifest[subject]:
            manifest[subject][topic] = sorted(manifest[subject][topic], key=lambda s: s.lower())

    return manifest


def write_manifest(manifest):
    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    js_content = "window.REPO_MANIFEST = " + json.dumps(manifest, indent=2) + ";\n"
    OUTPUT_JS.write_text(js_content, encoding="utf-8")


if __name__ == "__main__":
    manifest = discover_manifest(ROOT)
    write_manifest(manifest)
    print(f"Generated {OUTPUT_JSON.name} and {OUTPUT_JS.name}")
