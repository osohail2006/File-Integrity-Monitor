import hashlib
import json
import os

# Define the database filename
DB_FILE = "baseline.json"

def calculate_hash(file_path):
    """Generates a SHA-256 hash for the given file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        # Added extra error handling just in case the OS blocks access to a system file
        return None

def load_baseline():
    """Helper function to load the JSON database."""
    if not os.path.exists(DB_FILE):
        return {} # Return an empty dictionary if file doesn't exist
    
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {} # Return empty if file is corrupted/empty

def create_baseline():
    target_path = input("Drag and drop a file OR folder to scan: ").strip('"').strip("'")
    
    baseline_db = load_baseline()
    files_added = 0
    
    # Check if the user dropped a SINGLE FILE
    if os.path.isfile(target_path):
        file_hash = calculate_hash(target_path)
        if file_hash:
            baseline_db[target_path] = file_hash
            files_added += 1
            print(f"✅ Baseline UPDATED for file: {target_path}")
            
    # Check if the user dropped an ENTIRE FOLDER
    elif os.path.isdir(target_path):
        print(f"\n📂 Scanning directory: {target_path}...")
        
        # os.walk hunts down every file in every sub-folder
        for root, dirs, files in os.walk(target_path):
            for file_name in files:
                # Combine the folder path and file name to get the full exact path
                full_file_path = os.path.join(root, file_name)
                
                file_hash = calculate_hash(full_file_path)
                if file_hash:
                    baseline_db[full_file_path] = file_hash
                    files_added += 1
                    
        print(f"✅ Baseline UPDATED for {files_added} files in directory.")
        
    else:
        print("❌ Error: Path not found or invalid.")
        return

    # If we successfully found and hashed files, save the updated database
    if files_added > 0:
        with open(DB_FILE, "w") as f:
            json.dump(baseline_db, f, indent=4)
        print(f"💾 Saved to {DB_FILE}")

def monitor():
    print("\n🕵️‍♂️  Scanning ALL files in Smart Database...")
    
    # 1. Load the database
    baseline_db = load_baseline()
    
    if not baseline_db:
        print("❌ Database is empty! Run Option 1 first.")
        return

    # 2. Loop through the dictionary items (Path and Hash)
    for saved_path, saved_hash in baseline_db.items():
        current_hash = calculate_hash(saved_path)

        if current_hash is None:
            print(f"🚨 DELETED or UNREADABLE: {saved_path}")
        elif current_hash == saved_hash:
            print(f"✅ SAFE:    {saved_path}")
        else:
            print(f"⚠️  CHANGED: {saved_path}")

if __name__ == "__main__":
    print("--- 🧠 SMART FILE INTEGRITY MONITOR (JSON) ---")
    
    while True:
        print("\n--------------------------------")
        print("1. Add/Update File or Folder (Smart Database)")
        print("2. Monitor Files")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            create_baseline()
        elif choice == "2":
            monitor()
        elif choice == "3":
            print("Exiting. Stay safe! 👋")
            break
        else:
            print("❌ Invalid choice.")
