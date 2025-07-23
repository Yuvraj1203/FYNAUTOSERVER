from fynautoserver.models.index import ThemeSchema
from fynautoserver.schemas.index import Color
from fynautoserver.path_config import SRC_DIR
import os
import json


async def create_colors_db(tenantId: str, tenancyName: str, theme: ThemeSchema):
    existing = await Color.find_one({"tenantId": tenantId})
    colors_folder = f"tenant/tenants/{tenancyName}/assets/colors"
    save_path = os.path.join(SRC_DIR, colors_folder)
    index_ts_path = os.path.join(save_path, "index.ts")
    index_ts_content = f"""export const Colors = {{
    light: {json.dumps(theme.light.model_dump(), indent=2)},
    dark: {json.dumps(theme.dark.model_dump(), indent=2)}
    }};"""

    if existing:
        print("in existing")
        existing.light = theme.light
        existing.dark = theme.dark
        await existing.save()
        if os.path.exists(index_ts_path):
            with open(index_ts_path, "w", encoding="utf-8") as f:
                f.write(index_ts_content)
        else:
            os.makedirs(save_path,exist_ok=True)
            with open(index_ts_path, "w", encoding="utf-8") as f:
                f.write(index_ts_content)

        return {"message": "Colors Inserted Successfully"}
    else:
        os.makedirs(save_path, exist_ok=True)
        with open(index_ts_path, "w", encoding="utf-8") as f:
            f.write(index_ts_content)

        colors = Color(
            tenantId=tenantId or None,
            tenancyName=tenancyName or None,
            light=theme.light or None,
            dark=theme.dark or None,
        )
        await colors.insert()
        return {"message": "Colors Inserted Successfully"}
