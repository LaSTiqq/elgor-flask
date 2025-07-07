from flask import Flask, Response, render_template, request, jsonify
from flask_static_digest import FlaskStaticDigest
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from flask_mail import Message, Mail
from config import Config
from utils import restricted_list, year
from forms import ContactForm
import requests
import re
import os

flask_static_digest = FlaskStaticDigest()

app = Flask(__name__)
app.config.from_object(Config)

flask_static_digest.init_app(app)
csrf = CSRFProtect(app)
talisman = Talisman(app, content_security_policy=None, force_https=False)
mail = Mail(app)


@app.route("/", methods=["GET"])
def index():
    current_year = year()
    form = ContactForm()
    return render_template('index.html', form=form, current_year=current_year)


@app.route("/send-ajax", methods=["POST"])
def send_ajax():
    form = ContactForm()
    if form.validate_on_submit():
        if any(restricted_list(form[field].data) for field in ['name', 'subject', 'message']):
            return jsonify({"status": "warning", "message": "You wrote something disallowed! Please try again."}), 400

        recaptcha_response = request.form.get('g-recaptcha-response')
        secret_key = os.getenv('RECAPTCHA_PRIVATE_KEY')
        verification_url = "https://www.google.com/recaptcha/api/siteverify"
        response = requests.post(verification_url, data={
            'secret': secret_key,
            'response': recaptcha_response
        })
        result = response.json()
        if not result.get('success') or result.get('score', 0) < app.config['RECAPTCHA_REQUIRED_SCORE']:
            return jsonify({"status": "warning", "message": "Captcha verification failed. Please try again."}), 400

        html_content = render_template("email.html", name=form.name.data,
                                       sender=form.email.data, content=form.message.data)
        text_content = re.sub(r"<[^>]+>", "", html_content)
        try:
            msg = Message(
                subject=form.subject.data,
                sender=app.config['MAIL_USERNAME'],
                recipients=['forvest@inbox.lv'],
                body=text_content
            )
            msg.html = html_content
            mail.send(msg)
            return jsonify({"status": "success", "message": "Message sent!"})
        except Exception:
            return jsonify({"status": "danger", "message": "Something went wrong! Please try again."}), 500


@app.route('/sitemap.xml')
def sitemap_xml():
    content = render_template('crawlers/sitemap.xml')
    return Response(content, mimetype='application/xml')


@app.route('/robots.txt')
def robots_txt():
    content = render_template('crawlers/robots.txt')
    return Response(content, mimetype='text/plain')


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        "error.html",
        error_code=404,
        error_message="Page Not Found",
        error_comment="You have reached a non-existent page."
    ), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template(
        "error.html",
        error_code=500,
        error_message="Internal Server Error",
        error_comment="An error occurred, and the server could not fulfill your request."
    ), 500
