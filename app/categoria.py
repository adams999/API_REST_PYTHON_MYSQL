from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# el puerto debe de ser el que esta corriendo el mysql ya sea en xampp o el puerto del servidor
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/api_rest_python_mysql'
# evitar los warnings al momento de trabajar
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)

# creacion de tabla categoria
class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))
    cat_est = db.Column(db.Integer)

    def __init__(self, cat_nom, cat_desp, cat_est = 1):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp
        self.cat_est = cat_est


db.create_all()

# squema para manejar las consultas
class CategoriaSchema(ma.Schema):
    class Meta:
        # fields es reservado de marshmellow schema
        fields = ('cat_id', 'cat_nom', 'cat_desp', 'cat_est')


# una sola respuesta
categoria_schema = CategoriaSchema()

# muchas respuestas
categorias_schema = CategoriaSchema(many=True)

# GET ##############################################


@app.route('/categoria', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)


#GET #############################################
@app.route('/categoria/<id>', methods=['GET'])
def get_categoria_x_id(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)


#POST##############################################
@app.route('/categoria/insert', methods=['POST'])
def insert_categoria():
    # recibe parametros de la peticion
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']
    nuevo_registro = Categoria(cat_nom, cat_desp, 1)
    db.session.add(nuevo_registro)
    db.session.commit()
    return categoria_schema.jsonify(nuevo_registro)


#PUT ################################################
@app.route('/categoria/update/<id>', methods=['PUT'])
def update_categoria(id):
    data = request.get_json(force=True)
    act_categoria = Categoria.query.get(id)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']

    act_categoria.cat_nom = cat_nom

    db.session.commit()

    return categoria_schema.jsonify(act_categoria)


#DELETE#############################################
@app.route('/categoria/delete/<id>', methods=['DELETE'])
def delete_categoria(id):
    elim_categoria = Categoria.query.get(id)
    elim_categoria.cat_est = 0
    db.session.commit()
    return categoria_schema.jsonify(elim_categoria)

# la ruta de la app y que tipo de parametros recibe


@app.route('/', methods=['GET'])
def index():
    return jsonify({'Mensaje': 'Bienvenido a la api de python con mysql'})


if __name__ == "__main__":  # ejecuta la app
    app.run(debug=True)
