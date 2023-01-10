from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy





app = Flask(__name__)

#SqlAlchemy Database Configuration

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Secret Key"

db = SQLAlchemy(app)
app.app_context().push()

# Creating model table for database
class Data(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    company= db.Column(db.String(100))
    

    def __init__(self, name, email, phone,  company):

        self.name = name
        self.email = email
        self.phone = phone
        self.company = company

    def __repr__(self):
        return f"{self.name}:{self.email}"

db.create_all()

#This is the index route where we are going to
#query on all contact data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", contacts = all_data)


#this route is for inserting data to database via html forms
@app.route('/insert', methods = ['GET', 'POST'])
def insert():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        company = request.form['company']

        my_data = Data(name, email,phone,company)
        db.session.add(my_data)
        db.session.commit()

        flash("Contact Added Successfully")

        return redirect(url_for('Index'))



#this is update route where we are going to update contact
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.company = request.form['company']

        db.session.commit()
        flash("Contact Updated Successfully")

        return redirect(url_for('Index'))




#This route is for deleting contact
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Contact Deleted Successfully")

    return redirect(url_for('Index'))



#This route is for search contact
@app.route('/search', methods=['POST'])
def search_contacts():
  query = request.form['query']
  search_results = Data.query.filter(Data.name.contains(query)).all()
  return render_template('search_results.html', contacts=search_results)







if __name__ == "__main__":
    app.run(debug=True,port=5007)
