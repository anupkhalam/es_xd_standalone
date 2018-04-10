import sys
import tika
from tika import parser
tika.initVM()
import glob

def doc2html(files_location):
    file_list = glob.glob(files_location + '/*.docx') + glob.glob(files_location + '/*.doc')
    for file in file_list:
        html_file = files_location + '/' + file.split("/")[-1].split('.')[0] + '.html'
        with open(html_file, 'w') as f:
            parsed = parser.from_file(file, xmlContent=True)
            f.write(parsed['content'])

