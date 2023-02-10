from flask import Flask, render_template, request, redirect, url_for, flash
from model import db,CargoModel
#from compute_package import computeCargo  <---- old CargoModel

from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataCargo.db'
db.init_app(app)

# migrate = Migrate(app,db)

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buffer', methods=['GET','POST'])
def buffer():
    return render_template('buffer.html')

# Compute Using BnB Algorithm
@app.route('/optimize', methods=['GET','POST'])
def Optimize():
    return
    #computeCargo(CargoModel,db),

#[CREATE] done
@app.route('/cargo/create' , methods=['GET','POST'])
def cargo():
    if request.method == 'GET':
        return render_template('cargo.html')
    
    if request.method == 'POST':
        price_per_weight = request.form['price_per_weight']
        cbm = request.form['cbm']           
        profit = request.form['profit']
        #volume = 0.01 * (int(length) * int(height) * int(width)) 
        cargos = CargoModel(price_per_weight=price_per_weight, cbm = cbm, profit=profit)
        db.session.add(cargos)
        db.session.commit()
        return redirect ('/showData')

@app.route('/vehicle', methods=['GET','POST'])
def vehicle():
    if request.method == 'POST':
        climit = request.form['vehicle_limit']
        db.session.add(climit)
        db.session.commit()
        return redirect ('/cargo')


# [READ] Show all data in database in Tables done
@app.route('/showData', methods=['GET','POST'])
def showData():
    # data = CargoModel.query.order_by(CargoModel.date_created)
    result = CargoModel.query.all()
    print("The DATABASE", result)
    return render_template('showData.html', result=result)

#[UPDATE]
# [DELETE]
@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = CargoModel.query.get_or_404(id)
    print(item_to_delete)
    items = CargoModel.query.all()
    for i in items:
        if i.id == item_to_delete:
            w.remove(i.name)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return render_template('output.html',values = CargoModel.query.all())
    except:
        return render_template('output.html',values = CargoModel.query.all())


if __name__ == '__main__':    
    app.run(host='localhost', port=5000)
    # db.drop_all()
    # db.create_all()    
    app.run(debug = True)