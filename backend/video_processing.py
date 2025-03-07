import cv2
import numpy as np
import os

PROCESSED_DIR = "processed_videos"
os.makedirs(PROCESSED_DIR, exist_ok=True)

def process_video(video_path: str, output_filename: str, dot_size: int = 5, dot_spacing: int = 10, brightness_threshold: int = 128):
    """
    Converts a video into a black-and-white dot transformation effect.
    
    :param video_path: Path to the input video
    :param output_filename: Name of the processed output file
    :param dot_size: The size of the dots in the transformed video
    :param dot_spacing: The distance between dots in the transformed video
    :param brightness_threshold: Threshold for converting grayscale to black and white
    :return: Path to the processed video
    """
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_path = os.path.join(PROCESSED_DIR, output_filename)
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=False)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply custom brightness threshold
        _, bw = cv2.threshold(gray, brightness_threshold, 255, cv2.THRESH_BINARY)

        # Create a blank canvas for the dot pattern
        dot_pattern = np.zeros_like(bw)

        # Generate dots with custom spacing
        for i in range(0, height, dot_spacing):
            for j in range(0, width, dot_spacing):
                region = bw[i:i + dot_spacing, j:j + dot_spacing]
                if np.mean(region) < brightness_threshold:  # If the region is mostly dark
                    cv2.circle(dot_pattern, (j, i), dot_size // 2, (255, 255, 255), -1)

        out.write(dot_pattern)

    cap.release()
    out.release()
    
    return output_path
