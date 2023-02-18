from flask import Flask, render_template, request, redirect, url_for, flash, session
from compute_package import computeCargo
from model import  db,CargoModel, VehicleModel #VehicleModel not used; changed to session
#from compute_package import computeCargo  <==== old CargoModel

from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.secret_key = "A"

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataCargo.db'
db.init_app(app)

# migrate = Migrate(app,db)

# Arrays declaration


@app.before_first_request
def create_table():
    # db.drop_all()  #Uncomment to delete all data in database
    db.create_all()
    session.pop("vehicleLimit", None)

# ================================= #
#       ROUTES for Functions        #
# ================================= #

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buffer', methods=['GET','POST']) 
def buffer(): ## NOT USED
    return render_template('buffer.html')

@app.route('/vehicle', methods=['GET','POST'])
def vehicle():
    if request.method =='GET':
        return render_template ('vehicle.html')

    if request.method == 'POST':
        try:
            if 'submit_button' in request.form:
                vehicleLimit = request.form['capacity']                
                print("Vehicle Choice: ", vehicleLimit)
        except Exception as err: 
            print(err)
            vehicleLimit = 13
        # newSize = VehicleModel(vehicleLimit=vehicleLimit)
        # db.session.add(newSize)
        # db.session.commit()
        # vehicleSize = VehicleModel.query.all()
        # print(vehicleSize)
        session ["vehicleLimit"] = vehicleLimit
        print("Data Inside Session => ", session ["vehicleLimit"] )
        return redirect ('/')

#                                       --- DONE
@app.route('/optimize', methods=['GET','POST'])
def optimize():
    if "vehicleLimit" in session:
        vehicleLimit = session ["vehicleLimit"]
        print("Condition True: ",vehicleLimit)
        vehicleLimit = 20
        #add error handling for computeCargo()
        results=computeCargo(CargoModel,vehicleLimit)        
        print("="*25,"@"*10,"="*25)
        print(results)
    else:
        print('No vehicle selected, redirect to /vehicle')
        return redirect('/vehicle')       
    
    return "END RESULT DONE"




# = = = = = = = = = = = = = = = = = = = =  #
# |         Create  Retrieve            |  #
# |         Update  Delete              |  #
# = = = = = = = = = = = = = = = = = = = =  #


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
    
# [RETRIEVE] Show all data          -- 70% done  
@app.route('/showData', methods=['GET','POST'])
def showData():
    # data = CargoModel.query.order_by(CargoModel.date_created)
    result = CargoModel.query.all()    
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




if __name__ == "__main__":    
    app.run(host='localhost', port=5000)
    app.run(debug = True)   