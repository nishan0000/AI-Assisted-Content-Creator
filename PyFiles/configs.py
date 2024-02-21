import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE_FILES_PATH = os.path.join(BASE_DIR)#'..','engine', 'files')

FILE_PATH = os.path.abspath(ENGINE_FILES_PATH) + os.sep

output_files = 'Output Files'
input_files = 'input Files'
templates_path = "Hardcodes\\Templates"
fonts_path = 'Hardcodes\\Fonts'
twdl_path = 'twitter-video-dl'
rqdetails_json_path = 'src\\twitter_video_dl\\RequestDetails.json'