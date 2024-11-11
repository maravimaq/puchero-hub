from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length, Optional


class CommunityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=256)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1024)])
    created_at = DateTimeField('Created At', format='%Y-%m-%d %H:%M:%S', validators=[Optional()])
    owner_id = IntegerField('Owner ID', validators=[DataRequired()])  # Normalmente no se expone en formularios de usuario
    submit = SubmitField('Create Community')
