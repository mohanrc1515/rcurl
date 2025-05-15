import time
import os
import asyncio
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram.types import Message


async def fix_thumb(thumb):
    width = 0
    height = 0
    try:
        if thumb is not None:
            parser = createParser(thumb)
            metadata = extractMetadata(parser)
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
                
            # Open the image file
            with Image.open(thumb) as img:
                # Convert the image to RGB format and save it back to the same file
                img.convert("RGB").save(thumb)
            
                # Resize the image
                resized_img = img.resize((width, height))
                
                # Save the resized image in JPEG format
                resized_img.save(thumb, "JPEG")
            parser.close()
    except Exception as e:
        print(e)
        thumb = None 
       
    return width, height, thumb
    
async def take_screen_shot(video_file, output_directory, ttl=600):  # Default to 600 seconds (10 minutes)
    """Take screenshot from 10-minute mark (600 seconds) by default"""
    out_put_file_name = f"{output_directory}/{time.time()}.jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),  # This is now set to 600 by default
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None
    
async def set_video_thumbnail(video_path, thumbnail_path=None, ttl=600):
    """
    Set thumbnail for video from 10-minute mark (600 seconds)
    If thumbnail_path is not provided, creates one in the same directory
    """
    if thumbnail_path is None:
        thumbnail_path = f"{os.path.splitext(video_path)[0]}_thumbnail.jpg"
    
    # First take screenshot from 10-minute mark
    screenshot_path = await take_screen_shot(video_path, os.path.dirname(video_path), ttl)
    
    if not screenshot_path:
        return None
    
    # Fix the thumbnail (convert to proper format)
    width, height, fixed_thumb = await fix_thumb(screenshot_path)
    
    if fixed_thumb:
        # Now set the thumbnail to the video file
        command = [
            'ffmpeg', '-y', '-i', video_path,
            '-i', fixed_thumb,
            '-map', '0', '-map', '1',
            '-c', 'copy',
            '-c:v:1', 'mjpeg',
            '-disposition:v:1', 'attached_pic',
            '-metadata:s:t', 'mimetype=image/jpeg',
            video_path + '_temp.mp4'
        ]
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        
        if os.path.exists(video_path + '_temp.mp4'):
            os.replace(video_path + '_temp.mp4', video_path)
            return fixed_thumb
    
    return None

# Keep the existing add_metadata function unchanged
async def add_metadata(input_path, output_path, metadata, ms):
    try:
        await ms.edit("<i>I Found Metadata, Adding Into Your File ⚡</i>")
        command = [
            'ffmpeg', '-y', '-i', input_path, '-map', '0', '-c:s', 'copy', '-c:a', 'copy', '-c:v', 'copy',
            '-metadata', f'title={metadata}',
            '-metadata', f'author={metadata}',
            '-metadata:s:s', f'title={metadata}',
            '-metadata:s:a', f'title={metadata}',
            '-metadata:s:v', f'title={metadata}',
            '-metadata', f'artist={metadata}',
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
        print(e_response)
        print(t_response)

        if os.path.exists(output_path):
            await ms.edit("<i>Metadata Has Been Successfully Added To Your File ✅</i>")
            return output_path
        else:
            await ms.edit("<i>Failed To Add Metadata To Your File ❌</i>")
            return None
    except Exception as e:
        print(f"Error occurred while adding metadata: {str(e)}")
        await ms.edit("<i>An Error Occurred While Adding Metadata To Your File ❌</i>")
        return None
