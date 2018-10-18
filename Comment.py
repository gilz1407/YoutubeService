from AuthenticatedService import get_authenticated_service
from Helper import build_resource, print_response

class Comment:
    def __init__(self):
        self.client = get_authenticated_service()

    def comment_threads_insert(self,client, properties, **kwargs):
        # See full sample for function
        resource = build_resource(properties)

        # See full sample for function
        # kwargs = remove_empty_kwargs(**kwargs)

        response = client.commentThreads().insert(
            body=resource,
            **kwargs
        ).execute()

        return print_response(response)

    def uploadComment(self,content):
        self.comment_threads_insert(self.client,
                               {'snippet.channelId': content['channelId'],
                                'snippet.videoId': content['videoId'],
                                'snippet.topLevelComment.snippet.textOriginal': content['text']},
                               part='snippet')