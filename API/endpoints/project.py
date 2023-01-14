from flask import request, make_response
import logging
from flask_jsonpify import jsonify
from uuid import uuid4

from couch import CouchAuthenticator
# from models.fragment import Fragment, FragmentModel, ProjectField
from models.project import Project, ProjectModel, ProjectField


# fragments = FragmentModel(CouchAuthenticator().couch)
projects = ProjectModel(CouchAuthenticator().couch)

def get_project():
    title = None
    project_id = None

    try:
        if ProjectField.TITLE in request.get_json():
            title = request.get_json()[ProjectField.TITLE]
        if ProjectField.PROJECT_ID in request.get_json():
            project_id = request.get_json()[ProjectField.PROJECT_ID]

    except KeyError as e:
        logging.error(e)
        return make_response("Unprocessable entity", 422)

    project_lst = projects.filter(Project(title=title, project_id=project_id), sorted=True)
    if not project_lst:
        return make_response("Not found", 401)
    return jsonify(project_lst), 200

def create_project():    
    
    try:
        title = request.get_json()[ProjectField.TITLE]
        project_id = request.get_json()[ProjectField.PROJECT_ID]

    except KeyError as e:
        logging.error(e)
        return make_response("Unprocessable entity", 422)
    
    if projects.filter(
        Project(
            title=title,
            project_id=project_id
        )):
        logging.error("create_project(): duplicate project")
        return make_response("Forbidden", 403)

    project = projects.create(Project(
        _id=uuid4().hex, 
        title = title,
        project_id = project_id,
        ))
    if project == None:
        return make_response("Server error", 500)
    
    return make_response("Created", 200)

def link_fragment():
    try:
        author = request.get_json()[ProjectField.AUTHOR]
        title = request.get_json()[ProjectField.TITLE]
    except KeyError as e:
        logging.error(e)
        return make_response("Unprocessable entity", 422)
    
    fragment_lst = fragments.filter(Fragment(author=author, title=title))
    if not fragment_lst:
        return make_response("Not found", 401)

    while(fragment_lst):
        fragment = fragment_lst.pop()
        for line in fragment.lines:
            for other in fragment_lst:
                for other_line in other:
                    return "hello", 200

def update_fragment():    
    try:
        _id = request.get_json()[ProjectField.ID]
        author = request.get_json()[ProjectField.AUTHOR]
        title = request.get_json()[ProjectField.TITLE]
        editor = request.get_json()[ProjectField.EDITOR]
        name = request.get_json()[ProjectField.NAME]

        status = None
        lock = None
        translation = None
        differences = None
        apparatus = None
        commentary = None
        reconstruction = None
        context = None
        lines = None
        linked_fragments = None

        if ProjectField.STATUS in request.get_json():
            status = request.get_json()[ProjectField.STATUS]
        if ProjectField.LOCK in request.get_json():
            lock = request.get_json()[ProjectField.LOCK]
        if ProjectField.TRANSLATION in request.get_json():
            translation = request.get_json()[ProjectField.TRANSLATION]
        if ProjectField.DIFFERENCES in request.get_json():
            differences = request.get_json()[ProjectField.DIFFERENCES]
        if ProjectField.APPARATUS in request.get_json():
            apparatus = request.get_json()[ProjectField.APPARATUS]
        if ProjectField.COMMENTARY in request.get_json():
            commentary = request.get_json()[ProjectField.COMMENTARY]
        if ProjectField.RECONSTRUCTION in request.get_json():
            reconstruction = request.get_json()[ProjectField.RECONSTRUCTION]
        if ProjectField.CONTEXT in request.get_json():
            context = request.get_json()[ProjectField.CONTEXT]
        if ProjectField.LINES in request.get_json():
            lines = request.get_json()[ProjectField.LINES]
        if ProjectField.LINKED_FRAGMENTS in request.get_json():
            linked_fragments = request.get_json()[ProjectField.LINKED_FRAGMENTS]
    
    except KeyError as e:
        logging.error(e)
        return make_response("Unprocessable entity", 422)

    # FIXME: Given the id, we must make sure the fragment exists.
    # if not fragments.filter(Fragment(author=author, title=title, editor=editor, name=name)):
    #     logging.error("revise_fragment(): fragment does not exist")
    #     return make_response("Forbidden", 403)

    fragment = fragments.update(Fragment(_id=_id, author=author, title=title, editor=editor, name=name, status=status,
                                         lock=lock, translation=translation, differences=differences, apparatus=apparatus, 
                                         commentary=commentary, reconstruction=reconstruction, context=context, lines=lines, 
                                         linked_fragments=linked_fragments))
    if fragment == None:
        return make_response("Server error", 500)

    return make_response("Revised", 200)

def delete_fragment():
    try:
        author = request.get_json()[ProjectField.AUTHOR]
        title = request.get_json()[ProjectField.TITLE]
        editor = request.get_json()[ProjectField.EDITOR]
        name = request.get_json()[ProjectField.NAME]
    except KeyError as e:
        logging.error(e)
        return make_response("Unprocessable entity", 422)
    fragment = fragments.delete(Fragment(author=author, title=title, editor=editor, name=name))

    if fragment:
        return make_response("OK", 200)
    else:
        return make_response("Not found", 401)
