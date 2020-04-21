from flask_login import current_user, login_required
from sqlalchemy_searchable import search
from flask.views import View
from flask import (current_app, request, render_template, redirect, flash,
                   url_for,
                   abort)
from covador import split, opt
from covador.flask import query_string

from cowork_site.cache import cache
from cowork_site.models import Posting, NeedTeamPosting, NeedWorkPosting
from cowork_site.utils import back_redirect_url
from cowork_site import config
from .forms import PostingCreateForm, TeamPostingCreateForm


@cache.memoize(300)
def query_postings(search_string):
    s = current_app.session_factory()
    query = s.query(Posting).filter_by(display=True)
    if search_string:
        query = search(query, search_string, sort=True)
    query = query.order_by(Posting.created_at.desc())
    objects = query.all()
    return objects


@cache.memoize(300)
def query_need_team_postings(search_string):
    s = current_app.session_factory()
    query = s.query(NeedTeamPosting).filter_by(display=True)
    if search_string:
        query = search(query, search_string, sort=True)
    query = query.order_by(NeedTeamPosting.created_at.desc())
    objects = query.all()
    return objects


@cache.memoize(300)
def query_need_work_postings(search_string):
    s = current_app.session_factory()
    query = s.query(NeedWorkPosting).filter_by(display=True)
    if search_string:
        query = search(query, search_string, sort=True)
    query = query.order_by(NeedWorkPosting.created_at.desc())
    objects = query.all()
    return objects


class BaseView(View):
    template_name = None
    def render_template(self, **kwargs):
        return render_template(self.template_name, **kwargs)


class BasePostingListView(BaseView):
    template_name = None
    decorators = [query_string(search_string=opt(str, '')),
                  query_string(page=opt(int, 1))]

    def query_objects(self, search_string):
        return None

    def get_objects(self, search_string=None, page=None):
        per_page = config.Configuration.POSTINGS_PER_PAGE
        objects = self.query_objects(search_string)
        total = len(objects)

        objects = objects[(page - 1) * per_page:page * per_page]
        is_last_page = ((page - 1) * per_page + per_page) >= total
        return objects, is_last_page

    def dispatch_request(self, search_string, page):
        objects, is_last_page = self.get_objects(search_string, page)
        return self.render_template(objects=objects,
                                    is_last_page=is_last_page,
                                    search_string=search_string,
                                    page=page)


class PostingListView(BasePostingListView):
    template_name = 'list.html'

    def query_objects(self, search_string):
        return query_postings(search_string)


class NeedTeamListView(BasePostingListView):
    template_name = 'list.html'

    def query_objects(self, search_string):
        return query_need_team_postings(search_string)


class NeedWorkListView(BasePostingListView):
    template_name = 'list.html'

    def query_objects(self, search_string):
        return query_need_work_postings(search_string)


class PostingCreateView(BaseView):

    template_name = 'create.html'
    decorators = [login_required]

    def dispatch_request(self):
        s = current_app.session_factory()

        previous_post = s.query(Posting).filter(Posting.user==current_user, Posting.display==True).one_or_none()

        form = PostingCreateForm()
        if form.validate_on_submit():
            posting = Posting(
                name=form.name.data.strip(),
                oneliner=form.oneliner.data.strip(),
                description=form.description.data.strip(),
                cv_url=form.cv_url.data.strip(),
            )
            posting.user = current_user

            if previous_post:
                previous_post.display = False
                s.add(previous_post)
            s.add(posting)
            s.commit()
            cache.delete_memoized(query_postings)
            flash('Добавлено')
            return redirect(url_for('postings.posting_list'))

        return self.render_template(form=form, previous_post=previous_post)


class PostingArchiveView(BaseView):
    decorators = [login_required]

    def dispatch_request(self, posting_id):
        s = current_app.session_factory()

        if not posting_id:
            abort(400)

        posting = s.query(Posting).get(posting_id)

        if posting.user == current_user and posting.display:
            posting.display = False
            s.add(posting)
            s.commit()
            cache.delete_memoized(query_postings)
            flash('Архивировано')
        else:
            flash('А ты не можешь это архивировать')
        return redirect(back_redirect_url())


class PostingThanksView(BaseView):
    template_name = 'thanks.html'

    def dispatch_request(self):
        return render_template(self.template_name)


class NeedTeamCreateView(BaseView):
    template_name = 'need_team_form.html'
    decorators = [login_required]

    def dispatch_request(self):
        s = current_app.session_factory()

        form = TeamPostingCreateForm()
        if form.validate_on_submit():
            posting = NeedTeamPosting(
                name=form.name.data.strip(),
                oneliner=form.oneliner.data.strip(),
                description=form.description.data.strip(),
                url=form.url.data.strip(),
                contact=form.contact.data.strip(),
            )
            posting.user = current_user
            s.add(posting)
            s.commit()
            return redirect(url_for('postings.posting_thanks'))

        return self.render_template(form=form)


class NeedWorkCreateView(BaseView):
    template_name = 'need_work_form.html'
    decorators = [login_required]

    def dispatch_request(self):
        s = current_app.session_factory()

        form = TeamPostingCreateForm()
        if form.validate_on_submit():
            posting = NeedWorkPosting(
                name=form.name.data.strip(),
                oneliner=form.oneliner.data.strip(),
                description=form.description.data.strip(),
                url=form.url.data.strip(),
                contact=form.contact.data.strip(),
            )
            posting.user = current_user
            s.add(posting)
            s.commit()
            return redirect(url_for('postings.posting_thanks'))

        return self.render_template(form=form)