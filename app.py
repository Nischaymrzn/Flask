from flask import Flask,render_template, request, redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
import secrets
#The Flask(__name__) line thus creates an instance of the Flask application, which you can then use to define routes using the @app.route decorator and to start the development server with app.run().
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
app.secret_key = secrets.token_hex(16)    #Flask uses the secret key to sign session cookies, ensuring that the data stored in these cookies has not been tampered with

app.permanent_session_lifetime=timedelta(minutes=1) #session is removed after 1minutes

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    description=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:         #whenever todo model is printed then what should be seen
        return f"{self.sno} - {self.title}"

with app.app_context():  # Ensure operations are within the application context
    db.create_all()  # Create database tables if they don't exist


@app.route("/")
def landing():
    if ("user" in session):
        return redirect(url_for("hello_world"))
        
    else:
        return redirect(url_for("login_page"))


@app.route("/login", methods=['GET','POST'])
def login_page():
     if request.method=='POST':
         user=request.form["email"]
         session["user"]=user;
         return redirect(url_for("hello_world"))
          
     else:
        return render_template('login.html')

@app.route('/home', methods=['GET','POST'])  #@app.route- routes
def hello_world():
    if request.method=="POST":
        print("post")
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,description=desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo=Todo.query.all()    
    return render_template('index.html',allTodo=allTodo)   #rendering templates



@app.route('/delete/<int:sno>', methods=['GET', 'DELETE'])
def delete(sno):

        todo=Todo.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect("/home")



@app.route('/logout')
def logout():
    print("logout btn clicked")
    session.clear()
    
    return redirect(url_for('login_page'))




if __name__=="__main__":
    app.run(debug=True)   #entry point of the script, and the app.run(debug=True) line starts the Flask development server, which listens for incoming HTTP requests.