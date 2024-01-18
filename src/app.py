from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://root:1234+Abcd@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()
db=SQLAlchemy(app)
ma=Marshmallow(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))

    def __init__(self, title, description):
        self.title = title
        self.description=description



## Lee todas las clases que sean de db.Models
## Crea todas las tablas que tengamos definidas como en este flask

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

task_schema=TaskSchema()
tasks_schema= TaskSchema(many=True)

@app.route('/tasks', methods=['POST'])
def create_task():
    #print(request.json)
    title= request.json['title']
    description= request.json['description']

    new_task= Task(title, description)
    print('Tarea creada con éxito')

    #Almacenamos los datos en la base de datos
    db.session.add(new_task)
    db.session.commit()
    print("Almacenamiento en la base de datos --> OK!")
    print(new_task)
    return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks=Task.query.all()
    result=task_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/task/<id>', methods=['GET'])
def get_task(id):
    task=Task.query.get(id)
    return task_schema.jsonify(task)

@app.route('/task/<id>', methods=['PUT'])
def update_task(id):

    task=Task.query.session.get(Task, id)
    title=request.json["title"]
    description=request.json['description']

    task.title=title
    task.description=description

    db.session.commit()

    print(title,description)

    return task_schema.jsonify(task)


@app.route('/task/<id>', methods=['DELETE'])
def detele_task(id):
    task=Task.query.session.get(Task, id)

    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message':'Welcome to my first API with Python Flask and MySQL'})

@app.route('/task/dekete', methods=['DELETE'])
def delete_tasks():
    db.session.query(Task).delete()
    db.session.commit()

    return jsonify({"message":"All tasks deleted!!!"})

if __name__ == "__main__":
    app.run(debug=True)