from flask import Blueprint
from .views import CandidateListView

""", CandidateDetailView, CandidateCreateView,
                    CandidateUpdateView, CandidateDeleteView, CandidateCancelView,
                    CandidateLogsCreateView, CandidateLogsView, CandidateResultView)
"""

candidates_blueprint = Blueprint('candidates', __name__)

candidates_blueprint.add_url_rule('/', view_func=CandidateListView.as_view('candidates_list'), methods=['GET'])
