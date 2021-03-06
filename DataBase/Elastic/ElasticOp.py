from Configuration.cm import Cm
from elasticsearch import Elasticsearch

class ElasticOp():
    def __init__(self, index=None,doc_type=None):
         self.conf = Cm().config['ElasticSearch']
         self.es = Elasticsearch([{'host': self.conf['host'], 'port': self.conf['port']}])
         self.index = index
         self.doc_type=doc_type

    def GeneralQuery(self, query):
         return self.es.search(index=self.index,doc_type=self.doc_type, body=query)

    def InsertDoc(self,doc_type,body):
        self.es.index(index=self.index,doc_type=doc_type,body=body)

    def UpdateDoc(self,doc_type,body):
        self.es.update_by_query(index=self.index,doc_type=doc_type,body=body)







