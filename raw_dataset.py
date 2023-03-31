from model import  CargoModel, db


def getRawData():
    cargo = [
    {'cbm':	5	,  'profit':	 10000 	},
    {'cbm':	3	,  'profit':	 6500 	},
    {'cbm':	7	,  'profit':	 12500 	},
    {'cbm':	4	,  'profit':	 8000 	},
    {'cbm':	2	,  'profit':	 4000 	},                    
    {'cbm':	6	,  'profit':	 11500 	},
    {'cbm':	8	,  'profit':	 15000 	},
    {'cbm':	1	,  'profit':	 2000 	},
    {'cbm':	9	,  'profit':	 18000 	},
    {'cbm':	2	,  'profit':	 3500 	},                    
    {'cbm':	6	,  'profit':	 11000 	},
    {'cbm':	3	,  'profit':	 5500 	},
    {'cbm':	7	,  'profit':	 14000 	},
    {'cbm':	4	,  'profit':	 7500 	},
    {'cbm':	2	,  'profit':	 3000 	},                    
    {'cbm':	5	,  'profit':	 9500 	},
    {'cbm':	8	,  'profit':	 16500 	},
    {'cbm':	1	,  'profit':	 1500 	},
    {'cbm':	4	,  'profit':	 7000 	},
    {'cbm':	3	,  'profit':	 5000 	},                    
    {'cbm':	6	,  'profit':	 10500 	},
    {'cbm':	2	,  'profit':	 3500 	},
    {'cbm':	9	,  'profit':	 19500 	},
    {'cbm':	7	,  'profit':	 13000 	},
    {'cbm':	5	,  'profit':	 9000 	},                    
    {'cbm':	1	,  'profit':	 1500 	},
    {'cbm':	3	,  'profit':	 5000 	},
    {'cbm':	4	,  'profit':	 6500 	},
    {'cbm':	6	,  'profit':	 10000 	},
    {'cbm':	8	,  'profit':	 16000 	}
    ]  
    

    # Inserting the user data
    try:
        for raw_data in cargo:
            comp_data = CargoModel(**raw_data)
            db.session.add(comp_data)
        db.session.commit()
        return f"Successfully added raw data"
    except Exception as err:            
        return f"ERROR404: Manual data import failed. " 