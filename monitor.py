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
    except FileNotFoundError:
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
    target_file = input("Drag and drop the file to scan: ").strip('"')
    file_hash = calculate_hash(target_file)
    
    if file_hash:
        # 1. Load the existing database (Dictionary)
        baseline_db = load_baseline()
        
        # 2. Add or Update the file in the dictionary
        # The filename is the KEY, the hash is the VALUE
        baseline_db[target_file] = file_hash
        
        # 3. Save the updated dictionary back to the JSON file
        with open(DB_FILE, "w") as f:
            json.dump(baseline_db, f, indent=4)
            
        print(f"\n✅ Baseline UPDATED for: {target_file}")
        print(f"📂 Saved to {DB_FILE}")
    else:
        print("❌ Error: File not found.")

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
            print(f"🚨 DELETED: {saved_path}")
        elif current_hash == saved_hash:
            print(f"✅ SAFE:    {saved_path}")
        else:
            print(f"⚠️  CHANGED: {saved_path}")

if __name__ == "__main__":
    print("--- 🧠 SMART FILE INTEGRITY MONITOR (JSON) ---")
    
    while True:
        print("\n--------------------------------")
        print("1. Add/Update File (Smart Database)")
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