import os
from flask import Flask, render_template
from dotenv import load_dotenv
import psycopg2

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener variables de entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_CONNECTION_NAME = os.getenv("DB_CONNECTION_NAME")

# Dirección IP pública de tu instancia de Cloud SQL
DB_HOST = '34.151.218.220'

# Construir cadena de conexión
conn_str = f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST}"

# Configurar la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'you-will-never-guess'
app.config['DEBUG'] = os.getenv('DEBUG') or True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Función para obtener los detalles de los productos desde la base de datos
def get_products():
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(conn_str)
        print("Conexión exitosa")

        # Crear un cursor para ejecutar consultas
        cursor = conn.cursor()

        # Ejecutar una consulta para obtener los detalles de los productos
        cursor.execute("SELECT id_producto, nombre_producto, descripcion, precio FROM Producto")

        # Obtener los resultados de la consulta
        products = cursor.fetchall()

        # Agregar la ruta de la imagen para cada producto (asumiendo que las imágenes tienen nombres como product1.jpg, product2.jpg, etc.)
        products_with_images = []
        for product in products:
            product_id = product[0]
            image_path = f'images/products/product{product_id}.jpg'
            product_with_image = product + (image_path,)
            products_with_images.append(product_with_image)

        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()

        return products_with_images
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None


@app.route('/')
def index():
    # Obtener los detalles de todos los productos desde la base de datos
    all_products = get_products()

    # Dividir los productos según las secciones: cuidado facial, destacados y colecciones
    facial_care_products = all_products[:6]
    featured_products = all_products[6:9]
    collection_products = all_products[9:12]

    return render_template('index.html', facial_care_products=facial_care_products, 
                           featured_products=featured_products, collection_products=collection_products)

if __name__ == "__main__":
    # Iniciar el servidor Flask
    app.run(debug=True)





