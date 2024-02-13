from flask import Flask, jsonify, request
import AIReelGen

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def create_reel():

    try:
        data = request.get_json()  # Get JSON data sent in the POST request
        text = data.get('text', '')  # Get the 'text' field from the JSON data

        # Creating project_id
        project_id = AIReelGen.create_project()

        # Creating project
        project_creation_status = AIReelGen.create_project_folder(project_id)

        # Downloading and saving the video to specified directory (This should be changed with download code later)
        video_download_status = AIReelGen.copy_video_to_project_folder(project_id)

        # Returning the path to mp4 file
        input_video_path = AIReelGen.input_file_path_returner(project_id)

        # Generating initial video with small banner added to left and right : 14px
        w_gen_status = AIReelGen.generate_video_w(input_video_path, project_id)

        # Generating the image with text added
        img_gen_status = AIReelGen.generate_header_image(text, project_id)

        # Combining the image and video together
        combine_status = AIReelGen.combine_img_vid(project_id)

        # Generating Reel
        reel_gen_status = AIReelGen.generate_final_video(project_id)

        # Adding audio to the created video
        audio_video_status = AIReelGen.add_audio_to_final_video(project_id)

        # Success status
        completion_status = 'Completed'

    except:
        # Failure Status
        completion_status = 'Failed'

    return jsonify({'Status': completion_status})

if __name__ == '__main__':
    app.run(debug=True)
