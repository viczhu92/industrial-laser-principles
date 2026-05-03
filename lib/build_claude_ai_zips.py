#!/usr/bin/env python3
"""
build_claude_ai_zips.py

Repackage each skill in skills/ as a standalone zip suitable for upload to
Claude.ai (web app) or Claude Desktop, where each skill is uploaded
individually and must be self-contained.

Each output zip contains:
  <skill-name>/
    SKILL.md            (with ../../INSTRUCTIONS.md rewritten to INSTRUCTIONS.md)
    INSTRUCTIONS.md     (copied from repo root)
    references/         (all reference docs from references/)

Output: outputs/claude_ai_packages/<skill-name>.zip

Usage:
    python3 lib/build_claude_ai_zips.py
"""

from pathlib import Path
import re
import shutil
import zipfile

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
REFERENCES_DIR = REPO_ROOT / "references"
INSTRUCTIONS_FILE = REPO_ROOT / "INSTRUCTIONS.md"
OUTPUT_DIR = REPO_ROOT / "outputs" / "claude_ai_packages"


def rewrite_skill_md(content: str) -> str:
    """Rewrite paths in SKILL.md so it works as a self-contained bundle.

    The repo layout has SKILL.md at skills/<skill>/SKILL.md, so it references
    the shared rulebook at ../../INSTRUCTIONS.md. In a bundled zip the
    rulebook sits next to SKILL.md, so the path becomes INSTRUCTIONS.md.
    references/foo.md paths are already relative-from-skill-root and stay as-is.
    """
    return re.sub(r"\.\./\.\./INSTRUCTIONS\.md", "INSTRUCTIONS.md", content)


def build_one_skill(skill_dir: Path) -> Path:
    """Build a single skill bundle and return the zip path."""
    skill_name = skill_dir.name
    staging = OUTPUT_DIR / skill_name
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)

    skill_md_src = skill_dir / "SKILL.md"
    skill_md_dst = staging / "SKILL.md"
    skill_md_dst.write_text(rewrite_skill_md(skill_md_src.read_text()))

    shutil.copy2(INSTRUCTIONS_FILE, staging / "INSTRUCTIONS.md")

    refs_dst = staging / "references"
    refs_dst.mkdir()
    for ref in sorted(REFERENCES_DIR.glob("*.md")):
        shutil.copy2(ref, refs_dst / ref.name)

    zip_path = OUTPUT_DIR / f"{skill_name}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in sorted(staging.rglob("*")):
            if item.is_file():
                arcname = item.relative_to(OUTPUT_DIR)
                zf.write(item, arcname)

    shutil.rmtree(staging)
    return zip_path


def main() -> None:
    if not SKILLS_DIR.is_dir():
        raise SystemExit(f"skills/ not found at {SKILLS_DIR}")
    if not INSTRUCTIONS_FILE.is_file():
        raise SystemExit(f"INSTRUCTIONS.md not found at {INSTRUCTIONS_FILE}")
    if not REFERENCES_DIR.is_dir():
        raise SystemExit(f"references/ not found at {REFERENCES_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    if not skill_dirs:
        raise SystemExit(f"no skill directories with SKILL.md found in {SKILLS_DIR}")

    print(f"Building {len(skill_dirs)} Claude.ai-ready skill bundles → {OUTPUT_DIR.relative_to(REPO_ROOT)}/")
    for skill_dir in skill_dirs:
        zip_path = build_one_skill(skill_dir)
        size_kb = zip_path.stat().st_size / 1024
        print(f"  ✓ {zip_path.name:<40} ({size_kb:6.1f} KB)")

    print(f"\nDone. Upload each .zip via Claude.ai → Settings → Capabilities → Skills → + Create skill.")


if __name__ == "__main__":
    main()
