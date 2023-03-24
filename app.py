from flask import Flask, render_template, request, redirect, url_for, flash, session
from compute_package import computeCargo
from model import  db,CargoModel, TempModel #VehicleModel not used; changed to session
#from compute_package import computeCargo  <==== old CargoModel

# from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.secret_key = "A"

#Database
urlForDB = "postgresql://datacargo_user:Q7iWPt0jm5QKoxsdGrZ5klJ8V3CQjApv@dpg-cfro831gp3jo1ds3h5qg-a.singapore-postgres.render.com/datacargo" #use for Production
# urlForDB = 'sqlite:///dataCargo.db'  #use if local database

app.config['SQLALCHEMY_DATABASE_URI'] = urlForDB
db.init_app(app)

# migrate = Migrate(app,db)

# Arrays declaration


@app.before_first_request
def create_table():
    # db.drop_all()  #Uncomment to delete all data in database
    db.create_all()
    session.pop("vehicleLimit", None)


@app.route('/login', methods=['GET','POST'])
def loginPage():
    if request.method == 'POST':
        global userInfo
        userName = request.form['emailUser']    
        userPass = request.form['passwordUser']   
        if userName == "email@email.com" and userPass == "Test123!":  # CHANGE THIS BEFORE FINALS
            print("Password match")
            userInfo = "CredentialVerified"
            session ["currUser"] = userInfo
            return redirect(url_for('index'))        
        flash('Invalid email address or Password.') 
        return render_template('userLogin.html')
    return render_template('userLogin.html')

@app.route('/logout', methods=['GET','POST'])
def logoutUser():
    print("Current User has logout.")
    session.pop("currUser", None)
    session.pop("vehicleLimit", None)
    return redirect(url_for('index'))
    

 
# ================================= #
#       ROUTES for Functions        #
# ================================= #

@app.route('/')
def index():
    if "currUser" in session:
        return render_template('index.html')
    return redirect(url_for('loginPage'))

@app.route('/buffer', methods=['GET','POST']) 
def buffer(): ## NOT USED
    return render_template('buffer.html')

@app.route('/vehicle', methods=['GET','POST'])
def vehicle():
    if not "currUser" in session:
        return redirect(url_for('loginPage'))  
    if request.method =='GET':
        return render_template ('vehicle.html')    
    elif request.method == 'POST':
        global vehicleLimit
        try:
            if 'submit_button' in request.form:
                vehicleLimit = request.form['capacity']                
                print("Vehicle Choice: ", vehicleLimit)                
                session ["vehicleLimit"] = vehicleLimit
                print("Data Inside Session => ", session ["vehicleLimit"] )                
                return redirect ('/showData')                               
        except Exception as err: 
            print(err)
            return redirect ('/vehicle')
    

#                                       --- DONE
@app.route('/optimize', methods=['GET','POST'])
def optimize():
    if not "currUser" in session:
        return redirect(url_for('loginPage'))
    if "vehicleLimit" in session:
        vehicleLimit = session ["vehicleLimit"]
        print("Condition True: ",vehicleLimit)
        try:
            # results=computeCargo(CargoModel,vehicleLimit)        
            print("="*25,"@"*10,"="*25)
            # print(results)
            return render_template('optimize.html', data = computeCargo(CargoModel,vehicleLimit) )
        except Exception as err: 
            print(err)
            return render_template('error.html', err=err)
    else:
        print('No vehicle selected, redirect to /vehicle')
        return redirect('/vehicle')       
    
    


@app.route('/trial/<int:pkgID>', methods=['GET','POST'])
def getTrial(pkgID):
    err2 = None
    err = "package not found"
    # sample = db.get_or_404(CargoModel,pkgID,description=err)
    try:
        sample = db.get_or_404(CargoModel,pkgID)
    except Exception as err2:
        print(err2)

    if err2 is None:
        return render_template('index.html')
    print("ERROR --@@@")
    


