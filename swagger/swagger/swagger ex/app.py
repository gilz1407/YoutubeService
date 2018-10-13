#!/usr/bin/env python3
import connexion
import logging
import pytest
from gevent import os

from swagger.swagger.logic import get_authenticated_service, channels_list_by_username

parentFolder=".."
def post_testByFile(TestFile):
    pytest.main([parentFolder+TestFile["fileName"]])

def get_channelDetailes(details):
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    channels_list_by_username(service,
                              part='snippet,contentDetails,statistics',
                              forUsername='gilz1407')


def post_testByMarks(Marker):
    pytest.main([parentFolder+Marker["fileName"],'-v','-m',Marker["marker"]])

def post_testByName(TestName):
    pytest.main([parentFolder+TestName["fileName"],'-k',TestName["testName"]])

def post_testByFolder(FolderName):
    _folderName=parentFolder+FolderName["folderName"]
    for path in absoluteFilePaths(_folderName):
        before,after = path.split(FolderName["folderName"].replace("/",""))
        parsedAfter = after.replace("\\", "/")
        fileName=parsedAfter.split("/")[-1]
        if (fileName.startswith("Test")):
            pytest.main(_folderName+parsedAfter)

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


