from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class NominateForm(FlaskForm):

    reporter = SelectField('Reporter')
    nominee = SelectField('Nominee')
    category = SelectField('Category')
    submit = SubmitField('Nominate')
