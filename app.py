# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 11:56:49 2022

@author: Admin
"""
from flask import Flask, request, Response
import re

app = Flask(__name__)
import os

@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response


def get_chunk(fileName, byte1=None, byte2=None):
    full_path = "F:\\Backup\\TA\\Model\\{}.mp4".format(fileName)
    # full_path = "C:\\Users\\Mujir\\Downloads\\Shopping, People, Commerce, Mall, Many, Crowd, Walking   Free Stock video footage   YouTube.mp4"
    # full_path = "C:\\Users\\Mujir\\Downloads\\The CCTV People Demo 2.mp4"
    # full_path = "C:\\Users\\Mujir\\Downloads\\Street scene at night with walking people CCTV style  night view.mp4"
    file_size = os.stat(full_path).st_size
    start = 0
    
    if byte1 < file_size:
        start = byte1
    if byte2:
        length = byte2 + 1 - byte1
    else:
        length = file_size - start

    with open(full_path, 'rb') as f:
        f.seek(start)
        chunk = f.read(length)
    return chunk, start, length, file_size


@app.route('/video/<cameraId>')
def get_file(cameraId):
    # print("CameraId: ", cameraId)
    range_header = request.headers.get('Range', None)
    byte1, byte2 = 0, None
    if range_header:
        match = re.search(r'(\d+)-(\d*)', range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])
       
    chunk, start, length, file_size = get_chunk(cameraId, byte1, byte2)
    resp = Response(chunk, 206, mimetype='video/mp4',
                      content_type='video/mp4', direct_passthrough=True)
    resp.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
    return resp

if __name__ == "__main__":
    app.run(host='192.168.43.194', port=5001, debug=True, threaded=True)