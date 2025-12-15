import os
import shutil

def organize_music_repository(music_root_dir):
    """
    Goes into artist folders, then album folders, and moves music files 
    inside the album folders up to the artist folder.
    Renames files if a file with the same name already exists in the artist folder.
    
    Args:
        music_root_dir (str): The path to the main music folder.
    """
    print(f"Starting music repository organization in: {music_root_dir}")
    
    # 1. Iterate over all items in the music root directory
    for item in os.listdir(music_root_dir):
        artist_dir = os.path.join(music_root_dir, item)
        
        # Check if the item is an artist directory
        if os.path.isdir(artist_dir):
            print(f"\nProcessing Artist: {item}")
            
            # 2. Iterate over items inside the artist directory (looking for album folders)
            for sub_item in os.listdir(artist_dir):
                album_dir = os.path.join(artist_dir, sub_item)
                
                # Check if the item is an album directory
                if os.path.isdir(album_dir):
                    print(f"  > Entering Album: {sub_item}")
                    
                    # 3. Iterate over files inside the album directory
                    for filename in os.listdir(album_dir):
                        source_file_path = os.path.join(album_dir, filename)
                        
                        # Check if it's a file (and not a nested folder)
                        if os.path.isfile(source_file_path):
                            target_filename = filename
                            target_file_path = os.path.join(artist_dir, target_filename)
                            
                            copy_count = 0
                            
                            # Handle file name conflicts
                            while os.path.exists(target_file_path):
                                copy_count += 1
                                # Create a new filename: original_name_copy_i.ext
                                name, ext = os.path.splitext(filename)
                                target_filename = f"{name}_copy_{copy_count}{ext}"
                                target_file_path = os.path.join(artist_dir, target_filename)
                            
                            try:
                                # Move the file (shutil.move handles moving across drives if necessary)
                                shutil.move(source_file_path, target_file_path)
                                
                                if copy_count == 0:
                                    print(f"    - Moved: {filename}")
                                else:
                                    print(f"    - Moved and Renamed: {filename} -> {target_filename}")
                                    
                            except Exception as e:
                                print(f"    - Error moving {filename}: {e}")
                                
                    # Optional: Remove the now-empty album directory
                    try:
                        os.rmdir(album_dir)
                        print(f"  > Cleaned up (removed empty) Album folder: {sub_item}")
                    except OSError as e:
                        print(f"  > Could not remove Album folder {sub_item}: {e}")
                        
# --- Main Execution Block ---
if __name__ == "__main__":
    # Define the root music directory (adjust this path for your system)
    # Using 'Music_Repo' as the default folder name next to this script
    music_repo_path = os.path.join(os.getcwd(), "Music_Repo") 
    
    # Check if the directory exists before proceeding
    if not os.path.exists(music_repo_path):
        print(f"Error: The music repository folder was not found at {music_repo_path}")
        print("Please run 'create_simulation_data.py' first, or update the 'music_repo_path'.")
    else:
        organize_music_repository(music_repo_path)
        print("\n--- Organization Complete! ---")