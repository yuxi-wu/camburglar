from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class UrlForm(FlaskForm):
    '''
    '''
    length = StringField('Length', validators=[DataRequired])
    width = StringField('Width', validators=[DataRequired])
