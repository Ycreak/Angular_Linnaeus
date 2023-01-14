from flask import request, make_response
import logging
from flask_jsonpify import jsonify
from uuid import uuid4

from couch import CouchAuthenticator
# from models.fragment import Fragment, FragmentModel, TaxonField
from models.taxon import Taxon, TaxonModel, TaxonField


# fragments = FragmentModel(CouchAuthenticator().couch)
taxa = TaxonModel(CouchAuthenticator().couch)

def get_author():
    author = None
    title = None
    editor = None
    name = None
    try:
        if TaxonField.AUTHOR in request.get_json():
            author = request.get_json()[TaxonField.AUTHOR]
        if TaxonField.TITLE in request.get_json():
            title = request.get_json()[TaxonField.TITLE]
        if TaxonField.EDITOR in request.get_json():
            editor = request.get_json()[TaxonField.EDITOR]
        if TaxonField.NAME in request.get_json():
            name = request.get_json()[TaxonField.NAME]
    except KeyError as e:
        logging.error(e)
        return make_response("Unprocessable entity", 422)
    fragment_lst = fragments.filter(Fragment(author=author, title=title, editor=editor, name=name), sorted=True)
    if not fragment_lst:
        return make_response("Not found", 401)
    return jsonify(sorted(set([frag.author for frag in fragment_lst]))), 200

def get_title():
    author = None
    title = None
    editor = None
    name = None
    try:
        if TaxonField.AUTHOR in request.get_json():
            author = request.get_json()[TaxonField.AUTHOR]
        if TaxonField.TITLE in request.get_json():
            title = request.get_json()[TaxonField.TITLE]
        if TaxonField.EDITOR in request.get_json():
            editor = request.get_json()[TaxonField.EDITOR]
        if TaxonField.NAME in request.get_json():
            name = request.get_json()[TaxonField.NAME]
    except KeyError as e:
        logging.error(e)
        return make_response("Unprocessable entity", 422)
    fragment_lst = fragments.filter(Fragment(author=author, title=title, editor=editor, name=name), sorted=True)
    if not fragment_lst:
        return make_response("Not found", 401)
    return jsonify(sorted(set([frag.title for frag in fragment_lst]))), 200

def get_editor():
    author = None
    title = None
    editor = None
    name = None
    try:
        if TaxonField.AUTHOR in request.get_json():
            author = request.get_json()[TaxonField.AUTHOR]
        if TaxonField.TITLE in request.get_json():
            title = request.get_json()[TaxonField.TITLE]
        if TaxonField.EDITOR in request.get_json():
            editor = request.get_json()[TaxonField.EDITOR]
        if TaxonField.NAME in request.get_json():
            name = request.get_json()[TaxonField.NAME]
    except KeyError as e:
        logging.error(e)
        return make_response("Unprocessable entity", 422)
    fragment_lst = fragments.filter(Fragment(author=author, title=title, editor=editor, name=name), sorted=True)
    if not fragment_lst:
        return make_response("Not found", 401)
    return jsonify(sorted(set([frag.editor for frag in fragment_lst]))), 200

def get_name():
    author = None
    title = None
    editor = None
    name = None
    try:
        if TaxonField.AUTHOR in request.get_json():
            author = request.get_json()[TaxonField.AUTHOR]
        if TaxonField.TITLE in request.get_json():
            title = request.get_json()[TaxonField.TITLE]
        if TaxonField.EDITOR in request.get_json():
            editor = request.get_json()[TaxonField.EDITOR]
        if TaxonField.NAME in request.get_json():
            name = request.get_json()[TaxonField.NAME]
    except KeyError as e:
        logging.error(e)
        return make_response("Unprocessable entity", 422)
    fragment_lst = fragments.filter(Fragment(author=author, title=title, editor=editor, name=name), sorted=True)
    if not fragment_lst:
        return make_response("Not found", 401)
    return jsonify(list(set([frag.name for frag in fragment_lst]))), 200

