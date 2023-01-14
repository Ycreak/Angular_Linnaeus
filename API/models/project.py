from dataclasses import dataclass, asdict
import logging

import config as conf


class ProjectField(object):
    TITLE = "title"
    PROJECT_ID = "project_id"

@dataclass
class Project:
    _id: str = None
    project_id: int = None
    title: str = None

class ProjectModel:
    def __init__(self, server):
        self.db = server[conf.COUCH_PROJECTS]
    
    def __get_projects(self, frag_lst):
        result = list()
        for doc in frag_lst:
            project = Project(_id=doc.id)
            if ProjectField.TITLE in doc:
                project.title = doc[ProjectField.TITLE]
            if ProjectField.PROJECT_ID in doc:
                project.project_id = doc[ProjectField.PROJECT_ID]
            result.append(project)
        return result

    def all(self, sorted=False):
        result = self.db.find({
            "selector": dict(),
            "limit": conf.COUCH_LIMIT
        })
        result = self.__get_projects(result)
        if sorted:
            result.sort(key=lambda Taxon: Taxon.name)
        return result
        
    def filter(self, project, sorted=False):
        project = {key: value for key, value in project.__dict__.items() if value}
        # @deprecated because of refactoring
        # if "_id" in project: 
        #     project[ProjectField.ID] = project.pop("_id")
        # if "name" in project:
        #     project[ProjectField.NAME] = project.pop("name")
        mango = {
            "selector": project,
            "limit": conf.COUCH_LIMIT
        }
        print(mango)
        result = self.db.find(mango)
        result = self.__get_projects(result)
        if sorted:
            result.sort(key=lambda Taxon: Taxon.title)
        return result

    def create(self, project):
        project = {key: value for key, value in project.__dict__.items() if value}
        # @deprecated because of refactoring
        # project[ProjectField.ID] = project.pop("_id") # MongoDB uses "_id" instead of "id"
        # project[ProjectField.NAME] = project.pop("name")
        
        doc_id, _ = self.db.save(project)
        if not doc_id:
            logging.error("create(): failed to create project")
            return None
        return project

    def update(self, project):
        # we update projects via their _id, so no need for get.
        # FIXME: is this correct BORS?
        # project = self.get(project)

        # if project == None:
        #     logging.error("update(): project could not be found")
        #     return False
        try:
            doc = self.db[project._id]
            for key, value in asdict(project).items():
                if value != None:
                    doc[key] = value
            self.db.save(doc)
            return True
        except Exception as e:
            logging.error(e)
        return False

    def delete(self, project):
        project = self.get(project)
    
        if project == None:
            logging.error("delete(): project could not be found")
            return False
        try:
            doc = self.db[project._id]
            self.db.delete(doc)
            return True
        except Exception as e:
            logging.error(e)
        return False

    def get(self, project):
        project = {key: value for key, value in project.__dict__.items() if value}
        mango = {
            "selector": project,
            "limit": conf.COUCH_LIMIT
        }
        result = self.db.find(mango)
        result = self.__get_projects(result)

        if result:
            if len(result) > 1:
                logging.warning("get(): function returned more than 1 object!")
            return result[0]
        return None


