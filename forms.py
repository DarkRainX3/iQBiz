from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class F_Blanket_Order(FlaskForm):
    increment = StringField('Order Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')

