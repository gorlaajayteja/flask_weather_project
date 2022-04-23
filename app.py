from os import name
import logging
import requests
from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/classicmodels'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='thisissecretkey'
db=SQLAlchemy(app)


class City(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
db.create_all()

a=City(name='pithapuram')
b=City(name='kakinada')
db.session.add_all([a,b])
# db.session.commit()

def get_weather_data(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=e1713ddc5fab11fc1ecf70d945591123'
    r=requests.get(url.format(city)).json()
    return r
@app.route("/")
def index_get():
    cities=City.query.all()
    
    weather_data=[]
    for city in cities:
        r=get_weather_data(city.name)

        weather={
                'city':city.name,
                'temperature':r['main']['temp'],
                'description' :r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon']
        }
        weather_data.append(weather)
    return render_template('weather.html',weather_data=weather_data)

@app.route("/",methods=['POST'])
def index_post():
    new_city=request.form.get('city')
    err_message=""
    if new_city:
        new1=City.query.filter_by(name=new_city).first()
        if not new1:
            new_data=get_weather_data(new_city)
            if new_data['cod']==200:
                new_city_obj=City(name=new_city)
                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_message="city does not existed in the world!!!"
        else:
            err_message="city already existed in the database!!!"
    
    if err_message:
        flash(err_message,'error')
    else:
        flash('city inserted successfully!')
    return redirect(url_for('index_get'))

if __name__=='__main__':
    app.run(debug=True)
#e1713ddc5fab11fc1ecf70d945591123