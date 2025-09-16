import re
from pathlib import Path

def extract_fonts_from_ts(file_path: str):
    content = Path(file_path).read_text()
    match = re.search(r"CustomFonts\s*=\s*{([^}]+)}", content, re.MULTILINE | re.DOTALL)
    fonts = {}
    if match:
        entries = match.group(1).strip().split(",")
        for entry in entries:
            if ":" in entry:
                key, value = entry.split(":", 1)
                fonts[key.strip()] = value.strip().strip('"').strip("'")
    return fonts


# Example usage
# fonts = extract_fonts_from_ts("index.tsx")
# print(fonts)
