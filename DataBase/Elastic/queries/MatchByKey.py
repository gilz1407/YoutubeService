from DataBases.Elastic.queries.IQuery import IQuery

class MatchByKey(IQuery):
    def __init__(self):
        self.queryName=self.__class__.__name__
        super(MatchByKey,self).__init__()


    def setKeyValue(self,tuple):
        match=self.queryItem["query"]["match"]
        match.update({tuple[0]:tuple[1]})