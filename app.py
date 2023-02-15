from flask import Flask, render_template, request, redirect, url_for, flash
from compute_package import computeCargo
from model import db,CargoModel
#from compute_package import computeCargo  <---- old CargoModel

from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataCargo.db'
db.init_app(app)

# migrate = Migrate(app,db)

# Arrays declaration
dataList = []

@app.before_first_request
def create_table():
    db.create_all()

# ================================= #
#       ROUTES for Functions        #
# ================================= #

@app.route('/')
def index():
    return redirect('/optimize')
    # return render_template('index.html')

@app.route('/buffer', methods=['GET','POST']) 
def buffer(): ## NOT USED
    return render_template('buffer.html')


# Compute Using BnB Algorithm           -- not yet implemented
@app.route('/optimize', methods=['GET','POST'])
def Optimize():  
    
    results=computeCargo(CargoModel)
    print("-"*25,"@"*10,"-"*25)
    print(results)
    return "END RESULT DONE"


# [CREATE]                               ---  done
@app.route('/cargo/create' , methods=['GET','POST'])
def cargo():
    if request.method == 'GET':
        return render_template('cargo.html')
    
    if request.method == 'POST':
        cargos = CargoModel(
            price_per_weight = request.form['price_per_weight'],
            cbm = request.form['cbm'],
            profit = request.form['profit']
        )        
        #volume = 0.01 * (int(length) * int(height) * int(width))         
        db.session.add(cargos)
        db.session.commit()
        return redirect ('/showData')


@app.route('/vehicle', methods=['GET','POST'])
def vehicle():
    if request.method == 'POST':
        climit = request.form['vehicle_limit']
        db.session.add(climit)
        db.session.commit()    
    return render_template ('vehicle.html')
    

# [RETRIEVE] Show all data          -- 70% done  
@app.route('/showData', methods=['GET','POST'])
def showData():
    # data = CargoModel.query.order_by(CargoModel.date_created)
    result = CargoModel.query.all()
    # print("The DATABASE", result)
    # if result.cargonumer not in dataList execute for loop --- for algorithm!!!
    for item in result:
        dataList.append(item.cbm)
    print(dataList)
    return render_template('showData.html', result=result)

## ADD Single Retrieve FUNCTION             --- in progress
@app.route('/showSingleData/<int:pkgID>')
def GetSingleCargo(pkgID):
    cargos = CargoModel.query.filter_by(id = pkgID).first()
    if cargos:
        return render_template('showOneData.html', cargos = cargos)
    return f"ERROR: --- \nCargo # {pkgID} does not exist. "


# [UPDATE]                  -- ID not working? ? ? 
@app.route('/update/<int:pkgID>', methods = ['GET', 'POST'])
def update(pkgID):
    cargos = CargoModel.query.filter_by(id=pkgID).first()
    if request.method == 'POST':
        if cargos:
            db.session.delete(cargos)
            db.session.commit()

            newCargos = CargoModel(
            price_per_weight = request.form['price_per_weight'],
            cbm = request.form['cbm'],
            profit = request.form['profit']
            )
            db.session.add(newCargos)
            db.session.commit()
            return redirect(f'/update/{pkgID}')
        return f"ERROR: --- \nCargo # {pkgID} does not exist. "
    return render_template('cargoUpdate.html', cargos = cargos)
    

# [DELETE]  -                   -- no changes 
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