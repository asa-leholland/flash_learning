from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError
from flash_learning.models.student import Student
import re
def check_password(form, field):
    if len(field.data) < 8:
        raise ValidationError('Password must greater than 4 character')
    if re.search("[0-9]",field.data)!=None:
        length=len(field.data)
        index=0
        count=1
        while index<length-1:
            num1=field.data[index]
            num2 = field.data[index+1]
            #convert to int
            if ord(num1) > 47 and ord(num1) < 58:
                num1 = int(num1)
            num2 = field.data[index + 1]
            if ord(num2) > 47 and ord(num2) < 58:
                num2 = int(num2)
            index = index + 1
            #check if conversation susccesful
            if type(num1)!=int or type(num2)!=int:
                count=1
                continue
            #check if incrementing
            if num1+1==num2 or num1==num2:
                count=count+1
            else:
                count=1
            if count==3:
                raise ValidationError("Password can't have 123;456 or other single-incrementing numbers")
    if re.search("password",field.data,re.IGNORECASE)!=None and  re.search("password",field.data,re.IGNORECASE).start()==0:
        raise ValidationError('Password can not start with  the word Password[case-insenstive]')
    if len(re.findall("[A-Z]", field.data, re.IGNORECASE))==0:
        raise ValidationError('Password must contain at least 1 letter')
    if len(re.findall("[0-9]",field.data))==0:
        raise ValidationError('Password must contain at least 1 number')
    if (len(re.findall("[A-Z]",field.data,re.IGNORECASE))+len(re.findall("[0-9]",field.data)))==len(field.data):
        raise ValidationError('Password must contain at least 1 symbol')
    if re.search(form.username.data,field.data,re.IGNORECASE)!=None:
        raise ValidationError("Password Can Not Contain User Name")
    if re.search(form.first_name.data,field.data,re.IGNORECASE)!=None:
        raise ValidationError("Password Can Not Contain First Name")
    if re.search(form.last_name.data,field.data,re.IGNORECASE)!=None:
        raise ValidationError("Password Can Not Last Name")

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("Sign In")

class ResetForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[DataRequired(),check_password])
    username = StringField('username', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    submit = SubmitField("Reset")




class SignupForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    grade = IntegerField('grade', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(),check_password])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """Check if the username is already taken."""

        user = Student.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        """Check if the email is already tied to an account."""

        email = Student.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError("Please use a different email address.")
