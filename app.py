"""
TODO 
Add flash messagges
Add Blood receiver table
Disable donate button according the threshold(3 Months)
"""

from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from datetime import datetime


file_name = 'BloodDonation.db'
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{file_name}"
db = SQLAlchemy(app)

class BloodDonation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    blood_groups = db.Column(db.String)
    city = db.Column(db.String)
    phone_no = db.Column(db.String, unique= True)
    #donation_count = db.Column(db.Integer)
    #latest_donation = db.Column(db.Integer)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/empty_db')
def no_donations():
    return render_template('empty_db.html')

@app.route('/blood_donation', methods=['GET','POST'])
def blood_donation():
    if request.method == 'GET':
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        return render_template('donate.html', blood_groups = blood_groups)
    else:
        data_fields = ['name','age','blood_groups','city','phone_no']
    
        data_dict = {}
    
        for field in data_fields:
            data_dict[field] = request.form.get(field).lower()

        for value in data_dict.values():
           if value == "":
                return "Please enter all the details." 
                  


        blood_donation = BloodDonation(**data_dict)
        db.session.add(blood_donation)
        db.session.commit()

        return redirect(url_for('home'))
    
@app.route('/blood_receive', methods=['GET','POST'])
def blood_receive():
    if request.method == 'GET':

        all_donations = BloodDonation.query.all()
        if all_donations == []:
            print('Sorry no donations available')
            return render_template('empty_db.html')

        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        return render_template('find_blood.html', blood_groups = blood_groups)

    else:
        blood_groups = request.form.get('blood_groups').lower()
        city = request.form.get('city').lower()

        if city == "":
            return "Please enter all the details." 
        elif city != city:
            return "Your city is not available"

        print(city, blood_groups)
        result = BloodDonation.query.\
            filter_by(blood_groups = blood_groups).\
            filter_by(city = city).\
                all()


    print(result)
    return render_template('results.html', blood_donations=result)

@app.route('/take_donation')
def take_donation():
    blood_donation_id = request.args.get('id')
    result = BloodDonation.query.get(blood_donation_id)
    print(result)
    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)