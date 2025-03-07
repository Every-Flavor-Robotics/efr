from pathlib import Path

import requests

HARDWARE_LICENSE_PATH = "https://raw.githubusercontent.com/Every-Flavor-Robotics/licenses/refs/heads/main/hardware_license.md"
SOFTWARE_LICENSE_PATH = "https://raw.githubusercontent.com/Every-Flavor-Robotics/licenses/refs/heads/main/software_license.md"
GITIGNORE_TEMPLATES = {
    "Python": "https://www.toptal.com/developers/gitignore/api/python",
    "PlatformIO": "https://www.toptal.com/developers/gitignore/api/platformio",
    "Rust": "https://www.toptal.com/developers/gitignore/api/rust",
}


def create_readme(repo_root: Path, repo_name: str, repo_description: str, emoji: str):
    template_path = Path(__file__).parent / "templates" / "README.md.template"
    template_content = template_path.read_text(encoding="utf-8")
    readme_content = template_content.format(
        name=repo_name, description=repo_description, emoji=emoji
    )
    (repo_root / "README.md").write_text(readme_content, encoding="utf-8")


def create_license(repo_root: Path, project_type: str):
    license_url = (
        HARDWARE_LICENSE_PATH if project_type == "hardware" else SOFTWARE_LICENSE_PATH
    )
    license_content = requests.get(license_url).text
    (repo_root / "LICENSE").write_text(license_content, encoding="utf-8")


def create_gitignore(repo_root: Path, selected_templates: list):
    gitignore_content = "".join(
        requests.get(GITIGNORE_TEMPLATES[t]).text for t in selected_templates
    )
    (repo_root / ".gitignore").write_text(gitignore_content, encoding="utf-8")
