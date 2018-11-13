#!/usr/bin/env python3
import connexion
import logging
import pytest
from gevent import os
from redis import Redis

from AuthenticatedService import get_authenticated_service
from Channel import Channel
from Configuration.cm import Cm
from Video import Video

parentFolder=".."
def post_testByFile(TestFile):
    pytest.main([parentFolder+TestFile["fileName"]])

def post_UpdateChannelDetails(UpdateChannelInfo):
    Channel().UpdateChannelSection(UpdateChannelInfo)

def PostInsertVideo(UploadVideo):
    print(os.path.dirname(os.path.abspath(__file__)))
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
    get_authenticated_service()
    config=Cm().config['SwagerConnection']
    app.run(port=int(config['port']), server='gevent')

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))




