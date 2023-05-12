import tkinter as tk
from tkinter import filedialog
from moviepy.editor import *
import os

def browse_video():
    global video_file
    video_file = filedialog.askopenfilename(title="Select a video file")
    if video_file:
        video = VideoFileClip(video_file)
        original_size_label.config(text=f"Original size: {video.size[0]}x{video.size[1]}")
        original_duration_label.config(text=f"Duration: {video.duration:.2f} seconds")
        video.close()

def convert_video():
    output_file = filedialog.asksaveasfilename(defaultextension=".avi", title="Save as")
    if not video_file or not output_file:
        return

    video = VideoFileClip(video_file)

    # Apply time window settings
    if time_window_var.get():
        start, end = map(float, time_window_var.get().split(','))
        video = video.subclip(start, end)

    # Apply crop settings
    if crop_area_var.get():
        x1, y1, x2, y2 = map(int, crop_area_var.get().split(','))
        video = video.crop(x1, y1, x2, y2)

    # Apply other settings
    video = video.resize(float(scale_var.get()))
    video = video.set_fps(int(fps_var.get()))
    video = video.fx(vfx.speedx, float(speed_var.get()))

    # Save the video with compression
    video.write_videofile(output_file, codec='mpeg4', bitrate=f"{compression_var.get()}k")

    # Cleanup
    video.close()
    os.remove("temp_audiofile.mono.wav")

root = tk.Tk()
root.title("Video Converter")

video_file = ""

# Interface
browse_button = tk.Button(root, text="Browse Video", command=browse_video)
browse_button.pack()

original_size_label = tk.Label(root, text="Original size: ")
original_size_label.pack()

original_duration_label = tk.Label(root, text="Duration: ")
original_duration_label.pack()

scale_label = tk.Label(root, text="Scale (e.g., 0.5 for half-size, 2 for double-size):")
scale_label.pack()
scale_var = tk.StringVar()
scale_var.set("1")
scale_entry = tk.Entry(root, textvariable=scale_var)
scale_entry.pack()

fps_label = tk.Label(root, text="Frame rate (e.g., 24, 30, 60):")
fps_label.pack()
fps_var = tk.StringVar()
fps_var.set("30")
fps_entry = tk.Entry(root, textvariable=fps_var)
fps_entry.pack()

speed_label = tk.Label(root, text="Speed (e.g., 0.5 for half-speed, 2 for double-speed):")
speed_label.pack()
speed_var = tk.StringVar()
speed_var.set("1")
speed_entry = tk.Entry(root, textvariable=speed_var)
speed_entry.pack()

compression_label = tk.Label(root, text="Compression in kbps (e.g., 1000, 2000):")
compression_label.pack()
compression_var = tk.StringVar()
compression_var.set("1000")
compression_entry = tk.Entry(root, textvariable=compression_var)
compression_entry.pack()

# Crop area
crop_label = tk.Label(root, text="Crop area (x1, y1, x2, y2 or leave empty):")
crop_label.pack()
crop_area_var = tk.StringVar()
crop_area_entry = tk.Entry(root, textvariable=crop_area_var)
crop_area_entry.pack()

# Time window
time_window_label = tk.Label(root, text="Time window (