def get_taxon():
    name = None
    taxon_id = None
    parent = None
    rank = None
    order = None

    try:
        if TaxonField.NAME in request.get_json():
            name = request.get_json()[TaxonField.NAME]
        if TaxonField.TAXON_ID in request.get_json():
            taxon_id = request.get_json()[TaxonField.TAXON_ID]
        if TaxonField.PARENT in request.get_json():
            parent = request.get_json()[TaxonField.PARENT_ID]

    except KeyError as e:
        logging.error(e)
        return make_response("Unprocessable entity", 422)

    taxon_lst = taxa.filter(Taxon(name=name, taxon_id=taxon_id, parent=parent), sorted=True)
    if not taxon_lst:
        return make_response("Not found", 401)
    return jsonify(taxon_lst), 200

def create_taxon():    
    print('json:', request.get_json())
    
    try:
        taxon_id = request.get_json()[TaxonField.TAXON_ID]
        project = request.get_json()[TaxonField.PROJECT]
        name = request.get_json()[TaxonField.NAME]
        parent = request.get_json()[TaxonField.PARENT]
        rank = request.get_json()[TaxonField.RANK]
        order = request.get_json()[TaxonField.ORDER]

        if TaxonField.COMMON_NAME in request.get_json():
            common_name = request.get_json()[TaxonField.COMMON_NAME]

    except KeyError as e:
        logging.error(e)
        return make_response("Unprocessable entity", 422)
    
    if taxa.filter(
        Taxon(
            taxon_id=taxon_id,
            name=name
        )):
        logging.error("create_taxon(): duplicate taxon")
        return make_response("Forbidden", 403)

    taxon = taxa.create(Taxon(
        _id=uuid4().hex, 
        taxon_id=taxon_id,
        project=project,
        name=name,
        parent=parent,
        rank=rank,
        order=order,
        common_name=common_name,
        ))
    if taxon == None:
        return make_response("Server error", 500)
    
    return make_response("Created", 200)

def link_fragment():
    try:
        author = request.get_json()[TaxonField.AUTHOR]
        title = request.get_json()[TaxonField.TITLE]
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
        _id = request.get_json()[TaxonField.ID]
        author = request.get_json()[TaxonField.AUTHOR]
        title = request.get_json()[TaxonField.TITLE]
        editor = request.get_json()[TaxonField.EDITOR]
        name = request.get_json()[TaxonField.NAME]

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

        if TaxonField.STATUS in request.get_json():
            status = request.get_json()[TaxonField.STATUS]
        if TaxonField.LOCK in request.get_json():
            lock = request.get_json()[TaxonField.LOCK]
        if TaxonField.TRANSLATION in request.get_json():
            translation = request.get_json()[TaxonField.TRANSLATION]
        if TaxonField.DIFFERENCES in request.get_json():
            differences = request.get_json()[TaxonField.DIFFERENCES]
        if TaxonField.APPARATUS in request.get_json():
            apparatus = request.get_json()[TaxonField.APPARATUS]
        if TaxonField.COMMENTARY in request.get_json():
            commentary = request.get_json()[TaxonField.COMMENTARY]
        if TaxonField.RECONSTRUCTION in request.get_json():
            reconstruction = request.get_json()[TaxonField.RECONSTRUCTION]
        if TaxonField.CONTEXT in request.get_json():
            context = request.get_json()[TaxonField.CONTEXT]
        if TaxonField.LINES in request.get_json():
            lines = request.get_json()[TaxonField.LINES]
        if TaxonField.LINKED_FRAGMENTS in request.get_json():
            linked_fragments = request.get_json()[TaxonField.LINKED_FRAGMENTS]
    
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
        author = request.get_json()[TaxonField.AUTHOR]
        title = request.get_json()[TaxonField.TITLE]
        editor = request.get_json()[TaxonField.EDITOR]
        name = request.get_json()[TaxonField.NAME]
    except KeyError as e:
        logging.error(e)
        return make_response("Unprocessable entity", 422)
    fragment = fragments.delete(Fragment(author=author, title=title, editor=editor, name=name))

    if fragment:
        return make_response("OK", 200)
    else:
        return make_response("Not found", 401)
