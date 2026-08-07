import os
import re
import glob

TEMPLATE_CONTENT = """capital = 1
set_research_slots = 3

set_politics = {
	ruling_party = authoritarianism
	last_election = "1936.1.1"
	election_frequency = 48
	elections_allowed = no
}
set_popularities = {
	communism = 12.5
	socialism = 12.5
	liberalism = 12.5
	conservatism = 12.5
	authoritarianism = 12.5
	fascism = 12.5
	national_socialism = 12.5
	despotism = 12.5
}
"""

def generate_history_files():
    tags_dir = os.path.join("..", "common", "country_tags")
    history_dir = os.path.join("..", "history", "countries")
    
    os.makedirs(history_dir, exist_ok=True)
    
    # Grab all country tag text files
    tag_files = glob.glob(os.path.join(tags_dir, "*countries.txt"))
    if not tag_files:
        print(f"[-] No valid country tag files found in {tags_dir}")
        return

    print(f"[+] Scanning tag definitions in {tags_dir}...")
    generated_count = 0
    skipped_dynamic_count = 0
    skipped_existing_count = 0

    # Pattern accounts for: TAG = "countries/Country Name.txt"
    pattern = r'([A-Z0-9]{3})\s*=\s*"countries/(.+?)\.txt"'

    for file_path in tag_files:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            file_content = f.read()
            
        # FIX 2: Skip the entire file if it contains 'dynamic_tags = yes'
        if re.search(r'dynamic_tags\s*=\s*yes', file_content, re.IGNORECASE):
            print(f"[~] Skipping dynamic tag file: {os.path.basename(file_path)}")
            skipped_dynamic_count += 1
            continue

        # Process lines within valid non-dynamic files
        for line in file_content.splitlines():
            match = re.search(pattern, line)
            if match:
                tag = match.group(1)
                country_name = match.group(2).strip()
                
                # Naming Format: "TAG - Country Name.txt"
                filename = f"{tag} - {country_name}.txt"
                dest_path = os.path.join(history_dir, filename)
                
                # FIX 1: Safely look for ANY existing history file starting with this TAG 
                # (This prevents overwriting even if the country name part was slightly edited manually)
                existing_files = glob.glob(os.path.join(history_dir, f"{tag}*.txt"))
                if existing_files:
                    skipped_existing_count += 1
                    continue
                    
                # Safe to generate if it passed the check
                with open(dest_path, "w", encoding="utf-8") as out_f:
                    out_f.write(TEMPLATE_CONTENT)
                generated_count += 1

    print("\n=== Generation Summary ===")
    print(f"[+] Successfully generated: {generated_count} new history files.")
    print(f"[~] Skipped (Dynamic Tag files): {skipped_dynamic_count}")
    print(f"[~] Skipped (Already existed on disk): {skipped_existing_count}")

if __name__ == "__main__":
    print("=== Generating Country History Logs ===")
    generate_history_files()
