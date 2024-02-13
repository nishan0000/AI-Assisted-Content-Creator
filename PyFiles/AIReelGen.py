#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append('../Output Files')
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, AudioFileClip
import os
from datetime import datetime
import shutil

import warnings
warnings.filterwarnings('ignore')


# ### Project Initiation

# In[2]:


def create_project():
    
    year = str(datetime.now().year)
    month = str(datetime.now().month)
    day = str(datetime.now().day)
    hour = str(datetime.now().hour)
    minute = str(datetime.now().minute)
    second = str(datetime.now().second)
    micro_second = str(datetime.now().microsecond)

    project_id = year + month + day + hour + minute + second + micro_second
    
    return project_id


# In[3]:



def create_project_folder(project_id):
    
    output_folder_path = '..\\Output Files'
    project_output_folder_path = os.path.join(output_folder_path, project_id)    
    if not os.path.exists(project_output_folder_path):
        os.mkdir(project_output_folder_path)
        
    project_input_folder_path = os.path.join(project_output_folder_path, 'Input Files')
    if not os.path.exists(project_input_folder_path):
        os.mkdir(project_input_folder_path)
        
    return 200


# In[4]:


def extract_audio(video_file, project_id):
    """Function to extract audio from a video file and save it as an mp3"""
    try:
        # load video
        clip = VideoFileClip(video_file)

        # extract audio
        audio = clip.audio

        # save audio as mp3
        audio.write_audiofile(f'../Output Files/{project_id}/Audio.mp3')

        return 200

    except:
        pass


# In[5]:


def generate_video_w(video_file, project_id):
    
    """Function to create a video with 1080 px width and n height"""
    
    try:
        # Saving the audio of video as mp3
        extract_audio(video_file, project_id)
        
        # load video
        cap = cv2.VideoCapture(video_file)

        # get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(f'../Output Files/{project_id}/Bardotics W Video.mp4', fourcc, fps, (1080, height))

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                # create a blank canvas
                canvas = np.zeros((height, 1080, 3), dtype=np.uint8)

                # calculate new width of the frame
                new_width = 1066 - 14

                # resize frame
                frame = cv2.resize(frame, (new_width, height))

                # place the frame onto the canvas
                canvas[:, 14:14+new_width] = frame

                # write the frame
                out.write(canvas)
            else:
                break

        # release everything
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        return 200
    
    except Exception as e:
        print(str(e))
        return 401


# In[6]:


def generate_header_image(text, project_id):
    
    """Function to generate Header image with logo"""
    
    try:
    
        # Load the image
        image_path = r"../Hardcodes/Templates/Bardotics header.png"  # Replace with the path to your image file


        background = Image.open(image_path)

        # Load the font
        font_path = r"../Hardcodes\Fonts\GothamBook.ttf"  # Replace with the path to your Gotham font file
        font_size = 35
        font = ImageFont.truetype(font_path, int(font_size))

        # Create a draw object
        draw = ImageDraw.Draw(background)

        # Set the text and color
        text_color = (255, 255, 255)  # White color

        # Set the starting and ending columns for the text
        start_col = 14
        end_col = 1066

        # Calculate the width and height of the text
        tw, text_height = draw.textsize(text, font=font)

        # Calculate the width of the slice of the background
        background_slice_width = end_col - start_col

        # Split the text into words
        words = text.split()

        # Initialize a list to hold the lines of text
        lines = []
        line = ""

        # Create lines of text that fit within the specified width
        for word in words:
            if draw.textsize(line + word, font=font)[0] <= background_slice_width:
                line += word + " "
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)

        # Set the line spacing
        line_spacing = 12  # Change this value to adjust the line spacing

        # Calculate the total height of the text
        total_text_height = len(lines) * (text_height + line_spacing)

        # Calculate the starting y position to center the text vertically
        start_y = 106

        # Draw each line of text on the image
        for i, line in enumerate(lines):
            y = start_y + i * (text_height + line_spacing)
            draw.text((start_col, y), line, fill=text_color, font=font)

        # Calculate the cutting pixel (Bottom)
        cutting_px = y + text_height + 26

        # Cut the image
        background = background.crop((0, 0, background.width, cutting_px))

        # Save the image
        background.save(f'../Output Files/{project_id}/Bardotics H Img.png')
        
        return 200
    except Exception as e:
        print(str(e))
        return 401