# = = = = = = = = = = = = = = = = = = = =  #
# |         Create  Retrieve            |  #
# |         Update  Delete              |  #
# = = = = = = = = = = = = = = = = = = = =  #


# [CREATE]                               ---  done
@app.route('/cargo/create' , methods=['GET','POST'])
def cargo():
    if not "currUser" in session:
        return redirect(url_for('loginPage'))
    if request.method == 'GET':
        return render_template('cargo.html')
    
    if request.method == 'POST':
        cargos = CargoModel(
            # price_per_weight = request.form['price_per_weight'],
            cbm = request.form['cbm'],
            profit = request.form['profit']
        )        
        #volume = 0.01 * (int(length) * int(height) * int(width))         
        db.session.add(cargos)
        db.session.commit()
        return redirect('/cargo/create')
    
# [RETRIEVE] Show all data          -- 70% done 
@app.route('/showData', methods=['GET','POST'])
def showData():
    if not "currUser" in session:
        return redirect(url_for('loginPage'))
    # data = CargoModel.query.order_by(CargoModel.date_created)
    if request.method =='GET':
        result = CargoModel.query.all()    
        return render_template('showData.html', result=result)
    
    if request.method == 'POST':
        pkgID = request.form['pkgID']
        if pkgID == "0":
            err = "CARGO ID 0 is not possible..."
            return render_template('error.html', err=err)
        try:    
            data = db.get_or_404(CargoModel,pkgID)
        except Exception as err2:
            
            err = f"CargoID: ' {pkgID} '  is not in database... "
            return render_template("error.html",err = err)  
                            
        if request.form['submit_button'] == "update":
            return redirect (f'/update/{pkgID}')
        elif request.form['submit_button'] == "delete":
            return redirect (f'/delete/{pkgID}')
    

## ADD Single Retrieve FUNCTION             --- in progress
@app.route('/showSingleData/<int:pkgID>')
def GetSingleCargo(pkgID):
    cargos = CargoModel.query.filter_by(id = pkgID).first()
    if cargos:
        return render_template('showOneData.html', cargos = cargos)
    return f"ERROR: --- \nCargo # {pkgID} does not exist. "


# [UPDATE]                  -- DONE with error handl
@app.route('/update/<int:pkgID>', methods = ['GET', 'POST'])
def update(pkgID): 
    if not "currUser" in session:
        return redirect(url_for('loginPage')) 
    cargos = db.get_or_404(CargoModel,pkgID)
    if request.method == 'POST':
        # try:
        if cargos:         
            newCargos = CargoModel(
            # price_per_weight = request.form['price_per_weight'],
            cbm = request.form['cbm'],
            profit = request.form['profit']
            )
            db.session.delete(cargos)
            db.session.commit()
            db.session.add(newCargos)
            db.session.commit()
            return redirect('/showData')
        return f"ERROR404: UPDATE FUNCTION \nCargo # {pkgID} does not exist. "
        # except Exception as err: 
        #     err ="ERROR404: UPDATE FUNCTION \nCargo # {pkgID} does not exist. "
        #     print(err)
        #     return render_template('error.html', err=err)
    return render_template('cargoUpdate.html', cargos = cargos)
    

# [DELETE]  -                   -- DONE with error handl
@app.route('/delete/<int:pkgID>', methods = ['GET', 'POST'])
def delete(pkgID):
    if not "currUser" in session:
        return redirect(url_for('loginPage'))
    cargos = db.get_or_404(CargoModel,pkgID)    
    if request.method == 'POST':
        if cargos:
            # delCargo = CargoModel.query.filter_by(id=pkgID).first()
            db.session.delete(cargos)
            db.session.commit()
            return redirect('/showData')
        # except Exception as err: 
        #     err ="ERROR404: DELETE FUNCTION \nCargo # {pkgID} does not exist. "
        #     print(err)
        #     return render_template('error.html', err=err)
    return render_template('cargoDelete.html', cargos = cargos)


if __name__ == '__main__':    
    app.run(host='localhost', port=5000)
    app.run(debug = True)