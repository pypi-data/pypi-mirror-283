from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class SqlServerDatabase:
    def __init__(self, app : Flask, sql_connection: str) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = sql_connection
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['legacy_schema_aliasing'] = False
        #app.config["SQLALCHEMY_ECHO"] = True
        self.db = SQLAlchemy(app)
        self.engine = self.db.get_engine(app)

    @property
    def getDb(self):
        return self.db
    
    @property
    def getEngine(self):
        return self.engine
    
