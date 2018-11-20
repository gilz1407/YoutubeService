class Video:
    def __init__(self,data):
        self.queryName = data['name']
        self.index = data['index']
        self.type = data['type']
        self.query = data['query']