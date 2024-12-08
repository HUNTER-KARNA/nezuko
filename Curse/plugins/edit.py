import os
from pyrogram import Client, filters
from pyrogram.types import Message
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, vfx, ImageClip
from Curse.bot_class import app

TEMP_DIR = "temp_videos"
WATERMARK_PATH = os.path.join(TEMP_DIR, "watermark.png")
BACKGROUND_IMAGE = "background.jpg"  # Set your custom background image path here
os.makedirs(TEMP_DIR, exist_ok=True)

# Command to upload a watermark image
@app.on_message(filters.command("setwatermark") & filters.photo)
async def set_watermark_image(client, message):
    await message.reply("Uploading watermark image, please wait...")

    watermark_path = await client.download_media(
        message.photo.file_id, file_name=WATERMARK_PATH
    )
    if watermark_path:
        await message.reply("Watermark image has been successfully uploaded!")
    else:
        await message.reply("Failed to upload the watermark image.")

# Command to trim a video
@app.on_message(filters.command("trim") & filters.reply)
async def trim_video(client, message):
    if not message.reply_to_message.video:
        await message.reply("Please reply to a video with the command /trim <start-end>.")
        return

    if len(message.command) < 2:
        await message.reply("Please provide the trim range. Example: /trim 5-10")
        return

    trim_range = message.command[1]
    try:
        start, end = map(int, trim_range.split("-"))
        video_path = await client.download_media(message.reply_to_message.video)
        output_path = os.path.join(TEMP_DIR, "trimmed_video.mp4")

        video = VideoFileClip(video_path).subclip(start, end)
        video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        await message.reply_video(output_path, caption="Here is your trimmed video!")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(output_path):
            os.remove(output_path)

# Command to add text to a video
@app.on_message(filters.command("addtext") & filters.reply)
async def add_text_to_video(client, message):
    if not message.reply_to_message.video:
        await message.reply("Please reply to a video with the command /addtext <'text'> <start_time>.")
        return

    if len(message.command) < 3:
        await message.reply("Please provide text and start time. Example: /addtext 'Hello' 5")
        return

    text = message.command[1].strip("'")
    start_time = int(message.command[2])

    try:
        video_path = await client.download_media(message.reply_to_message.video)
        output_path = os.path.join(TEMP_DIR, "text_video.mp4")

        video = VideoFileClip(video_path)
        text_clip = (
            TextClip(text, fontsize=50, color="white")
            .set_position("center")
            .set_duration(5)
            .set_start(start_time)
        )

        final_video = CompositeVideoClip([video, text_clip])
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        await message.reply_video(output_path, caption="Here is your video with text!")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(output_path):
            os.remove(output_path)

# Command to add watermark
@app.on_message(filters.command("addwatermark") & filters.reply)
async def add_watermark_to_video(client, message):
    if not message.reply_to_message.video:
        await message.reply("Please reply to a video with the command /addwatermark.")
        return

    if not os.path.exists(WATERMARK_PATH):
        await message.reply("No watermark image found! Please upload one using /setwatermark.")
        return

    try:
        video_path = await client.download_media(message.reply_to_message.video)
        output_path = os.path.join(TEMP_DIR, "watermarked_video.mp4")

        video = VideoFileClip(video_path)
        watermark = (
            ImageClip(WATERMARK_PATH)
            .resize(height=100)
            .set_duration(video.duration)
            .set_position(("right", "bottom"))
        )

        final_video = CompositeVideoClip([video, watermark])
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        await message.reply_video(output_path, caption="Here is your watermarked video!")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(output_path):
            os.remove(output_path)

# Command to apply filters
@app.on_message(filters.command("applyfilter") & filters.reply)
async def apply_filter(client, message):
    if not message.reply_to_message.video:
        await message.reply("Please reply to a video with the command /applyfilter <filter_name>.")
        return

    if len(message.command) < 2:
        await message.reply("Please provide a filter name. Options: blackwhite, invert")
        return

    filter_name = message.command[1]
    try:
        video_path = await client.download_media(message.reply_to_message.video)
        output_path = os.path.join(TEMP_DIR, "filtered_video.mp4")

        video = VideoFileClip(video_path)
        if filter_name == "blackwhite":
            video = video.fx(vfx.blackwhite)
        elif filter_name == "invert":
            video = video.fx(vfx.invert_colors)
        else:
            await message.reply("Invalid filter name! Use blackwhite or invert.")
            return

        video.write_videofile(output_path, codec="libx264", audio_codec="aac")
        await message.reply_video(output_path, caption="Here is your filtered video!")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(output_path):
            os.remove(output_path)
