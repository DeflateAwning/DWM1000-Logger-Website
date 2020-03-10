
# apps/forms.py


#from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField
from wtforms.validators import DataRequired, Optional


class AddAnchorForm(FlaskForm):
    anchorNumber = IntegerField('Anchor Number', validators=[DataRequired()])
    enabled = BooleanField('Anchor Enabled?', validators=[])

    anchorCoordX = FloatField('Anchor X Coord (Meters)', validators=[Optional()], default=None)
    anchorCoordY = FloatField('Anchor Y Coord (Meters)', validators=[Optional()], default=None)

    anchorCoordXSteps = FloatField('Anchor X Coord (Steps)', validators=[Optional()], default=None)
    anchorCoordYSteps = FloatField('Anchor Y Coord (Steps)', validators=[Optional()], default=None)
