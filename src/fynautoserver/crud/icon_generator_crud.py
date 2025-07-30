import shutil
import os, base64
from fastapi import APIRouter, HTTPException, UploadFile, File
from PIL import Image, ImageDraw
from fynautoserver.path_config import SRC_DIR

IOS_ICON_SIZES = [
    (20, "Icon-App-20x20@1x.png"),
    (20*2, "Icon-App-20x20@2x.png"),
    (20*3, "Icon-App-20x20@3x.png"),
    (29, "Icon-App-29x29@1x.png"),
    (29*2, "Icon-App-29x29@2x.png"),
    (29*3, "Icon-App-29x29@3x.png"),
    (40, "Icon-App-40x40@1x.png"),
    (40*2, "Icon-App-40x40@2x.png"),
    (40*3, "Icon-App-40x40@3x.png"),
    (60*2, "Icon-App-60x60@2x.png"),
    (60*3, "Icon-App-60x60@3x.png"),
    (76, "Icon-App-76x76@1x.png"),
    (76*2, "Icon-App-76x76@2x.png"),
    (83.5*2, "Icon-App-83.5x83.5@2x.png"),
    (1024, "ItunesArtwork@2x.png")
    # Add or adjust sizes as needed
]

ANDROID_LAUNCHER_ICON_SIZES = [
    (36, "mipmap-ldpi/ic_launcher.png"),
    (48, "mipmap-mdpi/ic_launcher.png"),
    (72, "mipmap-hdpi/ic_launcher.png"),
    (96, "mipmap-xhdpi/ic_launcher.png"),
    (144, "mipmap-xxhdpi/ic_launcher.png"),
    (192, "mipmap-xxxhdpi/ic_launcher.png"),
]

ANDROID_LAUNCHER_ROUNDED_ICON_SIZES = [
    (36, "mipmap-ldpi/ic_launcher_round.png"),
    (48, "mipmap-mdpi/ic_launcher_round.png"),
    (72, "mipmap-hdpi/ic_launcher_round.png"),
    (96, "mipmap-xhdpi/ic_launcher_round.png"),
    (144, "mipmap-xxhdpi/ic_launcher_round.png"),
    (192, "mipmap-xxxhdpi/ic_launcher_round.png"),
]

ANDROID_NOTIFICATION_ICON_SIZES = [
    (24, "drawable-mdpi/notification_icon.png"),
    (36, "drawable-hdpi/notification_icon.png"),
    (48, "drawable-xhdpi/notification_icon.png"),
    (72, "drawable-xxhdpi/notification_icon.png"),
    (96, "drawable-xxxhdpi/notification_icon.png")
]



