import os
from datetime import time
from random import random

import httplib2
from googleapiclient import http
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from AuthenticatedService import get_authenticated_service
from Channel import RETRIABLE_EXCEPTIONS, RETRIABLE_STATUS_CODES
from Helper import build_resource, print_response


class Video:
    def __init__(self):
        self.client = get_authenticated_service()

    def resumable_upload(self,request, resource, method):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print ("Uploading file...")
                status, response = request.next_chunk()
                if response is not None:
                    if method == 'insert' and 'id' in response:
                        return response
                    elif method != 'insert' or 'id' not in response:
                        return response
                    else:
                        exit("The upload failed with an unexpected response: %s" % response)
            except HttpError as e:
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                         e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS as e:
                error = "A retriable error occurred: %s" % e

            if error is not None:
                print (error)
                retry += 1
                if retry > 3:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)

    def videos_insert(self, properties, media_file, **kwargs):
        resource = build_resource(properties)  # See full sample for function
        #kwargs = remove_empty_kwargs(**kwargs)  # See full sample for function
        request = self.client.videos().insert(
            body=resource,
            media_body=MediaFileUpload(media_file, chunksize=-1,
                                       resumable=True),
            **kwargs
        )

        # See full sample for function
        return self.resumable_upload(request, 'video', 'insert')

    def UploadVideo(self,videoData):
        media_file = videoData["fileName"]#'sample_video.flv'
        if not os.path.exists(media_file):
            exit('Please specify a valid file location.')

        res=self.videos_insert(
                      {'snippet.categoryId': '22',
                       'snippet.defaultLanguage': '',
                       'snippet.description': videoData["description"],#'Description of uploaded video.',
                       'snippet.tags[]': '',
                       'snippet.title': videoData["title"],#'Test video upload',
                       'status.embeddable': '',
                       'status.license': '',
                       'status.privacyStatus': 'private',#videoData["private"]
                       'status.publicStatsViewable': ''},
                      media_file,
                      part='snippet,status')
        return "{", "AddedVideo:",res['id'], "}"

    def videos_delete(self, **kwargs):
        # See full sample for function
       #kwargs = remove_empty_kwargs(**kwargs)

        response = self.client.videos().delete(
            **kwargs
        ).execute()

        return print_response(response)
