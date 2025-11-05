import moviepy as mp
import os

def avi_to_mp4(input_path: str, output_path: str):
    """
    Converts an AVI video file to MP4 format using moviepy.

    Parameters:
        input_path (str): Path to the input .avi file
        output_path (str): Path for the output .mp4 file

    Returns:
        str: Path to the converted .mp4 file
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Ensure correct extension
    if not output_path.lower().endswith(".mp4"):
        output_path += ".mp4"

    # Load and convert
    video = mp.VideoFileClip(input_path)
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return output_path
