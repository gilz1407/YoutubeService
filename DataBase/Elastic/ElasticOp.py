from Configuration.cm import Cm
from elasticsearch import Elasticsearch

class ElasticOp():
    def __init__(self, index=None):
         self.conf = Cm().config['ElasticSearch']
         self.es = Elasticsearch([{'host': self.conf['host'], 'port': self.conf['port']}])
         self.index = index

    def GeneralQuery(self, query):
         return self.es.search(index=self.index, body=query)

    def CreateIndex(self,indexName,number_of_shards=1,number_of_replicas=0):
        if not self.es.indices.exists(index=indexName):
            request_body = {
                "settings": {
                    "number_of_shards": number_of_shards,
                    "number_of_replicas": number_of_replicas
                }
            }
            self.es.create(index=indexName,body=request_body)

    def InsertDoc(self,doc_type,body):
        self.es.index(index=self.index,doc_type=doc_type,body=body)







