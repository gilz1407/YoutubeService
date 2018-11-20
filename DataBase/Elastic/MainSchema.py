from marshmallow import Schema, fields, post_load

from DataBase.Elastic.ElasticOp import ElasticOp


class QuerySchema(Schema):
     def __init__(self,data):
         super(QuerySchema, self).__init__()
         self.queryName=data["name"]
         self.index = data["index"]
         self.doc_type = data["doc_type"]
         self.query = data["query"]
         self.data=data

     queryName = fields.Str()
     index = fields.Str()
     doc_type = fields.Str()
     type = fields.Str()
     query=fields.Dict()
     @post_load
     def make_obj(self,data=None):
         op=ElasticOp(self.index,self.doc_type)
         res=op.GeneralQuery(self.query)
         i = __import__('DataBase.Elastic.Entities.'+self.data['type'])
         i = getattr(i,'Elastic')
         module = getattr(i, 'Entities')
         cs = getattr(module, self.data['type'])
         cs = getattr(cs, self.data['type'])
         return cs(self.data)