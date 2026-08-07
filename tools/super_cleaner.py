import os
import re

def clean_and_destroy():
    # Look for 02_missing_tags.txt in the root mod folder or the tags folder
    possible_paths = [
        os.path.join("..", "02_missing_tags.txt"),
        os.path.join("..", "common", "country_tags", "02_missing_tags.txt")
    ]
    
    missing_tags_file = None
    for path in possible_paths:
        if os.path.exists(path):
            missing_tags_file = path
            break
            
    if not missing_tags_file:
        print("[-] 02_missing_tags.txt not found. Nothing to clean up.")
        return

    # 1. Extract the ghost tags
    missing_tags = set()
    print(f"[+] Reading ghost tags from: {missing_tags_file}")
    with open(missing_tags_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip().startswith("#"):
                continue
            for tag in re.findall(r'\b[A-Z0-9]{3}\b', line):
                missing_tags.add(tag)

    if not missing_tags:
        print("[-] No valid 3-letter tags found in the file. Skipping colors.txt update.")
        return

    # 2. Clean colors.txt
    colors_path = os.path.join("..", "common", "countries", "colors.txt")
    if os.path.exists(colors_path):
        with open(colors_path, "r", encoding="utf-8") as f:
            content = f.read()

        output = []
        pos = 0
        length = len(content)
        purged_count = 0

        while pos < length:
            match = re.search(r'([A-Z0-9]{3})\s*=\s*\{', content[pos:])
            if not match:
                output.append(content[pos:])
                break
                
            start_match = pos + match.start()
            tag = match.group(1)
            output.append(content[pos:start_match])
            
            brace_count = 1
            block_end = start_match + match.end()
            
            while block_end < length and brace_count > 0:
                char = content[block_end]
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                block_end += 1
                
            if tag not in missing_tags:
                output.append(content[start_match:block_end])
            else:
                purged_count += 1
                
            pos = block_end

        with open(colors_path, "w", encoding="utf-8") as f:
            f.writelines(output)
        print(f"[+] Cleaned colors.txt! Removed {purged_count} ghost tag blocks.")
    else:
        print(f"[-] colors.txt not found at {colors_path}. Skipping color updates.")

    # 3. Self-destruct the missing tags file
    try:
        os.remove(missing_tags_file)
        print(f"[+] Successfully deleted {os.path.basename(missing_tags_file)}.")
    except Exception as e:
        print(f"[-] Failed to delete file: {e}")

if __name__ == "__main__":
    print("=== Running Ghost Tag Purge & File Cleanup ===")
    clean_and_destroy()
