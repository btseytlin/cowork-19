from flask import Blueprint
from .views import CandidateListView, CandidateCreateView


candidates_blueprint = Blueprint('candidates', __name__)

candidates_blueprint.add_url_rule('/', view_func=CandidateListView.as_view('candidate_list'), methods=['GET'])
candidates_blueprint.add_url_rule('/create', view_func=CandidateCreateView.as_view('candidate_create'),
                                  methods=['POST', 'GET'])
