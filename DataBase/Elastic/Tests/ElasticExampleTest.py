from DataBases.Elastic.queries.MatchByKey import MatchByKey

def TestAskForPerson():
    match = MatchByKey()
    match.setKeyValue(("id", "gil"))
    match.Query()


TestAskForPerson()