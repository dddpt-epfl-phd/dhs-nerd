import json



class Polity:
    def __init__(self, polity_id, toponym, typology=None, geoidentifer=None, hds_tag=None, hds_article_id=None):
        self.polity_id =polity_id
        self._typology = typology
        self.toponym = toponym
        self._geoidentifer = geoidentifer
        self.hds_tag = hds_tag
        self.hds_article_id = hds_article_id


    @property
    def typology(self):
        return self._typology if self._typology is not None else ""

    @property
    def geoidentifer(self):
        return self._geoidentifer if self._geoidentifer is not None else ""

    @property
    def canonic_title(self):
        typ = self._typology+" de " if self._typology is not None else ""
        return typ+self.toponym + (" ("+self.geoidentifier+")" if self.geoidentifier is not None else "")

    def __str__(self):
        return "Polity("+self.polity_id+", "+self.canonic_title+", )"
    def __repr__(self):
        return self.__str__()
    
    def to_json(self, as_dict=False, *args, **kwargs):
        def remove_first_(string):
            return string if string[0]!="_" else string[1:]
        result = {
            remove_first_(k): v
            for k,v in self.__dict__.items()
            if v is not None
        }
        if self.hds_tag is not None:
            result["hds_tag"] = self.hds_tag.tag
        if as_dict:
            return result
        else:
            return json.dumps(result)