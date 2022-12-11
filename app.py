from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key  = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cargo.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database
db = SQLAlchemy(app)

# Create Database Model
class Cargo(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,name):
        self.name = name

    #Function to return
    def __repr__(self) -> str:
        return '<Name %r>' % self.id 

cargo_num = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/view")
def view():
    return render_template('view.html', values=Cargo.query.all())

@app.route('/vehicle')
def vehicle():
    return render_template('vehicle.html')

@app.route('/cargo', methods=['GET','POST'])
def cargo():
    if request.method == 'POST':
        length = request.form['length']
        height = request.form['height']
        width = request.form['width']
        print(length,height,width)
        volume = 0.01 * (int(length) * int(height) * int(width)) 
        new_volume = Cargo(name=volume)
        new_item = volume
        try:
            db.session.add(new_volume)
            db.session.commit()
            return render_template('output.html',l=length,h=height,w=width,v=volume)
        except:
            return "There was an error"
    else:
        volumes = Cargo.query.order_by(Cargo.date_created)
        return render_template('output.html', values = Cargo.query.all()) 

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)