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
        
        # Running the function
        caption, completion_status, project_id = AIReelGen.create_reel(tweet_link, text)
        
        # What to return
        rets = jsonify({'Status': completion_status, 'Caption' : caption, 'Project ID' : project_id})
        
        return rets

    except Exception as e:
        
        # What to return
        rets = jsonify({'Status': completion_status, 'Project ID' : project_id})

        return rets


@app.route('/download', methods=['GET'])
def download_file():
    project_id = request.args.get('project_id')  # get project_id from request args
    if project_id is None:
        return "Error: No project_id field provided. Please specify a project_id."

    file_path = os.path.join(cf.FILE_PATH, cf.output_files, str(project_id), 'Bardotics Reel Final.mp4')
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e)
    

    
if __name__ == '__main__':
    app.run(debug=True)
