from pathlib import Path
import shutil

# Script is located in the same directory as the Music folder
BASE_DIR = Path(__file__).parent
MUSIC_DIR = BASE_DIR / "Music"

# One global duplicate folder
GLOBAL_DUPLICATE_FOLDER = MUSIC_DIR / "DuplicateSizes"
GLOBAL_DUPLICATE_FOLDER.mkdir(exist_ok=True)


def get_unique_destination(folder, file):
    """
    Returns a unique destination path inside 'folder'.

    Example:
        song.mp3
        song_v2.mp3
        song_v3.mp3
    """
    destination = folder / file.name

    if not destination.exists():
        return destination

    version = 2

    while True:
        destination = folder / f"{file.stem}_v{version}{file.suffix}"

        if not destination.exists():
            return destination

        version += 1


# Process each artist separately
for artist_folder in sorted(MUSIC_DIR.iterdir()):

    # Skip non-folders and the global duplicate folder
    if (
        not artist_folder.is_dir()
        or artist_folder.name == "DuplicateSizes"
    ):
        continue

    print(f"\nScanning artist: {artist_folder.name}")

    # Reset duplicate tracking for this artist
    size_map = {}

    # Get every file under this artist
    files = sorted(
        [
            f
            for f in artist_folder.rglob("*")
            if f.is_file()
        ]
    )

    # Build size map
    for file in files:
        file_size = file.stat().st_size

        if file_size not in size_map:
            size_map[file_size] = []

        size_map[file_size].append(file)

    # Find duplicate-size groups
    duplicate_groups = {
        size: file_list
        for size, file_list in size_map.items()
        if len(file_list) > 1
    }

    # Move duplicate files (keep the first one)
    for size, file_list in duplicate_groups.items():

        print(
            f"\nDuplicate size: {size} bytes "
            f"({len(file_list)} files)"
        )

        for duplicate in file_list[1:]:

            destination = get_unique_destination(
                GLOBAL_DUPLICATE_FOLDER,
                duplicate
            )

            shutil.move(
                str(duplicate),
                str(destination)
            )

            print(
                f"Moved duplicate: "
                f"{duplicate.relative_to(artist_folder)} "
                f"-> DuplicateSizes/{destination.name}"
            )

    # Refresh file list after duplicates were moved
    remaining_files = sorted(
        [
            f
            for f in artist_folder.rglob("*")
            if f.is_file()
        ]
    )

    # Flatten artist folder
    for file in remaining_files:

        # Already in artist root
        if file.parent == artist_folder:
            continue

        destination = get_unique_destination(
            artist_folder,
            file
        )

        shutil.move(
            str(file),
            str(destination)
        )

        print(
            f"Moved to artist root: "
            f"{file.relative_to(artist_folder)} "
            f"-> {destination.name}"
        )

    # Delete empty folders (deepest first)
    folders = sorted(
        [
            d
            for d in artist_folder.rglob("*")
            if d.is_dir()
        ],
        key=lambda p: len(p.parts),
        reverse=True,
    )

    for folder in folders:
        try:
            print(f"\nChecking: {folder}")
            print("Exists:", folder.exists())
            print("Contents:", list(folder.iterdir()))

            folder.rmdir()

            print("Deleted successfully")

        except Exception as e:
            print(f"FAILED: {e}")

print("\nFinished organizing music library.")