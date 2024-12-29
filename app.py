from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=["GET"])
def main():
    students = Student.query.all()
    return render_template('main.html', students=students)

@app.route('/add', methods=["GET","POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        email = request.form["email"]
        student = Student(name=name, age=age, email=email)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=["GET","POST"])
def edit(id):
    student = Student.query.get_or_404(id)
    if request.method == "POST":
        student.name = request.form['name']
        student.age = request.form['age']
        student.email = request.form['email']
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('edit.html',student=student)

@app.route('/delete/<int:id>', methods=["POST"])
def delete(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(debug=True)