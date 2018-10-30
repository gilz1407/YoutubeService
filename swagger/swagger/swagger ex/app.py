#!/usr/bin/env python3
import connexion
import logging
import pytest
from gevent import os

from Channel import Channel
from Video import Video
from swagger.swagger.logic import get_authenticated_service, channels_list_by_username

parentFolder=".."
def post_testByFile(TestFile):
    pytest.main([parentFolder+TestFile["fileName"]])

def post_UpdateChannelDetails(UpdateChannelInfo):
    Channel().UpdateChannelSection(UpdateChannelInfo)

def PostInsertVideo(UploadVideo):
    return Video().UploadVideo(UploadVideo),200


def DeleteVideo(VideoToDelete):
    Video().videos_delete(id=VideoToDelete["id"])

def PostUploadComment(Comment):
    Comment().uploadComment(Comment)



logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))


