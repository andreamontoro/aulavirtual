from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user
from models import get_db, User, Course, Follow, ParticipationCode, ParticipationRedeem
from module001.forms import *
from sqlalchemy import or_, and_
import random
module001 = Blueprint("module001", __name__,static_folder="static",template_folder="templates")
db = get_db()


@module001.route('/')
@login_required
def module001_index():
    user = User.query.filter_by(id=current_user.id).first()
    if current_user.profile in ('admin','staff','student'):
        return render_template("module001_index.html",module="module001", user=user)
    else:
        flash("Access denied!")
#        abort(404,description="Access denied!")
        return redirect(url_for('index'))

@module001.route('/test')
def module001_test():
    return 'OK'

@module001.route('/course', methods=['GET','POST'])
@login_required
def module001_course():
    form = CourseForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if not form.id.data:
                course = Course(name=form.name.data.strip(),
                                institution_name = form.institution_name.data.strip(),
                                user_id=current_user.id)
                db.session.add(course)
                db.session.commit()
                course.code = 'C'+str(course.id)+''.join(random.choice('AILNOQVBCDEFGHJKMPRSTUXZ') for i in range(4))
                newname = form.name.data.strip().replace('-' + course.code,'')
                if '-' + course.code not in newname:
                    course.name = newname + '-' + course.code
                try:
                    db.session.commit()
                    flash("Course created successfully with code: {}".format(course.code))
                except:
                    db.session.rollback()
                    flash("Error creating course!")
            else:
                change = 0
                course = Course.query.get(form.id.data)
                newcoursename = form.name.data.strip().replace('-' + course.code,'') + '-' + course.code
                if course.name != newcoursename:
                    course.name = newcoursename
                    change = 1

                newinstitutionname = form.institution_name.data.strip()
                if course.institution_name != newinstitutionname:
                    course.institution_name = newinstitutionname
                    change = 1

                try:
                    if change:
                        db.session.commit()
                        flash("Course  updated successfully!")
                    else:
                        flash("Nothing has changed!")
                except:
                    db.session.rollback()
                    flash("Error updating course!")
                return redirect(url_for('module001.module001_course'))

    elif ('rowid' in request.args):
        course = Course.query.get(request.args['rowid'])
        if not course or course.user_id != current_user.id:
            flash('Error retrieving data for the course {}'.format(request.args['rowid']))
        else:
            form = CourseForm(id=course.id, name=course.name.replace('-' + course.code,''), institution_name = course.institution_name, code=course.code)

    courses = Course.query.filter_by(user_id=current_user.id)
    return render_template("module001_course.html",module="module001", form=form, rows=courses)


@module001.route('/follow',methods=['GET','POST'])
@login_required
def module001_follow():
    form = FollowForm()
    unfollow=False
    if request.method == 'POST':
        if form.validate_on_submit():
            course_code = form.code.data
            follow = Follow.query.filter(and_(Follow.course_code==form.code.data,
                                              Follow.user_id==current_user.id)).first()
            if follow:
                flash("You are already following the course {} ".format(course_code))
            else:
                course = Course.query.filter_by(code=form.code.data).first()
                if not course:
                    flash('The code {} is invalid, try again with the correct code.'.format(form.code.data))
                else:
                    follow = Follow(user_id=current_user.id,
                                    course_id=course.id,
                                    course_code=course.code,
                                    course_name=course.name,
                                    institution_name = course.institution_name)
                    try:
                        db.session.add(follow)
                        db.session.commit()
                        flash("You are now following {}".format(course.name))
                    except:
                        db.session.rollback()
                        flash("Error following!")
    elif ('sharedlink' in request.args):
        form=FollowForm(code=request.args.get('code'))

    follows = Follow.query.filter_by(user_id=current_user.id)
    return render_template('module001_follow.html',module="module001", form=form, rows=follows, unfollow=unfollow)


@module001.route('/unfollow',methods=['GET','POST'])
@login_required
def module001_unfollow():
    form = FollowForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            course_code = form.code.data
            follow = Follow.query.filter(and_(Follow.course_code==form.code.data,
                                              Follow.user_id==current_user.id)).first()
            if follow:
                try:
                    db.session.delete(follow)
                    db.session.commit()
                    flash("You are not following {} any longer".format(course_code))
                    return redirect(url_for('module001.module001_follow'))
                except:
                    db.session.rollback()
                    flash("Error unfollowing!")
        flash('Something unusual happened, please try again later')
    else:
        form=FollowForm(code=request.args.get('code'))
    unfollow=True
    follows = Follow.query.filter_by(user_id=current_user.id)

    return render_template('module001_follow.html',module="module001", form=form, rows=follows, unfollow=unfollow)



@module001.route('/participation_generate')
@login_required
def module001_participation_generate():
    flash("participation_generate!")
    return redirect(url_for('index'))

from qrcode import QRCode, ERROR_CORRECT_L
@module001.route('/sharing_details',methods=['GET','POST'])
@login_required
def module001_sharing_details():
    qr = QRCode(version=20, error_correction=ERROR_CORRECT_L)
    base_url=request.host
    if request.args.get('itemtype') == 'course':
        course = Course.query.get(request.args.get('rowid'))
        if not course or course.user_id != current_user.id:
            flash("An error has occurred retrieving details for the activity")
            return redirect(url_for('module001.module001_course'))
        qr.add_data("http://{}/follow?sharedlink=1&code={}".format(base_url,course.code))
        module,itemtype,item="library","course",course
#    else:
#        participation = ParticipationCode.query.get(request.args.get('rowid'))
#        if not participation or participation.user_id != current_user.id:
#            flash("An error has occurred retrieving details for the participation")
#            return redirect(url_for('module001.module001_participation_generate'))
#        qr.add_data("http://{}/participation_redeem?sharedlink=1&code={}".format(base_url,participation.code))
#        module,itemtype,item="participation_gerenate","participation",participation
    try:
        qr.make() # Generate the QRCode itself
        im = qr.make_image()
        filename = "./static/qrcodes/{}.png".format(item.code)
        urlfilename = "http://{}/static/qrcodes/{}.png".format(base_url,item.code)
        im.save(filename)
        return render_template('module001_sharing_details.html',module="module001", item=item, itemtype=itemtype,filename=urlfilename,base_url=base_url)
    except:
        return render_template('module001_sharing_details.html',module="module001", item=item, itemtype=itemtype,base_url=base_url)



