"""Build a student-only archive. Draft utility; not executed during authoring."""

import argparse
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

RESOURCE_ROOT = Path(__file__).resolve().parent.parent / "Student" / "Resources"
FILES = (
    "README.md",
    ".env.sample",
    ".gitignore",
    "requirements.txt",
    "workshop.py",
    ".devcontainer/devcontainer.json",
    "data/sources.json",
    "data/questions.json",
    "data/safety.json",
    "elastic/context-automation.md",
    "infra/README.md",
    "infra/main.bicep",
    "infra/deploy.sh",
    "notebooks/00-Setup.ipynb",
    "notebooks/01-Brut-Force.ipynb",
    "notebooks/02-Context-Engine.ipynb",
    "notebooks/04-Evaluate.ipynb",
    "notebooks/99-Cleanup.ipynb",
)


def main():
    parser = argparse.ArgumentParser(description="Package only allowlisted student resources.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output.suffix != ".zip" or output.is_relative_to(RESOURCE_ROOT.resolve()):
        raise ValueError("Choose a .zip staging destination outside Student/Resources.")
    for relative in FILES:
        source = RESOURCE_ROOT / relative
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"Missing file or unexpected symlink: {relative}")
        if source.suffix == ".ipynb":
            notebook = json.loads(source.read_text(encoding="utf-8"))
            if any(cell.get("outputs") or cell.get("execution_count") is not None for cell in notebook["cells"]):
                raise ValueError(f"Clear notebook execution/output before packaging: {relative}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "x", compression=ZIP_DEFLATED) as archive:
        for relative in FILES:
            archive.write(RESOURCE_ROOT / relative, arcname=relative)
    print(f"Created {output} with {len(FILES)} allowlisted student files.")


if __name__ == "__main__":
    main()
