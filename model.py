# Create Database Model
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CargoModel(db.Model):    
    __tablename__ = "table"
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(200), nullable=False)

    price_per_weight = db.Column(db.Integer, nullable=False)
    cbm = db.Column(db.Integer, nullable= False)
    profit = db.Column(db.Integer, nullable=False)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,price_per_weight,cbm,profit):
        #self.id = id  # autocreate bc primary_key
        #self.name = name        
        self.price_per_weight = price_per_weight
        self.cbm = cbm 
        self.profit = profit
        #self.date_created = date_created
 
    #Function to return
    def __repr__(self) -> str:
        return '<Name %r>' % self.id 