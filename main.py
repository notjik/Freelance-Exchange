import flask
import flask_login
import datetime
import pymorphy2
import os
from flask import Flask, render_template, redirect, request, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user
from random import shuffle

from data import db_session
from data.users import User
from data.jobs import Jobs
from data.services import Services
from data.branches import Branch
from data.register import RegisterForm
from data.login import LoginForm
from data.editprofile import EditProfileForm
from data.editservice import EditServiceForm
from data.editjob import EditJobForm
from data.addservice import AddServiceForm
from data.addjob import AddJobForm

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')

login_manager = LoginManager()
login_manager.init_app(app)


@app.template_filter('dtfilter')
def dtfilter(date):
    morph = pymorphy2.MorphAnalyzer(lang='ru')
    day = morph.parse('день')[0]
    hour = morph.parse('час')[0]
    minutes = morph.parse('минута')[0]
    second = morph.parse('секунда')[0]
    res = datetime.datetime.now() - date
    if res.month:
        return f'{res.month} {day.make_agree_with_number(res.days).word}' \
               f'{res.days} {day.make_agree_with_number(res.days).word}' \
               f'{res.seconds // 3600} {hour.make_agree_with_number(res.seconds // 3600).word} ' \
               f'{(res.seconds // 60) % 60} {minutes.make_agree_with_number((res.seconds // 60) % 60).word} ' \
               f'{res.seconds % 60 % 60} {second.make_agree_with_number(res.seconds % 60 % 60).word}'
    if res.days:
        return f'{res.days} {day.make_agree_with_number(res.days).word} ' \
               f'{res.seconds // 3600} {hour.make_agree_with_number(res.seconds // 3600).word} ' \
               f'{(res.seconds // 60) % 60} {minutes.make_agree_with_number((res.seconds // 60) % 60).word} ' \
               f'{res.seconds % 60 % 60} {second.make_agree_with_number(res.seconds % 60 % 60).word}'
    if res.seconds // 3600:
        return f'{res.seconds // 3600} {hour.make_agree_with_number(res.seconds // 3600).word} ' \
               f'{(res.seconds // 60) % 60} {minutes.make_agree_with_number((res.seconds // 60) % 60).word} ' \
               f'{res.seconds % 60 % 60} {second.make_agree_with_number(res.seconds % 60 % 60).word}'
    if (res.seconds // 60) % 60:
        return f'{(res.seconds // 60) % 60} {minutes.make_agree_with_number((res.seconds // 60) % 60).word} ' \
               f'{res.seconds % 60 % 60} {second.make_agree_with_number(res.seconds % 60 % 60).word}'
    return f'{res.seconds % 60 % 60} {second.make_agree_with_number(res.seconds % 60 % 60).word}'


@app.template_filter('stddate')
def stddate(date):
    return date.strftime('%d/%m/%Y')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неверный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пользователь с этой почтой уже существует")
        if db_sess.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пользователь с этим никнеймом уже существует")
        user = User(
            email=form.email.data,
            nickname=form.nickname.data,
            surname=form.surname.data,
            name=form.name.data,
            speciality=form.speciality.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/preview/services/<int:s_id>')
def response_service_preview(s_id):
    db_sess = db_session.create_session()
    image = db_sess.query(Services).get(s_id)
    if image:
        return app.response_class(image.preview, mimetype='application/octet-stream')
    else:
        return flask.abort(404)


@app.route('/preview/jobs/<int:s_id>')
def response_job_preview(s_id):
    db_sess = db_session.create_session()
    image = db_sess.query(Jobs).get(s_id)
    if image:
        return app.response_class(image.preview, mimetype='application/octet-stream')
    else:
        return flask.abort(404)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    services = db_sess.query(Services).all()
    users = db_sess.query(User).all()
    branches = db_sess.query(Branch).all()
    names = {name.id: name.nickname for name in users}
    emails = {email.id: email.email for email in users}
    branche = {branch.id: branch.specialization for branch in branches}
    return render_template("index.html", services=services, names=names, emails=emails, branches=branche,
                           title='Доступные услуги')


@app.route("/jobs")
def ind_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = db_sess.query(User).all()
    names = {name.id: name.nickname for name in users}
    emails = {email.id: email.email for email in users}
    return render_template("jobs.html", jobs=jobs, names=names, emails=emails,
                           title='Доступные вакансии')


@app.route("/myprofile")
def myprofile():
    if flask_login.current_user.is_authenticated:
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        services = db_sess.query(Services).all()
        jobs = db_sess.query(Jobs).all()
        branches = db_sess.query(Branch).all()
        emails = {email.id: email.email for email in users}
        branche = {branch.id: branch.specialization for branch in branches}
        return render_template("myprofile.html", services=services, emails=emails, jobs=jobs, branches=branche,
                               title='Мой профиль')
    else:
        return redirect("/login")


@app.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    if flask_login.current_user.is_authenticated:
        edit_profile_form = EditProfileForm()
        if edit_profile_form.validate_on_submit():
            db_sess = db_session.create_session()
            u_id = flask_login.current_user.id
            # if edit_profile_form.password.data != edit_profile_form.password_again.data:
            #     return render_template('editprofile.html', title='Editing a profile', form=edit_profile_form,
            #                            message="Passwords don't match")
            if edit_profile_form.new_password.data:
                user = db_sess.query(User).filter_by(id=u_id).first()
                if user.check_password(edit_profile_form.old_password.data):
                    user.set_password(edit_profile_form.new_password.data)
                else:
                    return render_template('editprofile.html', title='Изменить профиль', form=edit_profile_form,
                                           message="Старый пароль не корректен или не введен")
            elif edit_profile_form.old_password.data:
                return render_template('editprofile.html', title='Изменить профиль', form=edit_profile_form,
                                       message="Новый пароль не введен")
            if edit_profile_form.name.data:
                db_sess.query(User).filter_by(id=u_id).update({'name': edit_profile_form.surname.data})
            if edit_profile_form.surname.data:
                db_sess.query(User).filter_by(id=u_id).update({'surname': edit_profile_form.name.data})
            if edit_profile_form.speciality.data:
                db_sess.query(User).filter_by(id=u_id).update({'speciality': edit_profile_form.speciality.data})
            db_sess.commit()
            return redirect('/')
        return render_template('editprofile.html', title='Изменить профиль', form=edit_profile_form)
    else:
        return redirect("/login")


@app.route('/editservice/<int:s_id>', methods=['GET', 'POST'])
def editservice(s_id):
    if flask_login.current_user.is_authenticated:
        edit_service_form = EditServiceForm()
        if request.method == 'POST':
            db_sess = db_session.create_session()
            if edit_service_form.service.data:
                db_sess.query(Services).filter_by(id=s_id).update({'service': edit_service_form.service.data})
            if edit_service_form.description.data:
                db_sess.query(Services).filter_by(id=s_id).update({'description': edit_service_form.description.data})
            if edit_service_form.branch.data:
                db_sess.query(Services).filter_by(id=s_id).update({'branch_id': edit_service_form.branch.data})
            if edit_service_form.price.data:
                db_sess.query(Services).filter_by(id=s_id).update({'price': edit_service_form.price.data})
            if edit_service_form.preview.data:
                if edit_service_form.preview.data.content_type.split('/')[1] in ['jpg', 'jpeg', 'png']:
                    file = edit_service_form.preview.data.read()
                    db_sess.query(Services).filter_by(id=s_id).update({'preview': file})
                else:
                    return render_template('editservice.html', title='Изменить услугу', form=edit_service_form,
                                           message='Загруженный файл не удовлетворяет формату')
            db_sess.query(Services).filter_by(id=s_id).update({'action': edit_service_form.action.data})
            db_sess.commit()
            return redirect('/myprofile')
        return render_template('editservice.html', title='Изменить услугу', form=edit_service_form)
    else:
        return redirect("/login")


@app.route('/addservice', methods=['GET', 'POST'])
def addservice():
    if flask_login.current_user.is_authenticated:
        add_service_form = AddServiceForm()
        if request.method == 'POST':
            db_sess = db_session.create_session()
            u_id = flask_login.current_user.id
            if not add_service_form.branch.data:
                return render_template('addservice.html', title='Добавить услугу', form=add_service_form,
                                       message='Категория не указана')
            elif add_service_form.preview.data:
                if add_service_form.preview.data.content_type.split('/')[1] in ['jpg', 'jpeg', 'png']:
                    file = add_service_form.preview.data.read()
                    service = Services(
                        service=add_service_form.service.data,
                        contractor=u_id,
                        description=add_service_form.description.data,
                        branch_id=add_service_form.branch.data,
                        price=add_service_form.price.data,
                        preview=file
                    )
                    db_sess.add(service)
                    db_sess.commit()
                else:
                    return render_template('addservice.html', title='Добавить услугу', form=add_service_form,
                                           message='Загруженный файл не удовлетворяет формату')
            else:
                service = Services(
                    service=add_service_form.service.data,
                    contractor=u_id,
                    description=add_service_form.description.data,
                    branch_id=add_service_form.branch.data,
                    price=add_service_form.price.data,
                )
                db_sess.add(service)
                db_sess.commit()
            return redirect('/myprofile')
        return render_template('addservice.html', title='Добавить услугу', form=add_service_form)
    else:
        return redirect("/login")


@app.route('/editjob/<int:s_id>', methods=['GET', 'POST'])
def editjob(s_id):
    if flask_login.current_user.is_authenticated:
        edit_job_form = EditJobForm()
        if request.method == 'POST':
            db_sess = db_session.create_session()
            if edit_job_form.job.data:
                db_sess.query(Jobs).filter_by(id=s_id).update({'job': edit_job_form.job.data})
            if edit_job_form.description.data:
                db_sess.query(Jobs).filter_by(id=s_id).update({'description': edit_job_form.description.data})
            if edit_job_form.price.data:
                db_sess.query(Jobs).filter_by(id=s_id).update({'price': edit_job_form.price.data})
            if edit_job_form.preview.data:
                if edit_job_form.preview.data.content_type.split('/')[1] in ['jpg', 'jpeg', 'png']:
                    file = edit_job_form.preview.data.read()
                    db_sess.query(Jobs).filter_by(id=s_id).update({'preview': file})
                else:
                    return render_template('editjob.html', title='Изменить вакансию', form=edit_job_form,
                                           message='Загруженный файл не удовлетворяет формату')
            db_sess.query(Jobs).filter_by(id=s_id).update({'action': edit_job_form.action.data})
            db_sess.commit()
            return redirect('/myprofile')
        return render_template('editjob.html', title='Изменить вакансию', form=edit_job_form)
    else:
        return redirect("/login")


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    if flask_login.current_user.is_authenticated:
        add_job_form = AddJobForm()
        if request.method == 'POST':
            db_sess = db_session.create_session()
            u_id = flask_login.current_user.id
            if add_job_form.preview.data:
                if add_job_form.preview.data.content_type.split('/')[1] in ['jpg', 'jpeg', 'png']:
                    file = add_job_form.preview.data.read()
                    job = Jobs(
                        job=add_job_form.job.data,
                        client=u_id,
                        description=add_job_form.description.data,
                        price=add_job_form.price.data,
                        preview=file
                    )
                    db_sess.add(job)
                    db_sess.commit()
                else:
                    return render_template('addjob.html', title='Добавить вакансию', form=add_job_form,
                                           message='Загруженный файл не удовлетворяет формату')
            else:
                job = Jobs(
                    job=add_job_form.job.data,
                    contractor=u_id,
                    description=add_job_form.description.data,
                    price=add_job_form.price.data,
                )
                db_sess.add(job)
                db_sess.commit()
            return redirect('/myprofile')
        return render_template('addjob.html', title='Добавить вакансию', form=add_job_form)
    else:
        return redirect("/login")


if __name__ == '__main__':
    db_session.global_init("db/freelance_exchange.db")
    app.run()
