#!/usr/bin/env python3
"""
Publish script for ComfyUI Ino Nodes.

Usage:
    python publish.py

Reads COMFY_REGISTRY_TOKEN and GITHUB_TOKEN from .env file.
Publishes to Comfy Registry and creates a GitHub release.
"""

import os
import re
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
PYPROJECT_PATH = ROOT / "pyproject.toml"
README_PATH = ROOT / "README.md"
INIT_PATH = ROOT / "__init__.py"
ENV_PATH = ROOT / ".env"


def load_env():
    """Load .env file into environment."""
    if not ENV_PATH.exists():
        print(f"Warning: .env file not found at {ENV_PATH}")
        print("Create one with:")
        print("  COMFY_REGISTRY_TOKEN=your_token_here")
        print("  GITHUB_TOKEN=your_token_here")
        return

    with open(ENV_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")


def get_current_version() -> str:
    """Read current version from pyproject.toml."""
    content = PYPROJECT_PATH.read_text()
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        print("Error: Could not find version in pyproject.toml")
        sys.exit(1)
    return match.group(1)


def bump_patch(version: str) -> str:
    """Increment patch version: 1.3.2 -> 1.3.3"""
    parts = version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


def set_version(old_version: str, new_version: str):
    """Update version in pyproject.toml, README.md, and __init__.py."""
    # pyproject.toml
    content = PYPROJECT_PATH.read_text()
    content = re.sub(r'version\s*=\s*"[^"]+"', f'version = "{new_version}"', content)
    PYPROJECT_PATH.write_text(content)
    print(f"  Updated pyproject.toml")

    # README.md
    if README_PATH.exists():
        content = README_PATH.read_text()
        updated = content.replace(old_version, new_version)
        if updated != content:
            README_PATH.write_text(updated)
            print(f"  Updated README.md")
        else:
            print(f"  README.md — no version string found to replace")

    # __init__.py
    if INIT_PATH.exists():
        content = INIT_PATH.read_text()
        updated = re.sub(r'__version__\s*=\s*"[^"]+"', f'__version__ = "{new_version}"', content)
        if updated != content:
            INIT_PATH.write_text(updated)
            print(f"  Updated __init__.py")
        else:
            print(f"  __init__.py — no __version__ found to replace")

    print(f"Version set to {new_version}")


def run(cmd: list[str], check=True, env=None) -> subprocess.CompletedProcess:
    """Run a command and print it."""
    print(f"\n> {' '.join(cmd)}")
    merged_env = {**os.environ, **(env or {})}
    result = subprocess.run(cmd, capture_output=True, text=True, env=merged_env)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    if check and result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        sys.exit(1)
    return result


def git_commit_and_tag(version: str):
    """Commit version bump and create a git tag."""
    run(["git", "add", "pyproject.toml", "README.md", "__init__.py"])
    run(["git", "commit", "-m", f"Release v{version}"])
    run(["git", "tag", f"v{version}"])
    print(f"Created git tag v{version}")


def git_push():
    """Push commits and tags to remote."""
    run(["git", "push"])
    run(["git", "push", "--tags"])
    print("Pushed to remote with tags")


def publish_comfy_registry(token: str):
    """Publish to Comfy Registry using comfy-cli."""
    print("\n> comfy node publish --token ***")
    result = subprocess.run(["comfy", "node", "publish", "--token", token])
    if result.returncode != 0:
        print(f"Comfy Registry publish exited with code {result.returncode}")
    else:
        print("Published to Comfy Registry")


def create_github_release(version: str):
    """Create a GitHub release using gh CLI (uses existing gh auth)."""
    print(f"\n> gh release create v{version}")
    result = subprocess.run(
        ["gh", "release", "create", f"v{version}",
         "--title", f"v{version}",
         "--notes", f"Release v{version}",
         "--latest"],
    )
    if result.returncode != 0:
        print(f"GitHub release creation exited with code {result.returncode}")
    else:
        print(f"Created GitHub release v{version}")


def main():
    os.chdir(Path(__file__).parent)
    load_env()

    current = get_current_version()
    auto_next = bump_patch(current)

    print(f"Current version: {current}")
    print(f"Auto next:       {auto_next}")
    print()

    user_input = input(f"Enter new version [{auto_next}]: ").strip()
    new_version = user_input if user_input else auto_next

    if new_version == current:
        print("Version unchanged. Aborting.")
        sys.exit(0)

    print(f"\nPublishing v{new_version}")
    print("=" * 40)

    # Update version in all files
    set_version(current, new_version)

    # Git commit + tag
    git_commit_and_tag(new_version)

    # Push
    confirm = input("\nPush to remote and publish? [y/N]: ").strip().lower()
    if confirm != "y":
        print("Aborted. Version is committed locally but not pushed.")
        print(f"To undo: git reset --soft HEAD~1 && git tag -d v{new_version}")
        sys.exit(0)

    git_push()

    # Publish to Comfy Registry
    comfy_token = os.environ.get("COMFY_REGISTRY_TOKEN", "")
    if comfy_token:
        try:
            publish_comfy_registry(comfy_token)
        except SystemExit:
            print("Warning: Comfy Registry publish failed. Continuing...")
    else:
        print("Skipping Comfy Registry (COMFY_REGISTRY_TOKEN not set)")

    # Create GitHub release (uses existing gh auth)
    import shutil
    if shutil.which("gh"):
        try:
            create_github_release(new_version)
        except Exception as e:
            print(f"Warning: GitHub release creation failed: {e}")
    else:
        print("Skipping GitHub release ('gh' CLI not installed)")
        print(f"  Create manually: gh release create v{new_version} --title 'v{new_version}' --latest")

    print(f"\nDone! v{new_version} published.")


if __name__ == "__main__":
    main()
