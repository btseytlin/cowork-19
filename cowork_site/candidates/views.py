from flask.views import View
from flask import current_app, request, render_template, redirect, flash, url_for

from cowork_site.models import Candidate
from .forms import CandidateCreateForm


class BaseView(View):

    template_name = None

    def render_template(self, **kwargs):

        return render_template(self.template_name, **kwargs)


class CandidateListView(BaseView):

    template_name = 'list.html'

    def get_objects(self):
        s = current_app.session_factory()
        objects = s.query(Candidate).all()
        return objects

    def dispatch_request(self):
        return self.render_template(objects=self.get_objects())


class CandidateCreateView(BaseView):

    template_name = 'create.html'

    def dispatch_request(self):
        s = current_app.session_factory()

        form = CandidateCreateForm()
        if form.validate_on_submit():
            candidate = Candidate(
                name=form.name.data,
                email=form.email.data,
                description=form.description.data,
                cv_url=form.cv_url.data,
            )
            s.add(candidate)
            s.commit()
            flash('Добавлено')
            return redirect(url_for('candidates.candidate_list'))

        return self.render_template(form=form)


