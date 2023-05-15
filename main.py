import tkinter as tk
import datetime
from tkinter import filedialog
from moviepy.editor import *
from PIL import ImageTk, Image
import os

def browse_video():
    # Function to browse and select a video file
    global video_file
    video_file = filedialog.askopenfilename(title="Select a video file")
    if video_file:
        video = VideoFileClip(video_file)
        original_size_label.config(text=f"Original size: {video.size[0]}x{video.size[1]}")
        original_duration_label.config(text=f"Duration: {video.duration:.2f} seconds")
        original_fps_label.config(text=f"Original FPS: {video.fps}")  
        video.close()

def show_frame():
    # Function to show a specific frame of the video
    if not video_file:
        return

    frame_time = float(frame_time_var.get())
    video = VideoFileClip(video_file)
    frame = video.get_frame(frame_time)

    # Convert the frame to an image
    image = Image.fromarray(frame)

    # # Resize the image to fit within the window
    # width, height = image.size
    # max_width = 300
    # max_height = 200
    # if width > max_width or height > max_height:
    #     image.thumbnail((max_width, max_height), Image.ANTIALIAS)
    
    # Display the image
    frame_image = ImageTk.PhotoImage(image)
    frame_image_label.configure(image=frame_image)
    frame_image_label.image = frame_image

    video.close()

def convert_video():
    # Function to convert and save the video with selected settings
    output_extension = ".mp4" if format_var.get() == "mp4" else ".avi"
    output_file = filedialog.asksaveasfilename(defaultextension=output_extension, title="Save as")

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
    
    # Remove audio if selected
    if remove_audio_var.get():
        video = video.without_audio()

    # Save the video with compression and selected format
    if format_var.get() == "mp4":
        video.write_videofile(output_file, codec='libx264', audio_codec='aac', bitrate=f"{compression_var.get()}k", fps=int(fps_var.get()), remove_temp=True)
    elif format_var.get() == "avi":
        video.write_videofile(output_file, codec='mpeg4', audio_codec='aac', bitrate=f"{compression_var.get()}k", fps=int(fps_var.get()), remove_temp=True)
    
    # Save video properties to a text file
    properties_file = output_file.replace(output_extension, '.txt')
    with open(properties_file, 'w') as f:
        f.write(f"Original video: {video_file}\n")
        f.write(f"Time of generation: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Original FPS: {video.fps}\n")  
        f.write(f"New FPS: {fps_var.get()}\n")
        f.write(f"Compression: {compression_var.get()} kbps\n")
        if crop_area_var.get():
            f.write(f"Crop area: {crop_area_var.get()}\n")
        if time_window_var.get():
            f.write(f"Time window: {time_window_var.get()}\n")
        if original_scale_var.get():
            f.write(f"Original scale: {original_scale_var.get()} um/pxl\n")
            new_scale = float(original_scale_var.get()) / float(scale_var.get())
            f.write(f"New scale: {new_scale:.2f} um/pxl\n")
            
        # Cleanup
        video.close()

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

original_fps_label = tk.Label(root, text="Original FPS: ")
original_fps_label.pack()

scale_label = tk.Label(root, text="Scale (e.g., 0.5 for half-size, 2 for double-size):")
scale_label.pack()
scale_var = tk.StringVar()
scale_var.set("1")
scale_entry = tk.Entry(root, textvariable=scale_var)
scale_entry.pack()

original_scale_label = tk.Label(root, text="Original scale (um/pxl or leave empty):")
original_scale_label.pack()
original_scale_var = tk.StringVar()
original_scale_entry = tk.Entry(root, textvariable=original_scale_var)
original_scale_entry.pack()

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
time_window_label = tk.Label(root, text="Time window (start, end in seconds or leave empty):")
time_window_label.pack()
time_window_var = tk.StringVar()
time_window_entry = tk.Entry(root, textvariable=time_window_var)
time_window_entry.pack()

# Remove audio
remove_audio_var = tk.BooleanVar()
remove_audio_checkbox = tk.Checkbutton(root, text="Remove Audio", variable=remove_audio_var)
remove_audio_checkbox.pack()

# Select format
format_var = tk.StringVar(value="mp4")
format_label = tk.Label(root, text="Output Format:")
format_label.pack()

format_frame = tk.Frame(root)
format_frame.pack()

mp4_radio = tk.Radiobutton(format_frame, text="MP4", variable=format_var, value="mp4")
mp4_radio.pack(side=tk.LEFT)

avi_radio = tk.Radiobutton(format_frame, text="AVI", variable=format_var, value="avi")
avi_radio.pack(side=tk.LEFT)

# Convert
convert_button = tk.Button(root, text="Convert Video", command=convert_video)
convert_button.pack()


root.mainloop()

