from flask import Blueprint, render_template, request, session, redirect, url_for,g
from flask import views

import config
from .decorators import login_required
from .forms import LoginForm
from .models import CMSUser

bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.route("/")
@login_required
def index():
    return render_template("cms/cms_index.html")

@bp.route("/logout")
@login_required
def logout():
    # session.clear()
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


class LoginView(views.MethodView):

    def get(self, message=None):

        return render_template("cms/cms_login.html", message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    # 如果设置session.permanent=True那么过期时间是31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message="邮箱或密码错误")

        else:
            # print(form.errors)
            message = form.errors.popitem()[1][0]
            print(message)
            return self.get(message=message)





bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
