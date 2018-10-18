import http
import random
from datetime import time


import httplib2
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from AuthenticatedService import get_authenticated_service
from Helper import remove_empty_kwargs, build_resource, print_response

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
                        http.client.IncompleteRead, http.client.ImproperConnectionState,
                        http.client.CannotSendRequest, http.client.CannotSendHeader,
                        http.client.ResponseNotReady, http.client.BadStatusLine)
class Channel:
    def __init__(self):
        self.client = get_authenticated_service()

    def channel_sections_insert(self,client, properties, **kwargs):
        # See full sample for function
        resource = build_resource(properties)

        # See full sample for function
      #  kwargs = remove_empty_kwargs(**kwargs)

        response = client.channelSections().insert(
            body=resource,
            **kwargs
        ).execute()

        return print_response(response)

    def channels_update_branding_settings(self,client, properties, **kwargs):
        # See full sample for function
        resource = build_resource(properties)

        # See full sample for function
        #kwargs = remove_empty_kwargs(**kwargs)

        response = client.channels().update(
            body=resource,
            **kwargs
        ).execute()

        return print_response(response)

    def upload_banner(self, image_file):
        insert_request = self.client.channelBanners().insert(
            media_body=MediaFileUpload(image_file, chunksize=-1, resumable=True)
        )

        image_url = self.resumable_upload(insert_request)
        self.set_banner(image_url)

    def resumable_upload(self,insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print
                "Uploading file..."
                status, response = insert_request.next_chunk()
                if 'url' in response:
                    print ("Banner was successfully uploaded to '%s'." % (response['url']))
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

        return response['url']

    def set_banner(self,banner_url):
        channels_response = self.client.channels().list(
            mine=True,
            part="brandingSettings"
        ).execute()

        if "brandingSettings" not in channels_response["items"][0]:
            channels_response["items"][0]["brandingSettings"]["image"]["bannerExternalUrl"] = []

        channel_brandingSettings = channels_response["items"][0]["brandingSettings"]

        channel_brandingSettings["image"]["bannerExternalUrl"] = banner_url

        channels_update_response = self.client.channels().update(
            part='brandingSettings',
            body=dict(
                brandingSettings=channel_brandingSettings,
                id=channels_response["items"][0]["id"]
            )).execute()

        banner_mobile_url = channels_update_response["brandingSettings"]["image"]["bannerMobileImageUrl"]
        print ("Banner is set to '%s'." % (banner_mobile_url))

    def CreteNewChannelSection(self,data):

        res=self.channel_sections_insert(self.client,
                                {'snippet.type': 'postedVideos',
                                 'snippet.style': 'horizontalRow',
                                 'snippet.title': 'TestAutomationExamples'
                                 #'snippet.position': '',
                                 #'snippet.defaultLanguage': '',
                                 #'contentDetails.playlists[]': '',
                                 #'contentDetails.channels[]': '',
                                 #'targeting.countries[]': '',
                                 #'targeting.languages[]': '',
                                 #'targeting.regions[]': ''
                                  },
                                part='snippet,contentDetails,targeting')
        print_response(res)

    def UpdateChannelSection(self,data):
        self.channels_update_branding_settings(self.client,
                                          {
                                              'id': data["id"],#'UCfflPRy4IEYFKbhHAtbANiA',
                                              'brandingSettings.channel':
                                              {
                                               # "title": "TestAutomation",
                                                "description":data["description"],#"My first channel",
                                                "defaultTab": "Featured",
                                                "showRelatedChannels": True,
                                                "showBrowseView": True,
                                                "profileColor": "#000000",
                                                "defaultLanguage":"en_US"
                                              },
                                              'brandingSettings.image':
                                              {
                                                "bannerImageUrl":"http://storage.googleapis.com/ehimages/2018/3/16/img_377e85ec2c9211d7fe7fb985f2dfb7d9_1521183373492_original.png"
                                              },
                                              'brandingSettings.hints':[{"property": "channel.modules.show_comments.bool", "value": "True"}, {"property": "channel.featured_tab.template.string", "value": "Everything"}]
                                            },
                                          part='brandingSettings')
        self.channels_update_branding_settings(self.client,
                                               {
                                                   'id': data["id"],
                                                   'localizations':{'en': {'title': data["title"], 'description': data["description"]}}
                                               },
                                               part='localizations')
        try:
            self.upload_banner(data["bannerImage"])#"D:/ex.png")
        except HttpError as e:
            print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
        else:
            print   ("The custom banner was successfully uploaded.")
    def GetChannelSection(self):
        self.channel_sections_insert(self.client,
                                {'snippet.type': '',
                                 'snippet.style': '',
                                 'snippet.title': '',
                                 'snippet.position': '',
                                 'snippet.defaultLanguage': '',
                                 'contentDetails.playlists[]': '',
                                 'contentDetails.channels[]': '',
                                 'targeting.countries[]': '',
                                 'targeting.languages[]': '',
                                 'targeting.regions[]': ''},
                                part='snippet,contentDetails,targeting',
                                onBehalfOfContentOwner='')

#Channel().UpdateChannelSection()