from flask import Flask, render_template, current_app, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False

db=SQLAlchemy(app)

class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key = True)
    
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.SNo} - {self.title}"
    
with app.app_context():
    db.create_all()

@app.route('/' , methods=['GET' , 'POST'])
def hello_world():
    if request.method== 'POST':
        title=request.form['title']
        desc=request.form['desc']

        todo=Todo(title=title , desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    

    return render_template('index.html', allTodo=allTodo)

    # return "<p>Hello World</p>"

@app.route('/show')
def products():
   allTodo = Todo.query.all()
   print(allTodo)
   return redirect('/')


@app.route("/delete/<int:SNo>")
def delete(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first()
    if todo:
       db.session.delete(todo)
       db.session.commit()
    return redirect('/')
@app.route("/update/<int:SNo>" , methods=['POST' , "GET"])
def update(SNo):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(SNo=SNo).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(SNo=SNo).first()
    return render_template("update.html", todo=todo)

if __name__ == "__main__":
    app.run(debug=True)