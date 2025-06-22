from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField(
        label='Name',
        id='name',
        render_kw={
            'class': 'form-control',
            'placeholder': 'Your name',
            'autocomplete': 'off',
            'value': 'John',
        },
        validators=[
            DataRequired(),
            Length(min=3, max=15)
        ],
    )
    email = EmailField(
        label='Email',
        id='email',
        render_kw={
            'class': 'form-control',
            'placeholder': 'Your email',
            'autocomplete': 'off',
            'value': 'john.doe@gmail.com',
        },
        validators=[
            DataRequired(),
            Email()
        ],
    )
    subject = StringField(
        label='Topic',
        id='subject',
        render_kw={
            'class': 'form-control',
            'placeholder': 'Topic',
            'autocomplete': 'off',
            'value': 'Collaboration',
        },
        validators=[
            DataRequired(),
            Length(min=5, max=25)
        ],
    )
    message = TextAreaField(
        label='Message',
        id='message',
        render_kw={
            'class': 'form-control',
            'placeholder': 'Message',
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Length(min=20)
        ],
    )
