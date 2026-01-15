import os

class Config:
    SECRET_KEY = "secret-key-change-this"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
