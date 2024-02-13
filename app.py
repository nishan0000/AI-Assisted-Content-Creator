from flask import Flask, jsonify
import AIReelGen

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def create_reel():

    # Creating project_id
    project_id = AIReelGen.create_project()
    # Creating project
    project_creation_status = AIReelGen.create_project_folder(project_id)

    return jsonify({'project_id': project_id})

if __name__ == '__main__':
    app.run(debug=True)