# In[7]:


def combine_img_vid(project_id):
    
    try:

        # specify video file path
        video_file = f"../Output Files/{project_id}/Bardotics W Video.mp4"

        # specify image file path
        image_file = f"../Output Files/{project_id}/Bardotics H Img.png"

        # load video
        cap = cv2.VideoCapture(video_file)

        # get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # load image
        image = cv2.imread(image_file)

        # resize image to match video width
        image = cv2.resize(image, (width, image.shape[0]))

        # create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(fr"../Output Files/{project_id}/Bardotics Combined Video.mp4", fourcc, fps, (width, height + image.shape[0]))

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                # create a blank canvas
                canvas = np.zeros((height + image.shape[0], width, 3), dtype=np.uint8)

                # place the image onto the canvas
                canvas[:image.shape[0], :] = image

                # place the frame onto the canvas
                canvas[image.shape[0]:, :] = frame

                # write the frame
                out.write(canvas)
            else:
                break

        # release everything
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        return 200
    except Exception as e:
        print(str(e))
        return 401


# In[8]:


def generate_final_video(project_id):

    try:
        # specify video file path
        video_file = fr"../Output Files/{project_id}/Bardotics Combined Video.mp4"

        # load video
        cap = cv2.VideoCapture(video_file)

        # get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # create a blank canvas
        canvas = np.zeros((1920, 1080, 3), dtype=np.uint8)

        # create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(fr"../Output Files/{project_id}/Bardotics Reel.mp4", fourcc, fps, (1080, 1920))

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                # calculate the y-coordinate to place the frame at the center of the canvas
                y = (1920 - height) // 2

                # place the frame onto the canvas
                canvas[y:y+height, :] = frame

                # write the frame
                out.write(canvas)

                # clear the canvas for the next frame
                canvas.fill(0)
            else:
                break

        # release everything
        cap.release()
        out.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(str(e))
        return 401


# In[9]:


def add_audio_to_final_video(project_id):
    """Function to add an audio track to a video file"""
    
    audio_file = f'../Output Files/{project_id}/Audio.mp3'
    video_file = f'../Output Files/{project_id}/Bardotics Reel.mp4'
    
    if os.path.exists(audio_file):
        try:

            # load video
            video = VideoFileClip(video_file)

            # load audio
            audio = AudioFileClip(audio_file)

            # add audio to video
            video_with_audio = video.set_audio(audio)

            # save video with new audio
            video_with_audio.write_videofile(f'../Output Files/{project_id}/Bardotics Reel Final.mp4', codec='libx264')


        except Exception as e:
            print(e)
            pass
    
    return 200


# In[32]:


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'png'}

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def input_file_path_returner(project_id):

    project_input_folder_path = f'../Output Files/{project_id}/Input Files'

    input_file_name = os.listdir(project_input_folder_path)[0]

    input_file_path = os.path.join(project_input_folder_path, input_file_name)

    return input_file_path

def copy_video_to_project_folder(project_id):
    source_path = "C:\\Users\\mnsnn\\Downloads\\fI3Gz5m0yzwgUSJA.mp4"
    destination_folder = f'../Output Files/{project_id}/Input Files'
    
    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)
    
    # Define the destination path
    destination_path = os.path.join(destination_folder, 'fI3Gz5m0yzwgUSJA.mp4')
    
    # Copy the video to the destination folder
    shutil.copy2(source_path, destination_path)

    return 100

# In[10]:


def generate_reel(video_file, text):
    
    try:
        project_id = create_project()

        project_creation_status = create_project_folder(project_id)
    
        w_gen_status = generate_video_w(video_file, project_id)

        img_gen_status = generate_header_image(text, project_id)

        combine_status = combine_img_vid(project_id)

        reel_gen_status = generate_final_video(project_id)
        
        audio_video_status = add_audio_to_final_video(project_id)
        
        return project_id, 200
        
    except Exception as e:
        
        return None, 401
