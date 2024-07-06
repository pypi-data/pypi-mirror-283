from flask_sqlalchemy import SQLAlchemy
from config import sql_connection
from ShopifyTupperware import app

app.config['SQLALCHEMY_DATABASE_URI'] = sql_connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['legacy_schema_aliasing'] = False
#app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)
engine = db.get_engine(app)
