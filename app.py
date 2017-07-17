from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:fred123@localhost:8889/blogz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sygsapyeevhjou:177c0e3f2d1552f13bc2000d3c6eb1913e7a780932f9cea55eef7b0cf943f087@ec2-184-73-199-72.compute-1.amazonaws.com:5432/ddo005ds9e3no4'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