def ensure_dir_exists(path: str):
    """Ensure the directory exists."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

def make_rounded_icon(input_path, output_path, size, bg_color=(255, 255, 255, 255)):
    img = Image.open(input_path).convert("RGBA")
    img = img.resize((size, size), Image.LANCZOS)

    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    background = Image.new('RGBA', (size, size), bg_color)
    rounded_icon = Image.composite(img, background, mask)

    rounded_icon.save(output_path, format="PNG")


def generate_icons(
    tenantId,tenancyName,
    app_icon_path: str,
    notification_icon_path: str,
):
    ios_output_dir: str = f"./src/tenant/tenants/{tenancyName}/Images.xcassets/AppIcon.appiconset"
    android_output_dir: str = f"./src/tenant/tenants/{tenancyName}/res"
    """
    Generates iOS and Android launcher icons from the given image.
    Uses a different icon for Android notification icons.
    """
    app_img = Image.open(app_icon_path).convert("RGBA")
    notif_img = Image.open(notification_icon_path).convert("RGBA")

    # iOS
    for size, filename in IOS_ICON_SIZES:
        out_path = os.path.join(ios_output_dir, filename)
        ensure_dir_exists(out_path)
        img_resized = app_img.resize((int(size), int(size)), Image.LANCZOS)
        img_resized.save(out_path, format="PNG")

    # Android launcher icons
    for size, rel_path in ANDROID_LAUNCHER_ICON_SIZES:
        out_path = os.path.join(android_output_dir, rel_path)
        ensure_dir_exists(out_path)
        img_resized = app_img.resize((size, size), Image.LANCZOS)
        img_resized.save(out_path, format="PNG")
    
    SCALE = 4  # Super-sampling factor (higher = smoother)
    PADDING = int(size * 0.01)

    for size, rel_path in ANDROID_LAUNCHER_ROUNDED_ICON_SIZES:
        out_path = os.path.join(android_output_dir, rel_path)
        ensure_dir_exists(out_path)

        inner_size = size - 2 * PADDING
        img_resized = app_img.resize((inner_size, inner_size), Image.LANCZOS)

        # Create high-res mask
        mask_size = (size * SCALE, size * SCALE)
        high_res_mask = Image.new("L", mask_size, 0)
        draw = ImageDraw.Draw(high_res_mask)
        offset = PADDING * SCALE
        draw.ellipse(
            (offset, offset, mask_size[0] - offset, mask_size[1] - offset),
            fill=255
        )

        # Downscale mask to target size
        mask = high_res_mask.resize((size, size), Image.LANCZOS)

        # Prepare final image
        base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        base.paste(img_resized, (PADDING, PADDING))

        rounded_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        rounded_img.paste(base, (0, 0), mask)

        rounded_img.save(out_path, format="PNG")

    # Android notification icons
    for size, rel_path in ANDROID_NOTIFICATION_ICON_SIZES:
        out_path = os.path.join(android_output_dir, rel_path)
        ensure_dir_exists(out_path)
        img_resized = notif_img.resize((size, size), Image.LANCZOS)
        img_resized.save(out_path, format="PNG")

    print("iOS and Android icons generated!")



async def generate_icons_crud(
    tenantId:str,
    tenancyName:str,
    app_icon: UploadFile = File(...),
    notification_icon: UploadFile = File(...),
    app_banner: UploadFile = File(...)
    ):
    images_folder = f"tenant/tenants/{tenancyName}/assets/images"
    save_path = os.path.join(SRC_DIR, images_folder)
    # Ensure the target folder exists
    os.makedirs(save_path, exist_ok=True)

    app_icon_bytes = await app_icon.read()  # Read file only once

    # Save app_icon
    app_icon_path = os.path.join(save_path, "appIcon.png")
    with open(app_icon_path, "wb") as f:
        f.write(app_icon_bytes)
    
    # Save banner_icon
    app_banner_path = os.path.join(save_path, "appBanner.png")
    with open(app_banner_path, "wb") as buffer:
        shutil.copyfileobj(app_banner.file, buffer)

    # Save notification_icon
    notification_icon_temp_path = os.path.join(save_path, "temp_notification_icon.png")

    # Temporary save uploads
    app_icon_temp_path = 'temp_app_icon.png'

    with open(app_icon_temp_path, "wb") as f:
        f.write(app_icon_bytes)
    with open(notification_icon_temp_path, "wb") as buffer:
        shutil.copyfileobj(notification_icon.file, buffer)

    try:
        # Generate icons as before
        generate_icons(
            tenantId,tenancyName,
            app_icon_path=app_icon_temp_path,
            notification_icon_path=notification_icon_temp_path
            
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Icon generation failed: {e}")
    finally:
        # Clean up temp files
        os.remove(app_icon_temp_path)

    source_icons = await get_icons_data(tenantId,tenancyName)
    return {"message": "Icons generated successfully!","iconsData":source_icons}

def read_file_base64(file_path: str):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
    
async def get_icons_data(tenantId:str,tenancyName:str):
    common_path = os.path.join(SRC_DIR,f"tenant/tenants/{tenancyName}/assets/images/")
    notification_image = os.path.join(SRC_DIR,common_path,"temp_notification_icon.png")

    if os.path.exists(notification_image):
        #file location
        icon_image = os.path.join(SRC_DIR, common_path,'appIcon.png')
        banner_image = os.path.join(SRC_DIR, common_path,'appBanner.png')

        response_data = {
            "appIcon": read_file_base64(icon_image) if icon_image else None,
            "bannerIcon": read_file_base64(banner_image) if banner_image else None,
            "notificationIcon": read_file_base64(notification_image) if notification_image else None,
            'success': True,
        }

        return response_data
    else:
        return {"message":'no fonts found'} 