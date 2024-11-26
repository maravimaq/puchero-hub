from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, IntegerField
from wtforms.validators import Optional, NumberRange
from app.modules.dataset.models import PublicationType  # Import PublicationType


class ExploreForm(FlaskForm):
    title = StringField('Title', validators=[Optional()])
    author = StringField('Author', validators=[Optional()])
    date_from = DateField('Date From', validators=[Optional()])
    date_to = DateField('Date To', validators=[Optional()])
    size_from = IntegerField('Size From (KB)', validators=[Optional(), NumberRange(min=0)])
    size_to = IntegerField('Size To (KB)', validators=[Optional(), NumberRange(min=0)])
    format = StringField('Format', validators=[Optional()])
    files_count = IntegerField('Number of Files', validators=[Optional(), NumberRange(min=0)])
    publication_type = SelectField(
        'Publication Type',
        choices=[('any', 'Any')] + [(pt.value, pt.name.replace('_', ' ').title()) for pt in PublicationType],
        validators=[Optional()]
    )
    sorting = SelectField(
        'Sort By',
        choices=[('newest', 'Newest First'), ('oldest', 'Oldest First')],
        validators=[Optional()]
    )
    submit = SubmitField('Search')