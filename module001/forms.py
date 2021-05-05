from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length

class CourseForm(FlaskForm): # class RegisterForm extends FlaskForm
    id = StringField('id')
    name = StringField('Course Name',validators=[InputRequired(),Length(min=1,max=50)])
    institution_name = StringField('Institution Name')
    code = StringField('Course Code')

class FollowForm(FlaskForm): # class RegisterForm extends FlaskForm
    code = StringField('Enter the course code you wish to follow / unfollow:',validators=[InputRequired(),Length(min=1,max=50)])