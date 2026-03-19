from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
# Aquí es donde ocurre la magia del diseño
api = Api(app, version='1.0', title='API de Tareas de Pau',
    description='Una API completa con Swagger',)

ns = api.namespace('tareas', description='Operaciones de tareas')

# Definimos cómo se ve una tarea para Swagger
tarea_model = api.model('Tarea', {
    'id': fields.Integer(readOnly=True, description='El identificador único'),
    'titulo': fields.String(required=True, description='Título de la tarea'),
    'descripcion': fields.String(description='Detalles de la tarea'),
    'estado': fields.String(description='Pendiente/Completado')
})

# Datos de prueba (puedes usar tu DB aquí)
TAREAS = [{'id': 1, 'titulo': 'Aprender Swagger', 'descripcion': 'Ver los colores', 'estado': 'pendiente'}]

@ns.route('/')
class ListaTareas(Resource):
    @ns.marshal_list_with(tarea_model)
    def get(self):
        '''Muestra todas las tareas'''
        return TAREAS

    @ns.expect(tarea_model)
    def post(self):
        '''Crea una nueva tarea'''
        return {'mensaje': 'Tarea creada'}, 201

@ns.route('/<int:id>')
class TareaIndividual(Resource):
    def delete(self, id):
        '''Elimina una tarea'''
        return {'mensaje': 'Eliminado'}, 204
    
    @ns.expect(tarea_model)
    @ns.marshal_with(tarea_model)
    def put(self, id):
            '''Actualizar una tarea existente (PUT naranja)'''
            for t in TAREAS:
                if t['id'] == id:
                    # api.payload es lo que escribes en Swagger
                    t.update(api.payload) 
                    return t
            api.abort(404)

if __name__ == '__main__':
    app.run(debug=True)