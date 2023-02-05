from flask import Flask, render_template, redirect, request, session, url_for, flash
from db import Actions, config
from flask_mail import Mail

# Initializing the flask webapp
app = Flask(__name__)

# Assigning a secret key for session
app.secret_key = 'super-secret-key'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USE_TSL=False,
    MAIL_USERNAME='*********',
    MAIL_PASSWORD='*********'
)
mail = Mail(app)

execute = Actions(config)


# Renders the home page
@app.route('/')
def home():
    return render_template('index.html')


# Renders the join page
@app.route('/join', methods=['GET', 'POST'])
def join():
    form = request.form.to_dict()

    # Form validation
    if 'name' in form and 'birthday' in form and 'gender' in form:
        session['name'] = name = form['name']
        session['birthday'] = birthday = form['birthday']
        session['gender'] = gender = form['gender']
        session['spot'] = spot = execute.new_spot()
        execute.new_entry(name, birthday, gender, spot)
        return redirect('/queue')

    return render_template('join.html')


# Rendering the Queue page
@app.route('/queue')
def queue():
    name = session['name']
    session['spot'] = execute.get_spot(name)
    infront = execute.total_infront(name)
    if session['spot'] is not None:
        return render_template('queue.html', name=session['name'], spot=session['spot'][0], total_infront=infront)

    return render_template('queue.html', name=name, spot=1, total_infront=infront)


# Handling when a person leaves
@app.route('/leave')
def leave():
    if 'name' in session:
        name = session['name']
        spot = session['spot']
        execute.leave(name, spot)
        for i in list(session.keys()):
            session.pop(i, None)

        return redirect(url_for('join'))

# Renders the contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        mail.send_message('HospQueue: New message from ' + name,
                          sender = email,
                          recipients = ['*********'],
                          body = 'Email-ID: ' + email + '\n\n' + message,
                          )

        flash("Thanks for sending the message!", "success")
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(debug=True)
