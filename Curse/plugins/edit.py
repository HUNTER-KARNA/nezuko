import os
from pyrogram import Client, filters
from pyrogram.types import Message
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, vfx, ImageClip
from Curse.bot_class import app


TEMP_DIR = "temp_videos"
WATERMARK_PATH = os.path.join(TEMP_DIR, "watermark.png")
os.makedirs(TEMP_DIR, exist_ok=True)


@app.on_message(filters.command("seltpic") & filters.photo)
async def set_watermark_image(client, message):
    await message.reply("Uploading watermark image, please wait...")

    # Download and save the uploaded watermark image
    watermark_path = await client.download_media(
        message.photo.file_id, file_name=WATERMARK_PATH
    )
    if watermark_path:
        await message.reply("Watermark image has been successfully uploaded!")
    else:
        await message.reply("Failed to upload the watermark image.")


@app.on_message(filters.command("edit") & filters.reply)
async def edit_video(client, message):
    if not message.reply_to_message.video:
        await message.reply("Please reply to a video with the command /edit <instructions>.")
        return

    if len(message.command) < 2:
        await message.reply(
            "Please provide instructions! Example: /edit trim 5-10 add_text 'Hello' at 3, watermark, speed 2"
        )
        return

    instructions = message.text.split(" ", 1)[1]
    await message.reply("Processing your video, please wait...")

    video_path = await client.download_media(message.reply_to_message.video)
    output_path = os.path.join(TEMP_DIR, "edited_video.mp4")

    try:
        video = VideoFileClip(video_path)

        # Trim video
        if "trim" in instructions:
            trim_range = instructions.split("trim")[1].split()[0].strip()
            start, end = map(int, trim_range.split("-"))
            video = video.subclip(start, end)

        # Add text
        if "add_text" in instructions:
            text_params = instructions.split("add_text")[1].split("at")[0].strip()
            text = text_params.split("'")[1]
            time = int(instructions.split("at")[1].split(",")[0].strip())
            text_clip = (
                TextClip(text, fontsize=50, color="white")
                .set_position("center")
                .set_duration(5)
                .set_start(time)
            )
            video = CompositeVideoClip([video, text_clip])

        # Add watermark
        if "watermark" in instructions and os.path.exists(WATERMARK_PATH):
            watermark = (
                ImageClip(WATERMARK_PATH)
                .resize(height=100)
                .set_duration(video.duration)
                .set_position(("right", "bottom"))
            )
            video = CompositeVideoClip([video, watermark])

        # Apply filters
        if "filter" in instructions:
            filter_type = instructions.split("filter")[1].split()[0].strip()
            if filter_type == "blackwhite":
                video = video.fx(vfx.blackwhite)
            elif filter_type == "invert":
                video = video.fx(vfx.invert_colors)

        # Adjust speed
        if "speed" in instructions:
            speed_factor = float(instructions.split("speed")[1].split()[0].strip())
            video = video.fx(vfx.speedx, speed_factor)

        # Mirror effect
        if "mirror" in instructions:
            video = video.fx(vfx.mirror_x)

        # Reverse effect
        if "reverse" in instructions:
            video = video.fx(vfx.time_mirror)

        # Export the edited video
        video.write_videofile(output_path, codec="libx264", audio_codec="aac")
        await message.reply_video(output_path, caption="Here's your edited video!")

    except Exception as e:
        await message.reply(f"An error occurred: {e}")

    finally:
        # Clean up temporary files
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(output_path):
            os.remove(output_path)


