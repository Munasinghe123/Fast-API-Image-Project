import shutil
from pathlib import Path
from helpers.folder_creation_helper import get_raw_uploads_root
from helpers.folder_creation_helper import get_published_uploads_root


def delete_published_pole_images(pole_code: str):
    published_root = get_published_uploads_root()
    pole_dir = published_root / "Poles" / pole_code

    if pole_dir.exists():
        shutil.rmtree(pole_dir)


def publish_pole_images_from_raw(pole_code: str):
    raw_root = get_raw_uploads_root()
    published_root = get_published_uploads_root()

    raw_pole_dir = raw_root / "Poles" / pole_code
    published_pole_dir = published_root / "Poles" / pole_code

    if not raw_pole_dir.exists():
        raise RuntimeError("Raw pole folder does not exist")

    published_pole_dir.mkdir(parents=True, exist_ok=True)

    for file in raw_pole_dir.iterdir():
        if file.is_file():
            shutil.copy2(file, published_pole_dir / file.name)
            
def delete_published_line_images(line_id: str):
    published_root = get_published_uploads_root()
    line_dir = published_root / "LineSections" / line_id

    if line_dir.exists():
        shutil.rmtree(line_dir)


def publish_line_images_from_raw(line_id: str):
    raw_root = get_raw_uploads_root()
    published_root = get_published_uploads_root()

    raw_line_dir = raw_root / "LineSections" / line_id
    published_line_dir = published_root / "LineSections" / line_id

    if not raw_line_dir.exists():
        raise RuntimeError(f"RAW line folder not found: {raw_line_dir}")

    published_line_dir.parent.mkdir(parents=True, exist_ok=True)

    # Replace published folder atomically
    if published_line_dir.exists():
        shutil.rmtree(published_line_dir)

    shutil.copytree(raw_line_dir, published_line_dir)