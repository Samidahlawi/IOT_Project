from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,RadioField,IntegerField,TextField,BooleanField,FieldList,FormField
from wtforms.validators import DataRequired,Length,NumberRange,Email,InputRequired


class SignupForm(FlaskForm):
    username = StringField('Username',	validators=[DataRequired("Please Enter a Username")])
    password = PasswordField('Password',	validators=[DataRequired("Please Enter a Password"),Length(min=4,message="Please Enter More than 4 characters")])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email')])


class LoginForm(FlaskForm):
    username = StringField('Username',	validators=[DataRequired("Please Enter a Username")])
    password = PasswordField('Password',	validators=[DataRequired("Please Enter a Password")])
    remember = BooleanField('remember me')



class ExperimentForm(FlaskForm):
    title = StringField('Title',	validators=[DataRequired("Please Enter a title")])
    description = TextField("Description")
    etype = RadioField('Type',choices=[('Data Collection','Data Collection'),('Performance Evalution','Performance Evalution'),('Education','Education')],validators=[DataRequired("Please Choose a type")])
    protocol = RadioField('Protocol',choices=[('Zigbee','Zigbee'),('6lowpan','6lowpan')],validators=[DataRequired("Please Choose a type")])
    duration = IntegerField("Duration",validators=[NumberRange(min=0, max=10000)])

class NodeForm(FlaskForm):
    name = StringField('Node Name')
    temperature = IntegerField('Temperature Interval')
    humdity = IntegerField('Humdity Interval')
    mode = BooleanField('Coordinator?')

class NodesForm(FlaskForm):
    nodes = FieldList(FormField(NodeForm),min_entries=2,max_entries=7)

class ScenarioForm(FlaskForm):
    en1 = IntegerField("Sender")
    en2 = IntegerField("Reciver")