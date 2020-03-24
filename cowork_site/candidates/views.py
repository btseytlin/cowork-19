from flask.views import View
from flask import render_template
from flask import current_app

from cowork_site.models import Candidate


class CandidateListView(View):

    template_name = 'list.html'

    def render_template(self, context):
        return render_template(self.template_name, **context)

    def get_objects(self):
        s = current_app.session_factory()
        objects = s.query(Candidate).all()
        return objects

    def dispatch_request(self):
        context = {'objects': self.get_objects()}
        return self.render_template(context)
