**ElasticSearch**

A wrapper for management and questioning Elasticsearch queries.

**Getting Started**
 
**Prerequisites**

If you don't have Elasticsearch and Kibana yet:
1. Install "Elasticsearch" server by using the tutorial: https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html
2. Install "Kibana" client (for querying) by using the tutorial https://www.elastic.co/guide/en/kibana/current/windows.html

**Installing**

For using/developing on the elastic wrapper: 
Install "Elasticsearch" package.

Or for more general preparation please install:
    "pip install requirements.txt" 

**Structure**

All of the queries needs to be on "queries.json" file.
The file contains list of queries- "queries":[]
Every query item must contains the following fields:
1. "name" - The name of the query
2. "type" - Type of object as a return value from the query.
3. "query" - Contains the actual query for the ElaticSearch.

Query example:
```json
{
  "queries":[
    {
      "name":"PersonByName",
      "query":{
        "query": {
          "match":
          {
            "name":""
          }
        }
      }
    }
  ]
}
```

After the relevant query was added , suitable class needs to be defined on queries folder.
Structure of the class name {index}_{queryName}:

```python
from DataBases.Elastic.Entities.Person import Person
from DataBases.Elastic.IQuery import IQuery

#Person->index  PersonByName->The name of the query
class Person_PersonByName(IQuery):  

    def __init__(self):
        super().__init__(self.__class__)

    def SetPersonName(self,name):
        self.query["query"]["match"]["name"]=name

    def Query(self):
        res=self.op.GeneralQuery(self.query)
        return Person.Deserialize(res)
```
  Tם your attention: "Query" method must be implemented. 
        
In order to get the query result as object:
1. Every entity needs to implement IEntity and as a result implement 
    ```python
    @classmethod
    def Deserialize(cls,data):
        tempPerson =cls(data["name"])
        return tempPerson
     ``` 
   The method above takes the Json response from the elastic query and creates object from the suitable class "Person"

**Author**
Gil zur




    
    


 









 
