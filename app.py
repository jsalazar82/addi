import os
from flask import Flask, request, jsonify, render_template
from config import configbyname
from medium import db
from models import Client

def create_app():
    application = Flask(__name__)
    application.config.from_object(os.environ['APP_SETTINGS'])#configbyname[os.getenv('APP_SETTINGS') or 'dev'])
    db.init_app(application)
    return application

app = create_app()
app.app_context().push()


#Index
@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')
    #return "This is the app index"

#Add client and money
@app.route("/add", methods=['GET', 'POST'])
def add_client():
    #name=request.args.get('name')
    #money=request.args.get('money')
    name=request.form['name']
    money=request.form['money']
    try:
        client=Client(
            name=name,
            money=money
        )
        db.session.add(client)
        db.session.commit()
        return "Client added with id={}".format(client.id)
    except Exception as e:
	    return(str(e))

#Get all clients
@app.route("/getall")
def get_all():
    try:
        clients=Client.query.all()
        return  jsonify([e.serialize() for e in clients])
    except Exception as e:
	    return(str(e))

#Get client by ID
@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        client=Client.query.filter_by(id=id_).first()
        return jsonify(client.serialize())
    except Exception as e:
	    return(str(e))

#Get client by Name
@app.route("/getn/<name_>")
def get_by_name(name_):
    try:
        client=Client.query.filter_by(name=name_).first()
        return jsonify(client.serialize())
    except Exception as e:
	    return(str(e))
 
#Delete client by Id
@app.route("/delete/<id_>")
def delete_by_id(id_):
    try:
        client=Client.query.filter_by(id=id_).first()
        db.session.delete(client)
        db.session.commit()
        return "Client id={}".format(client.id) + " deleted - Name: " + client.name
    except Exception as e:
	    return(str(e))

#Update client name by Id 
@app.route("/updaten/<id_>/<name_>", methods=['GET', 'PUT'])
def modificar_name(id_, name_):
    try:
        client=Client.query.filter_by(id=id_).first()
        #TODO: Read from a json parameter and change the values
        client.name = name_
        db.session.commit()
        return "Client update with id={}".format(client.id)
    except Exception as e:
	    return(str(e))

#Update client money by Id 
@app.route("/updatem/<id_>/<money_>", methods=['GET', 'PUT'])
def modificar_money(id_, money_):
    try:
        client=Client.query.filter_by(id=id_).first()
        #TODO: Read from a json parameter and change the values
        client.money = money_
        db.session.commit()
        return "Client update with id={}".format(client.id)
    except Exception as e:
	    return(str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
