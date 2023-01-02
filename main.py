from flask import Flask, render_template, request, redirect, session, jsonify
from flask.helpers import make_response
import random
import smtplib
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(10)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="tharun@159",
  database="real_estate",
)
mycursor=mydb.cursor()

@app.route('/')
def home():
  return render_template('login.html')

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')


@app.route('/login_validation', methods=['POST'])
def login_validiation():
      Email = request.form.get('Email')
      password = request.form.get('password')
      mycursor.execute('SELECT * FROM admin WHERE AdminEMAIL=%s AND Password=%s',(Email,password))
      admin = mycursor.fetchall()
      mycursor.execute('SELECT * FROM broker WHERE BrokerEMAIL=%s AND Password=%s',(Email,password))
      broker = mycursor.fetchall()
      print(admin)
      if len(admin)>0:
          session['AdminID'] = int(admin[0][0])
          session['AdminNAME']=admin[0][1]
          return redirect('/admin')
      elif len(broker)>0:
          session['BrokerID'] = int(broker[0][0])
          session['BrokerNAME']=broker[0][1]
          return redirect('/broker')
      else:
          return render_template('login.html', error_message="Invalid Email Id or Password")

@app.route('/admin')
def admin():
   mycursor.execute('select * from broker')
   brokers=mycursor.fetchall()
   mycursor.execute('select * from property')
   properties=mycursor.fetchall()
   return render_template('admin.html',number=session['AdminNAME'],properties=properties,brokers=brokers)

@app.route('/add_broker')
def add_broker():
  mycursor.execute('select * from property')
  props=mycursor.fetchall()
  mycursor.execute('select max(PropertyID) from property')
  mxID=mycursor.fetchall()
  return render_template('addbroker.html',props=props,mxID=mxID[0])


property=1

@app.route('/add_brokers', methods=['POST'])
def add_broker1():
  email=request.form.get('Email')
  password=request.form.get('password')
  name=request.form.get('Name')
  contact=request.form.get('Contact')
  global property
  property=int(request.form.get('property'))
  experience=request.form.get('experience')
  commission=request.form.get('commission')
  status=request.form.get('status')
  status=bool(status)
  experience=int(experience)
  commission=int(commission)
  property=int(property)
  mycursor.execute('insert into broker(BrokerNAME,BrokerEMAIL,BrokerMobileNum,BrokerEXP,BrokerCOMM,BrokerSTAT,password) value(%s,%s,%s,%s,%s,%s,%s)',(name,email,contact,experience,commission,status,password))
  mydb.commit()
  return redirect('/admin_index')

@app.route('/admin_index')
def admin_index():
  mycursor.execute('select max(BrokerID) from broker')
  myid=mycursor.fetchall()
  mynum=myid[0][0]
  print(property)
  mycursor.execute('insert into relation value (%s,%s)',(mynum,property))
  mydb.commit()
  return redirect('/admin')

@app.route('/add_property')
def add_property():
    return render_template('addproperty.html')

