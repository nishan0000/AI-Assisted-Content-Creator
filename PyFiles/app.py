import streamlit as st
import sys
import os
import tempfile
sys.path.append('PyFiles')
import ReelsGenerator
import time

st.title('Reels Generator')

with st.form(key='my_form'):
    uploaded_file = st.file_uploader("Choose a video file")
    text = st.text_area('Enter your text:')
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if uploaded_file is not None and text:
        # Create a temporary file and save the uploaded file's data to it
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            video_file = tmp.name

        output_status = ReelsGenerator.generate_reel(video_file, text)
        if output_status == 200:
            st.success('Reel generated successfully!')
            # Assuming the output video is named 'output.mp4' and is in the 'OutputFiles' folder
            with open('Output Files/Bardotics Reel Final.mp4', 'rb') as f:
                video_data = f.read()
            st.download_button(
                label="Download Reel",
                data=video_data,
                file_name='Bardotics Reel.mp4',
                mime='video/mp4'
            )
            # Delete the temporary file

        else:
            st.error('Error generating reel.')

        for _ in range(5):  # Retry up to 5 times
            try:
                os.unlink(video_file)
                break
            except PermissionError:
                time.sleep(1)  # Wait for 1 second

    else:
        st.error('Please upload a video file and provide text.')
