from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import certifi
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://basitabass27411:iamahacker313@baiq.o4c0pn6.mongodb.net/?retryWrites=true&w=majority", tlsCAFile = certifi.where())

db = client['Bank']
coll = db['bankAccount']  

# coll.insert_one({'name': 'Basit Abass', 'account_number': 315, 'balance':0})

app = Flask(__name__) 

newBalance = 0

@app.route('/') 
def home():
     accounts = list(coll.find({}))
     return render_template("home.html", accounts = accounts)   

@app.route('/create-account', methods=['GET', 'POST'])  
def create():
     # balance = 0
     if request.method == 'GET': 
          balance = list(coll.find({}))
          return render_template("create.html", accounts = balance) 
     elif request.method == 'POST':
          name = request.form['name']
          account_number = request.form['accNumber'] 
          balance = request.form.get('amount', type=int) 
          coll.insert_one({'name':name, 'account number': account_number, 'balance': balance}) 
          return redirect('/') 

@app.route('/deposit', methods = ['GET', 'POST'])
def deposit(): 
     if request.method == 'GET':
          accountId = request.args.get('form')
          account = dict(coll.find_one({"_id": ObjectId(accountId)}))
          return render_template('deposit.html', account = account) 
     elif request.method == 'POST':
          id = request.form['_id']
          bal = request.form.get('balance', type=int)
          amount = request.form.get('amount', type=int)
          bal+=amount
          
          coll.update_one({'_id':ObjectId(id)}, {'$set':{'balance':bal}})
          return redirect('/')
          
@app.route('/withdraw', methods = ['GET', 'POST'])
def withdraw():
     if request.method == 'GET':
          accountId = request.args.get('form')
          account = dict(coll.find_one({"_id":ObjectId(accountId)}))
          return render_template('withdraw.html', account = account )  
     elif request.method == 'POST':
          name  = request.form['name']
          bal = request.form.get('balance', type=int)
          amount = request.form.get('amount', type=int)
          bal-=amount
          
          coll.update_one({'name':name}, {'$set':{'balance':bal}}) 
          return redirect('/')
     
     
     


if __name__ == "__main__":
     app.run(debug=True)

