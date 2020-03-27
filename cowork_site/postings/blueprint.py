from flask import Blueprint
from .views import PostingListView, PostingCreateView, PostingArchiveView


postings_blueprint = Blueprint('postings', __name__)

postings_blueprint.add_url_rule('/', view_func=PostingListView.as_view('posting_list'), methods=['GET'])
postings_blueprint.add_url_rule('/create', view_func=PostingCreateView.as_view('posting_create'),
                                  methods=['POST', 'GET'])
postings_blueprint.add_url_rule('/archive/<posting_id>', view_func=PostingArchiveView.as_view('posting_archive'),
                                  methods=['GET'])