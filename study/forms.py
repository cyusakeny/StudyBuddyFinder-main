from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, InputRequired, ValidationError

def max_length_check(form, field):
    if len(field.data) > 5:
        raise ValidationError('You can select a maximum of 5 options.')

# Define the choices dictionary
subjects = [
    ('C++', 'C++'), 
    ('Python', 'Python'), 
    ('JavaScript', 'JavaScript'), 
    ('HTML', 'HTML'), 
    ('CSS', 'CSS'),
    ('React', 'React'),
    ('Angular', 'Angular'),
    ('Django', 'Django'),
    ('Flask', 'Flask'),
    ('Express', 'Express'),
    ('Node.js', 'Node.js'),
    ('MongoDB', 'MongoDB'),
    ('SQL', 'SQL'),
    ('PostgreSQL', 'PostgreSQL'),
    ('MySQL', 'MySQL'),
    ('Java', 'Java'),
    ('C#', 'C#'),
    ('Ruby', 'Ruby'),
    ('PHP', 'PHP'),
    ('Swift', 'Swift'),
    ('Kotlin', 'Kotlin'),
    ('Networking', 'Networking'),
    ('Docker', 'Docker'),
    ('Git', 'Git')
]

days_of_week = [
    ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')
]

time_slots = [
    ('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening')
]

languages = [
    ('English', 'English'), ('French', 'French'), ('Spanish', 'Spanish'), 
    ('Swahili', 'Swahili'), ('Kinyarwanda', 'Kinyarwanda')
]
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    submit = SubmitField('Login')
class ProfileForm(FlaskForm):
    school = StringField('School/College Name', validators=[DataRequired(), Length(max=100)])
    primary_language = SelectField('Primary Language', choices=languages, validators=[DataRequired()])
    secondary_languages = SelectMultipleField('Secondary Languages', choices=languages, coerce=str)
    days = SelectMultipleField('Select your days availability', choices=days_of_week, validators=[InputRequired()])
    times = SelectMultipleField('Select your time availability', choices=time_slots, validators=[InputRequired()])
    strong_subjects = SelectMultipleField('Select your strong subjects', choices=subjects, validators=[InputRequired(), max_length_check])
    weak_subjects = SelectMultipleField('Select your weak subjects', choices=subjects, validators=[InputRequired(), max_length_check])
    submit = SubmitField('Complete Profile')
class VerifyEmailForm(FlaskForm):
    otp = StringField('Verify your email', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify')
class ResendConfirmationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Resend Confirmation Email')
class CreateGroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired(), Length(max=100)])
    subject = SelectField('Select group subject', choices=subjects, validators=[InputRequired()])
    
    days = SelectMultipleField('Select group days', choices=days_of_week, validators=[InputRequired()])
    times = SelectMultipleField('Select group times', choices=time_slots, validators=[InputRequired()])
    submit = SubmitField('Create Group')
class ScheduleForm(FlaskForm):
    summary = StringField('Summary', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description', validators=[DataRequired(), Length(max=255)])
    start_datetime = DateTimeField('Start Date and Time', format='%d-%m-%Y %H:%M', validators=[DataRequired()])
    end_datetime = DateTimeField('End Date and Time', format='%d-%m-%Y %H:%M', validators=[DataRequired()])
    group_id = IntegerField('Group ID', validators=[DataRequired()])
    submit = SubmitField('Schedule Event')
class DeleteEventForm(FlaskForm):
    event_id = IntegerField('Event ID', validators=[DataRequired()])
    submit = SubmitField('Delete Event')
class ReviewForm(FlaskForm):
    message = StringField('Message', validators=[DataRequired(), Length(max=1024)])
    to =  StringField('User', validators=[DataRequired(), Length(max=50)])
    rating = StringField('Rating',validators=[DataRequired(),Length(max=5)])
    submit = SubmitField('Rate')