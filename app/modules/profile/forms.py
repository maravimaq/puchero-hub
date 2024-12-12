from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class UserProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    surname = StringField('Surname', validators=[DataRequired(), Length(max=100)])
    orcid = StringField('ORCID', validators=[
        Length(min=19, max=19, message='ORCID must be exactly 19 characters long'),
        Regexp(r'^\d{4}-\d{4}-\d{4}-\d{4}$', message='Invalid ORCID format')
    ])
    affiliation = StringField('Affiliation', validators=[
        Length(min=5, max=100, message='Affiliation must be between 5 and 100 characters')
    ])

    submit = SubmitField('Save profile')
