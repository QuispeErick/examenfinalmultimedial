from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Cambia según tu configuración
    'database': 'hospital'
}

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Rutas para mostrar tablas
@app.route('/tabla/<tabla>', methods=['GET'])
def mostrar_tabla(tabla):
    if tabla not in ['Pacientes', 'Hospitalizaciones', 'Salas', 'TiposDiagnostico']:
        return jsonify({"error": "Tabla no válida"}), 400
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {tabla}")
        resultados = cursor.fetchall()
        return jsonify(resultados)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Ruta para obtener diagnósticos
@app.route('/diagnosticos', methods=['GET'])
def obtener_diagnosticos():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM TiposDiagnostico")
        diagnosticos = cursor.fetchall()
        return jsonify(diagnosticos)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtener datos de un paciente por ID
@app.route('/pacientes/<int:id>', methods=['GET'])
def obtener_paciente(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Pacientes WHERE id = %s", (id,))
        paciente = cursor.fetchone()
        if paciente:
            return jsonify(paciente)
        else:
            return jsonify({"error": "Paciente no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


# Página de gestión de pacientes
@app.route('/pacientes', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gestionar_pacientes():
    if request.method == 'GET':
        return render_template('pacientes.html')
    elif request.method == 'POST':
        # Lógica para crear paciente
        data = request.json
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Pacientes (nombre, apellido, diagnostico) VALUES (%s, %s, %s)",
                (data['nombre'], data['apellido'], data['diagnostico'])
            )
            conn.commit()
            return jsonify({"message": "Paciente creado"}), 201
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()
    elif request.method == 'PUT':
        # Lógica para actualizar paciente
        data = request.json
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Pacientes SET nombre=%s, apellido=%s, diagnostico=%s WHERE id=%s",
                (data['nombre'], data['apellido'], data['diagnostico'], data['id'])
            )
            conn.commit()
            return jsonify({"message": "Paciente actualizado"}), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()
    elif request.method == 'DELETE':
        # Lógica para eliminar paciente
        id = request.args.get('id')
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Pacientes WHERE id=%s", (id,))
            conn.commit()
            return jsonify({"message": "Paciente eliminado"}), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()


# Página de gestión de hospitalizaciones
@app.route('/hospitalizaciones', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gestionar_hospitalizaciones():
    if request.method == 'GET':
        # Renderiza el archivo HTML en lugar de devolver JSON
        return render_template('hospitalizaciones.html')

    elif request.method == 'POST':
        # Crear nueva hospitalización
        data = request.json
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Hospitalizaciones (fecha_alta, fecha_ingreso, paciente_id, sala_id) VALUES (%s, %s, %s, %s)",
                (data['fecha_alta'], data['fecha_ingreso'], data['paciente_id'], data['sala_id'])
            )
            conn.commit()
            return jsonify({"message": "Hospitalización creada"}), 201
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()

    elif request.method == 'PUT':
        # Actualizar hospitalización
        data = request.json
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Hospitalizaciones SET fecha_alta=%s, fecha_ingreso=%s, paciente_id=%s, sala_id=%s WHERE id=%s",
                (data['fecha_alta'], data['fecha_ingreso'], data['paciente_id'], data['sala_id'], data['id'])
            )
            conn.commit()
            return jsonify({"message": "Hospitalización actualizada"}), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()

    elif request.method == 'DELETE':
        # Eliminar hospitalización
        id = request.args.get('id')
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Hospitalizaciones WHERE id=%s", (id,))
            conn.commit()
            return jsonify({"message": "Hospitalización eliminada"}), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()

# Ruta para obtener salas
@app.route('/salas', methods=['GET'])
def obtener_salas():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Salas")
        salas = cursor.fetchall()
        return jsonify(salas)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/hospitalizaciones/<int:id>', methods=['GET'])
def obtener_hospitalizacion(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Hospitalizaciones WHERE id = %s", (id,))
        hospitalizacion = cursor.fetchone()

        if not hospitalizacion:
            return jsonify({"error": "Hospitalización no encontrada"}), 404

        return jsonify(hospitalizacion)
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
