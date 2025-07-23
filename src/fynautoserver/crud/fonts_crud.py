from typing import Optional
from fynautoserver.schemas.index import Fonts
import re
from fynautoserver.path_config import SRC_DIR
import os

def update_index_tsx(font_filename: str, tenancyName: str, role: str):

    # Normalize role (e.g., 'regular' -> 'Regular')
    role = role.strip().capitalize()
    allowed_roles = {"Light", "Regular", "Bold"}  # Extend this set if needed

    if role not in allowed_roles:
        raise ValueError(f"Invalid role '{role}'. Allowed roles are: {allowed_roles}")

    # Build file path
    colors_folder = f"tenant/tenants/{tenancyName}/assets/fonts/index.tsx"
    INDEX_TSX_PATH = os.path.join(SRC_DIR, colors_folder)

    font_name = os.path.splitext(font_filename)[0]  # Remove extension like .ttf
    new_line = f"  {role}: '{font_name}',\n"

    # Read the index.tsx file
    with open(INDEX_TSX_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Locate the start of CustomFonts object
    start_index = next((i for i, line in enumerate(lines) if "export const CustomFonts" in line), None)
    if start_index is None:
        raise ValueError("CustomFonts block not found in index.tsx")

    # Modify the role line if found, or insert it
    inside = False
    updated = False
    for i in range(start_index, len(lines)):
        if "{" in lines[i]:
            inside = True
            continue
        if inside:
            if re.match(rf"\s*{role}:\s*['\"].*?['\"],", lines[i]):
                lines[i] = new_line
                updated = True
                break
            if "}" in lines[i]:  # End of object
                if not updated:
                    lines.insert(i, new_line)
                    updated = True
                break

    # Write updated content back to file
    with open(INDEX_TSX_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"✅ Updated '{role}' font to '{font_name}' in index.tsx")


async def create_fonts_db(tenantId:str,tenancyName:str,lightFontPath:Optional[str]=None,regularFontPath:Optional[str]=None,boldFontPath:Optional[str]=None):
    fonts=Fonts(
        tenantId=tenantId or None,
        tenancyName=tenancyName or None,
        lightFontPath=lightFontPath or None,
        regularFontPath=regularFontPath or None,
        boldFontPath=boldFontPath or None
        )
    await fonts.insert()
    return {"message":'Fonts File Uploaded Successfully'}