@app.route('/add_properties',methods=['POST'])
def add_properties():
  name=request.form.get('Name')
  contact=request.form.get('Contact')
  address=request.form.get('address')
  city=request.form.get('city')
  zipcode=request.form.get('zipcode')
  kind=request.form.get('kind')
  area=int(request.form.get('area'))
  valuation=float(request.form.get('valuation'))
  status=int(request.form.get('status'))
  mycursor.execute('insert into property(PropertyOwnerNAME,PropertyOwernMobileNum,PropertyADD,PropertyCITY,ProperyCODE,PropertyKind,PropertyAREA,PropertyVAL,PropertySTAT) value(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(name,contact,address,city,zipcode,kind,area,valuation,status))
  mydb.commit()
  return redirect('/admin')

@app.route('/broker')
def broker():
  print(session['BrokerID'])
  mycursor.execute("""select * from property inner join relation on relation.PropertyID=property.PropertyID where relation.BrokerID='{}'""".format(session['BrokerID']))
  properties=mycursor.fetchall()
  return render_template('broker.html',number=session['BrokerNAME'],properties=properties)

@app.route('/delete_broker', methods=['post'])
def delete_broker():
  id=int(request.form.get('delete'))
  mycursor.execute("""delete from broker where BrokerID='{}'""".format(id))
  mydb.commit()
  return redirect('/admin')

@app.route('/delete_property', methods=['post'])
def delete_property():
  id=int(request.form.get('delete'))
  mycursor.execute("""delete from property where PropertyID='{}'""".format(id))
  mydb.commit()
  return redirect('/admin')

@app.route('/edit_broker',methods=['post'])
def edit_broker():
  id=int(request.form.get('edit'))
  mycursor.execute('select * from property')
  props=mycursor.fetchall()
  mycursor.execute("""select * from broker where BrokerID='{}'""".format(id))
  broks=mycursor.fetchall()
  mycursor.execute('select max(PropertyID) from property')
  mxID=mycursor.fetchall()
  mycursor.execute("""select * from property where PropertyID in (select distinct PropertyID from relation where BrokerID='{}')""".format(id))
  brokerprops=mycursor.fetchall()
  mycursor.execute("""select * from property where PropertyID not in (select distinct PropertyID from relation where BrokerID='{}')""".format(id))
  brokernotprops=mycursor.fetchall()
  
  return render_template('edit_broker.html',props=props,mxID=mxID[0],broks=broks[0],brokerprops=brokerprops,brokernotprops=brokernotprops)

@app.route('/edit_broker_details1', methods=['post'])
def edit_broker_details1():
  email=request.form.get('Email')
  password=request.form.get('password')
  name=request.form.get('Name')
  contact=request.form.get('Contact')
  experience=int(request.form.get('experience'))
  commission=int(request.form.get('commission'))
  status=int(request.form.get('status'))
  id=request.form.get('btn1')
  mycursor.execute("""update broker set BrokerNAME='{}',BrokerEMAIL='{}',BrokerMobilenUM='{}',BrokerEXP='{}',BrokerCOMM='{}',BrokerSTAT='{}',password='{}' where BrokerID='{}'""".format(name,email,contact,experience,commission,status,password,id))
  mydb.commit()
  return redirect('/admin')

@app.route('/edit_broker_details2', methods=['post'])
def edit_broker_details2():
  p=int(request.form.get('property'))
  id=request.form.get('btn2')
  mycursor.execute("""insert into relation value('{}','{}')""".format(id,p))
  mydb.commit()
  return redirect('/admin')

@app.route('/edit_broker_details3', methods=['post'])
def edit_broker_details3():
  p1=int(request.form.get('property'))
  p2=int(request.form.get('property1'))
  id=int(request.form.get('btn3'))
  mycursor.execute("""update relation set PropertyID='{}' where PropertyID='{}' and BrokerID='{}'""".format(p2,p1,id))
  mydb.commit()
  return redirect('/admin')

@app.route('/edit_property_main',methods=['post'])
def edit_property_main():
  id=int(request.form.get('edit'))
  mycursor.execute("""select * from property where PropertyID='{}'""".format(id))
  props=mycursor.fetchall()
  return render_template('edit_property.html',prop=props[0])

@app.route('/edit_property', methods=['post'])
def edit_property():
  name=request.form.get('Name')
  contact=request.form.get('Contact')
  address=request.form.get('address')
  city=request.form.get('city')
  zipcode=request.form.get('zipcode')
  kind=request.form.get('kind')
  area=int(request.form.get('area'))
  valuation=float(request.form.get('valuation'))
  status=int(request.form.get('status'))
  id=int(request.form.get('edit'))
  mycursor.execute("""update property set PropertyOwnerNAME='{}',PropertyOwernMobileNum='{}',PropertyADD='{}',PropertyCITY='{}',ProperyCODE='{}',PropertyKind='{}',PropertyAREA='{}',PropertyVAL='{}',PropertySTAT='{}' where PropertyID='{}'""".format(name,contact,address,city,zipcode,kind,area,valuation,status,id))
  mydb.commit()
  return redirect('/admin')

if __name__ == '__main__':
  app.run(debug=True)