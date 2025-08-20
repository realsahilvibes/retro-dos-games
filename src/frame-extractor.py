from PIL import Image
import os

gif_path = "assets/heli.gif"
frames_folder = "assets/heli_frames"
os.makedirs(frames_folder, exist_ok=True)

max_width = 60  # desired max width of helicopter frames

gif = Image.open(gif_path)
frame_count = 0

try:
    while True:
        gif.seek(frame_count)
        frame = gif.convert('RGBA')

        # Calculate new height preserving aspect ratio
        wpercent = (max_width / float(frame.size[0]))
        hsize = int((float(frame.size[1]) * float(wpercent)))

        resized_frame = frame.resize((max_width, hsize), Image.Resampling.LANCZOS)

        frame_path = f"{frames_folder}/frame_{frame_count}.png"
        resized_frame.save(frame_path)
        print(f"Saved resized frame {frame_count}: {frame_path}")

        frame_count += 1
except EOFError:
    print(f"Extracted and resized {frame_count} frames.")
