from flask import Blueprint
from .views import (PostingListView, PostingCreateView, PostingArchiveView,
                    PostingThanksView, NeedTeamPostingCreateView,
                    NeedWorkPostingCreateView)

postings_blueprint = Blueprint('postings', __name__)

postings_blueprint.add_url_rule('/', view_func=PostingListView.as_view('posting_list'), methods=['GET'])
postings_blueprint.add_url_rule('/create', view_func=PostingCreateView.as_view('posting_create'),
                                  methods=['POST', 'GET'])
postings_blueprint.add_url_rule('/archive/<posting_id>', view_func=PostingArchiveView.as_view('posting_archive'),
                                  methods=['GET'])

postings_blueprint.add_url_rule('/need_team', view_func=NeedTeamPostingCreateView.as_view('need_team'),
                                  methods=['GET', 'POST'])
postings_blueprint.add_url_rule('/team_needs_work', view_func=NeedWorkPostingCreateView.as_view('team_needs_work'),
                                  methods=['GET', 'POST'])
postings_blueprint.add_url_rule('/thanks', view_func=PostingThanksView.as_view('posting_thanks'),
                                  methods=['GET'])