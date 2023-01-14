from dataclasses import dataclass, asdict
import logging

import config as conf


class TaxonField(object):
    TAXON_ID = "taxon_id"
    PROJECT = "project"
    NAME = "name"
    PARENT = "parent"
    RANK = "rank"
    ORDER = "order"
    COMMON_NAME = "common_name"

@dataclass
class Taxon:
    _id: str = None
    taxon_id: str = None
    name: str = None
    parent: int = None
    rank: int = None
    order: int = None
    project: int = None
    common_name: str = None

class TaxonModel:
    def __init__(self, server):
        self.db = server[conf.COUCH_TAXA]
    
    def __get_taxa(self, frag_lst):
        result = list()
        for doc in frag_lst:
            taxon = Taxon(_id=doc.id)
            if TaxonField.NAME in doc:
                taxon.name = doc[TaxonField.NAME]
            if TaxonField.PARENT in doc:
                taxon.parent = doc[TaxonField.PARENT]
            if TaxonField.RANK in doc:
                taxon.rank = doc[TaxonField.RANK]
            if TaxonField.ORDER in doc:
                taxon.order = doc[TaxonField.ORDER]
            if TaxonField.PROJECT in doc:
                taxon.project = doc[TaxonField.PROJECT]
            result.append(taxon)
        return result

    def all(self, sorted=False):
        result = self.db.find({
            "selector": dict(),
            "limit": conf.COUCH_LIMIT
        })
        result = self.__get_taxa(result)
        if sorted:
            result.sort(key=lambda Taxon: Taxon.name)
        return result
        
    def filter(self, taxon, sorted=False):
        taxon = {key: value for key, value in taxon.__dict__.items() if value}
        # @deprecated because of refactoring
        # if "_id" in taxon: 
        #     taxon[TaxonField.ID] = taxon.pop("_id")
        # if "name" in taxon:
        #     taxon[TaxonField.NAME] = taxon.pop("name")
        mango = {
            "selector": taxon,
            "limit": conf.COUCH_LIMIT
        }
        print(mango)
        result = self.db.find(mango)
        result = self.__get_taxa(result)
        if sorted:
            result.sort(key=lambda Taxon: Taxon.title)
        return result

    def create(self, taxon):
        taxon = {key: value for key, value in taxon.__dict__.items() if value}
        # @deprecated because of refactoring
        # taxon[TaxonField.ID] = taxon.pop("_id") # MongoDB uses "_id" instead of "id"
        # taxon[TaxonField.NAME] = taxon.pop("name")
        
        doc_id, _ = self.db.save(taxon)
        if not doc_id:
            logging.error("create(): failed to create taxon")
            return None
        return taxon

    def update(self, taxon):
        # we update taxons via their _id, so no need for get.
        # FIXME: is this correct BORS?
        # taxon = self.get(taxon)

        # if taxon == None:
        #     logging.error("update(): taxon could not be found")
        #     return False
        try:
            doc = self.db[taxon._id]
            for key, value in asdict(taxon).items():
                if value != None:
                    doc[key] = value
            self.db.save(doc)
            return True
        except Exception as e:
            logging.error(e)
        return False

    def delete(self, taxon):
        taxon = self.get(taxon)
    
        if taxon == None:
            logging.error("delete(): taxon could not be found")
            return False
        try:
            doc = self.db[taxon._id]
            self.db.delete(doc)
            return True
        except Exception as e:
            logging.error(e)
        return False

    def get(self, taxon):
        taxon = {key: value for key, value in taxon.__dict__.items() if value}
        mango = {
            "selector": taxon,
            "limit": conf.COUCH_LIMIT
        }
        result = self.db.find(mango)
        result = self.__get_taxa(result)

        if result:
            if len(result) > 1:
                logging.warning("get(): function returned more than 1 object!")
            return result[0]
        return None


