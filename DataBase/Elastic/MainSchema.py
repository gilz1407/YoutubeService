from marshmallow import Schema, fields, post_load
from DataBases.Elastic.ElasticOp import ElasticOp


class QuerySchema(Schema):
     def __init__(self,data):
         super(QuerySchema, self).__init__()
         self.queryName=data["name"]
         self.index = data["index"]
         self.query = data["query"]
         self.data=data

     queryName = fields.Str()
     index = fields.Str()
     type = fields.Str()
     query=fields.Dict()
     @post_load
     def make_obj(self,data=None):
         op=ElasticOp(self.index)
         op.GeneralQuery(self.query)
         i = __import__('DataBases.Elastic.Entities.'+self.data['type'])
         i = getattr(i,'Elastic')
         module = getattr(i, 'Entities')
         cs = getattr(module, self.data['type'])
         cs = getattr(cs, self.data['type'])
         return cs(**self.data)