from flask import Flask, jsonify, request, send_file
import AIReelGen, TextGen
import os
import configs as cf

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def create_reel():

    try:
        data = request.get_json()  # Get JSON data sent in the POST request
        tweet_link = data.get('url', '')
        text = data.get('text', '')

        if text == None:
            # Generating hookline using AI (Gemini API)
            text, caption = TextGen.generate_text_using_ai(tweet_link)
        else:
            pass

        # Creating project_id
        project_id = AIReelGen.create_project()

        # Creating project
        project_creation_status = AIReelGen.create_project_folder(project_id)

        # Downloading and saving the video to specified directory (This should be changed with download code later)
        video_download_status = AIReelGen.download_twitter_video(tweet_link, project_id)

        # Generating initial video with small banner added to left and right : 14px
        w_gen_status = AIReelGen.generate_video_w(project_id)

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

    except Exception as e:
        print(e)
        # Failure Status
        completion_status = 'Failed'

    return jsonify({'Status': completion_status, 'Caption' : caption, 'Project ID' : project_id})


@app.route('/download', methods=['GET'])
def download_file():
    project_id = request.args.get('project_id')  # get project_id from request args
    if project_id is None:
        return "Error: No project_id field provided. Please specify a project_id."

#     file_path = os.path.join('..', 'Output Files', str(project_id), 'Bardotics Reel Final.mp4')
    file_path = os.path.join(cf.FILE_PATH, cf.output_files, str(project_id), 'Bardotics Reel Final.mp4')
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e)
    

    
if __name__ == '__main__':
    app.run(debug=True)
