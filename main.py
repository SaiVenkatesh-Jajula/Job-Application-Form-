from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["MAIL_USERNAME"] = 'saivenkatesh619@gmail.com'
app.config["MAIL_PASSWORD"] = 'lfzwbmpcwxtasafu'

app.config["MAIL_USE_SSL"] = True
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465


db = SQLAlchemy(app)
mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=['POST', 'GET'])
def index():
    # After submit button
    if request.method == 'POST':
        fname = request.form['firstname']
        lname = request.form['lastname']
        email = request.form['Email']
        date = request.form['date']
        dateobj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form['occupation']

        form = Form(fname=fname, lname=lname, email=email, date=dateobj, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        flash(f"{fname}, Form submitted successfully", 'success')

        message_body = f"Hi {fname}! Your application form was successfully submitted.\n" \
                       f"Here your data is:\n" \
                       f"{fname}\n" \
                       f"{lname}\n" \
                       f"{occupation}"
        message = Message(subject="New Form Submitted", sender=app.config["MAIL_USERNAME"],recipients=[email],
                          body=message_body)
        mail.send(message)

        # Redirect to different route
        return redirect(url_for('submitted'))

    return render_template('index.html')


@app.route("/submitted")
def submitted():
    return render_template('Notification.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
