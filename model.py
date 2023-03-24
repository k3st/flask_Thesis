# Create Database Model
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CargoModel(db.Model):    
    __tablename__ = "table"
    id = db.Column(db.Integer, primary_key=True)
    # keyID = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(200), nullable=False)

    # price_per_weight = db.Column(db.Integer, nullable=False)
    cbm = db.Column(db.Float, nullable= False)
    profit = db.Column(db.Float, nullable=False)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,cbm,profit):
        #self.id = id  #bcoz id is auto-increment
        #self.name = name        
        # self.price_per_weight = price_per_weight
        self.cbm = cbm 
        self.profit = profit
        #self.date_created = date_created
 
    #Function to return
    def __repr__(self) -> str:
        return '<CargoID: %r>' % self.id 




class TempModel(db.Model):
    __tablename__ = "temp"
    keyID = db.Column(db.Integer, primary_key=True)
    # vehicleLimit = db.Column(db.Integer)

    # def __init__(self, vehicleLimit):
    #     self.vehicleLimit = vehicleLimit

    # def __repr__(self) -> str:
    #     return '<Content %r>' % self.vehicleLimit 