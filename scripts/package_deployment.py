"""Create a small allowlisted deployment archive; never include credentials."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]


def main():
    files = [ROOT / name for name in (
        "Dockerfile", ".dockerignore", "requirements.txt", "pyproject.toml", "data/catalog.sqlite",
        "deploy/cloudrun.sh", "deploy/smoke_container.sh", "scripts/smoke_http.py",
    )]
    files.extend(sorted((ROOT / "src/supplier_atlas").glob("*.py")))
    files.extend(sorted((ROOT / "src/supplier_atlas/web").glob("*")))
    for path in files:
        if not path.is_file():
            raise FileNotFoundError(path)
    target = ROOT / "dist/supplieratlas-demo.zip"
    target.parent.mkdir(exist_ok=True)
    with ZipFile(target, "w", ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(ROOT).as_posix())
    print(f"Packaged {len(files)} files: {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
