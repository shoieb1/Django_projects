from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object('config.Config')

mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user[4], password):  # Assuming user[4] is the hashed password
            login_user(User(user[0]))  # Assuming user[0] is the ID
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO blogs (title, content) VALUES (%s, %s)", (title, content))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('blog'))
    return render_template('create.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/blog')
def blog():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM blogs")
    blogs = cur.fetchall()
    cur.close()
    return render_template('blog.html', blogs=blogs)

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out')
    return redirect(url_for('home'))

@app.route('/send_contact', methods=['POST'])
def send_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact_number = request.form['contact_number']
        message = request.form['message']
        
        # Save this information to the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (name, email, contact_number, message) VALUES (%s, %s, %s, %s)", 
                    (name, email, contact_number, message))
        mysql.connection.commit()
        cur.close()
        
        flash('Your message has been sent successfully!')
        return redirect(url_for('contact_us'))

    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(debug=True)