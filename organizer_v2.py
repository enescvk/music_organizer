from pathlib import Path
import shutil

# Script is located in the same directory as the Music folder
BASE_DIR = Path(__file__).parent
MUSIC_DIR = BASE_DIR / "Music"


def get_unique_destination(folder, file):
    """
    Creates a unique filename inside the destination folder.
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


for artist_folder in MUSIC_DIR.iterdir():

    # Only process artist folders
    if not artist_folder.is_dir():
        continue

    print(f"\nScanning artist: {artist_folder.name}")

    # Reset for every artist
    size_map = {}

    # Find all files inside artist folder and album subfolders
    for file in artist_folder.rglob("*"):

        if not file.is_file():
            continue

        # Do not scan already moved duplicates
        if "DuplicateSizes" in file.parts:
            continue

        file_size = file.stat().st_size

        if file_size not in size_map:
            size_map[file_size] = []

        size_map[file_size].append(file)


    # Find groups where size appears more than once
    duplicate_groups = {
        size: files
        for size, files in size_map.items()
        if len(files) > 1
    }


    if not duplicate_groups:
        print("No duplicate sizes found.")
        continue


    duplicate_folder = artist_folder / "DuplicateSizes"
    duplicate_folder.mkdir(exist_ok=True)


    for size, files in duplicate_groups.items():

        print(
            f"\nDuplicate size found: {size} bytes "
            f"({len(files)} files)"
        )

        # Keep the first file, move the rest
        files_to_move = files[1:]

        for file in files_to_move:

            destination = get_unique_destination(
                duplicate_folder,
                file
            )

            shutil.move(
                str(file),
                str(destination)
            )

            print(
                f"Moved: {file.relative_to(artist_folder)} "
                f"-> {destination.name}"
            )


print("\nFinished organizing duplicates.")