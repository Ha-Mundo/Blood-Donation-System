"""
TODO 
Add flash messagges
Add donation counter
Disable donate button according the threshold(3 Months)
"""

from flask import Flask, request, jsonify, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import datetime
from time_limit import threshold_time, timer

file_name = 'BloodDonation.db'
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{file_name}"
db = SQLAlchemy(app)

class BloodDonation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    blood_groups = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    phone_no = db.Column(db.String, nullable=False)
    latest_donation = db.Column(db.DateTime, nullable=False)
    next_donation = db.Column(db.DateTime)
    donation_counter = db.Column(db.Integer, default=1)
    #timer = db.Column(db.Boolean)

    def __init__(self, name, age, blood_groups, city, phone_no, latest_donation, next_donation, donation_counter):
        self.name = name
        self.age = age
        self.blood_groups = blood_groups
        self.city = city
        self.phone_no = phone_no
        self.latest_donation = latest_donation
        self.next_donation = next_donation
        self.donation_counter = donation_counter

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
        donation_day = datetime.datetime.now()
        next_donation_date = threshold_time(donation_day)
       

        data_fields = ['name','age','blood_groups','city','phone_no']
    
        data_dict = {}
        data_dict['latest_donation'] = donation_day
        data_dict['next_donation'] = next_donation_date
        data_dict['donation_counter'] = 1                
        
        counter = data_dict['donation_counter']
    
        for field in data_fields:
            data_dict[field] = request.form.get(field).lower()

        for value in data_dict.values():
           if value == "":
                return "Please enter all the details." 
                  

        if db.session.query(BloodDonation).filter(BloodDonation.phone_no == data_dict['phone_no']) and \
            db.session.query(BloodDonation).filter(BloodDonation.next_donation <= data_dict['latest_donation']):
            #donation_number = db.session.query(BloodDonation.donation_counter)
            #total_donation = donation_number + counter
            #data_dict['donation_counter'] = total_donation
            blood_donation = BloodDonation(**data_dict)
            db.session.add(blood_donation)
            db.session.commit()
            
            return redirect(url_for('home'))   

        return "Donation forbidden!!!"

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

   
        print(city, blood_groups)
        result = BloodDonation.query.\
            filter_by(blood_groups = blood_groups).\
            filter_by(city = city).\
                all()

        if result == []:
            print('Sorry no donations available')
            return render_template('empty_db.html')
        else:
            return render_template('results.html', blood_donations=result)

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

@app.route('/all_donations_db', methods=['GET'] )
def all_donations_db():
    all_donations = BloodDonation.query.all()
    return render_template('results.html', blood_donations=all_donations)

if __name__ == '__main__':
    app.run(debug=True)