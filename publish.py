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

PYPROJECT_PATH = Path(__file__).parent / "pyproject.toml"
ENV_PATH = Path(__file__).parent / ".env"


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


def set_version(new_version: str):
    """Update version in pyproject.toml."""
    content = PYPROJECT_PATH.read_text()
    content = re.sub(r'version\s*=\s*"[^"]+"', f'version = "{new_version}"', content)
    PYPROJECT_PATH.write_text(content)
    print(f"Updated pyproject.toml to version {new_version}")


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
    run(["git", "add", "pyproject.toml"])
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
    run(
        ["comfy", "node", "publish"],
        env={"COMFY_REGISTRY_TOKEN": token},
    )
    print("Published to Comfy Registry")


def create_github_release(version: str, token: str):
    """Create a GitHub release using gh CLI."""
    run(
        ["gh", "release", "create", f"v{version}",
         "--title", f"v{version}",
         "--notes", f"Release v{version}",
         "--latest"],
        env={"GH_TOKEN": token},
    )
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

    # Update version
    set_version(new_version)

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

    # Create GitHub release
    github_token = os.environ.get("GITHUB_TOKEN", "")
    if github_token:
        try:
            create_github_release(new_version, github_token)
        except SystemExit:
            print("Warning: GitHub release creation failed. Continuing...")
    else:
        print("Skipping GitHub release (GITHUB_TOKEN not set)")

    print(f"\nDone! v{new_version} published.")


if __name__ == "__main__":
    main()
