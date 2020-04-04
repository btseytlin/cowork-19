from flask import redirect, url_for
from flask_login import current_user
from flask_admin.contrib import sqla
from flask_admin import expose, AdminIndexView

from ..utils import is_admin


class AdminModelView(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and is_admin(current_user)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("postings.posting_list"))


class ProtectedIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (current_user.is_authenticated and is_admin(current_user)):
            return redirect(url_for("postings.posting_list"))
        return super(ProtectedIndexView, self).index()
