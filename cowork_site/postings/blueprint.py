from flask import Blueprint
from .views import (PostingListView, PostingCreateView, PostingArchiveView,
                    PostingThanksView,
                    NeedTeamListView, NeedTeamCreateView,
                    NeedWorkListView, NeedWorkCreateView)

postings_blueprint = Blueprint('postings', __name__)

postings_blueprint.add_url_rule('/list_posting', view_func=PostingListView.as_view('posting_list'), methods=['GET'])
postings_blueprint.add_url_rule('/create', view_func=PostingCreateView.as_view('posting_create'),
                                  methods=['POST', 'GET'])
postings_blueprint.add_url_rule('/archive/<posting_id>', view_func=PostingArchiveView.as_view('posting_archive'),
                                  methods=['GET'])

postings_blueprint.add_url_rule('/list_need_team', view_func=NeedTeamListView.as_view('list_need_team'), methods=['GET'])
postings_blueprint.add_url_rule('/need_team', view_func=NeedTeamCreateView.as_view('need_team'),
                                  methods=['GET', 'POST'])

postings_blueprint.add_url_rule('/list_need_work', view_func=NeedWorkListView.as_view('list_need_work'), methods=['GET'])
postings_blueprint.add_url_rule('/team_needs_work', view_func=NeedWorkCreateView.as_view('team_needs_work'),
                                  methods=['GET', 'POST'])


postings_blueprint.add_url_rule('/thanks', view_func=PostingThanksView.as_view('posting_thanks'),
                                  methods=['GET'])