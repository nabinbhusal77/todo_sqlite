from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from datetime import datetime

app = Flask(__name__)

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    """Creates model for Todo Database"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=False, nullable=False)
    description = db.Column(db.String(260), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Id: {self.id}\nTitle: {self.title}"



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        title_form = request.form['title']
        desc_form = request.form['desc']

        new_todo = Todo(title=title_form, description=desc_form)
        
        db.session.add(new_todo)
        db.session.commit()
        
    all_todo = Todo.query.all()
    return render_template('index.html', all_todo=all_todo)

@app.route('/delete/<int:id>')
def delete(id):
    delete_todo = Todo.query.filter_by(id=id).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    if request.method == "POST":
        
        print(type(todo))
        title_form = request.form['title']
        desc_form = request.form['desc']
        
        todo.title = title_form
        todo.description = desc_form

        db.session.add(todo)
        db.session.commit()

        return redirect("/")

    return render_template("update.html", todo=todo)



if __name__ == "__main__":
    app.run(debug=True)