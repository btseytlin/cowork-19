from flask import redirect, url_for
from flask_login import current_user
from flask_admin.contrib import sqla
from flask_admin import expose, AdminIndexView

from ..utils import is_admin


class AdminModelView(sqla.ModelView):
    can_export = True
    can_delete = False
    column_searchable_list = ['name', 'description', 'user.email']
    column_filters = ['display']
    column_sortable_list = ['created_at',]
    column_default_sort = [('display', True), ('created_at', True)]

    column_list = ('user.email', 'name', 'oneliner', 'description', 'cv_url', 'display')

    form_ajax_refs = {
        'user': {
            'fields': ['email'],
            'page_size': 10
        }
    }

    def is_accessible(self):
        return current_user.is_authenticated and is_admin(current_user)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("postings.posting_list"))


class NeedTeamModelView(AdminModelView):
    column_list = ('user.email', 'name', 'oneliner', 'description', 'url', 'contact', 'display')


class ProtectedIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not (current_user.is_authenticated and is_admin(current_user)):
            return redirect(url_for("postings.posting_list"))
        return super(ProtectedIndexView, self).index()
