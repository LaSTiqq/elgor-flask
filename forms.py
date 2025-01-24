from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField(
        label='Name',
        render_kw={
            'class': 'form-control mb-1',
            'placeholder': 'Your name *',
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Length(min=3, max=15)
        ],
    )
    email = EmailField(
        label='Email',
        render_kw={
            'class': 'form-control my-1',
            'placeholder': 'Your email *',
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Email()
        ],
    )
    subject = StringField(
        label='Topic',
        render_kw={
            'class': 'form-control my-1',
            'placeholder': 'Message topic *',
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Length(min=5, max=30)
        ],
    )
    message = TextAreaField(
        label='Text',
        render_kw={
            'class': 'form-control bg-transparent mt-1',
            'placeholder': 'Message text',
            'autocomplete': 'off',
            'rows': 6,
        },
        validators=[
            DataRequired(),
            Length(min=50)
        ],
    )
