from flask_login import current_user, login_required
from sqlalchemy_searchable import search
from flask.views import View
from flask import current_app, request, render_template, redirect, flash, url_for
from covador import split, opt
from covador.flask import query_string

from cowork_site.models import Posting
from .forms import PostingCreateForm


class BaseView(View):

    template_name = None

    def render_template(self, **kwargs):

        return render_template(self.template_name, **kwargs)


class PostingListView(BaseView):
    template_name = 'list.html'
    decorators = [query_string(search_string=opt(str, ''))]

    def get_objects(self, search_string=None):
        s = current_app.session_factory()
        query = s.query(Posting)
        if search_string:
            query = search(query, search_string, sort=True)
        objects = query.all()
        return objects

    def dispatch_request(self, search_string, *args, **kwargs):
        return self.render_template(objects=self.get_objects(search_string, *args, **kwargs), search_string=search_string)


class PostingCreateView(BaseView):

    template_name = 'create.html'
    decorators = [login_required]

    def dispatch_request(self):
        s = current_app.session_factory()

        form = PostingCreateForm()
        if form.validate_on_submit():
            posting = Posting(
                name=form.name.data,
                description=form.description.data,
                cv_url=form.cv_url.data,

            )
            posting.user = current_user
            s.add(posting)
            s.commit()
            flash('Добавлено')
            return redirect(url_for('postings.posting_list'))

        return self.render_template(form=form)


