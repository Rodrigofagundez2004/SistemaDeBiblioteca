from .database import Database
import mysql.connector
import hashlib 
import secrets 
class LoginModel:
    def verificar_login(self, email, password):
        # En esta funcion vamos a verificar las credenciales del login
        db = Database()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""SELECT l.correo, l.contraseña, p.ci, p.nombre, p.apellido
                              FROM login l
                              JOIN participante p ON l.correo = p.email
                              WHERE l.correo = %s""", (email,))
            usuario = cursor.fetchone()
            if not usuario:
                return False, "Usuario no encontrado"
            #Verifico la contraseña 
            if self._verificar_contraseñ(password, usuario['contraseña']):
                #Credenciales correctas
                return True, {
                    "ci": usuario['ci'],
                    "nombre": usuario['nombre'],
                    "apellido": usuario['apellido'],
                    "email": usuario['correo']
                }
            else:
                return False, "Contraseña incorrecta"
        except Exception as e:
            return False, f"Error al verificar login: {e}" 
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    def crear_usuario(self, ci, email, password):
        #Crear un nuevo usuario en login
        db = Database()
        conn = db.get_connection()
        cursor = None 

        try:
            cursor = conn.cursor()
            #Hash de la password
            password_hash = self._hash_password(password)
            #Insertamos el login
            cursor.execute("INSERT INTO login (correo, contraseña) VALUES (%s, %s)", (email, password_hash))
            conn.commit()
            return True, "Usuario creado de forma exitosa"
        except mysql.connector.IntegrityError as e:
            return False, "Error: ya existe un usuario con ese email"
        except Exception as e:
            return False , f"Error al crear usuario: {e}"
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    def _hash_password(self, password):
        salt = "Mejor_MasterYi_BR"     #Hasheo mi password con este salt
        return hashlib.sha256((password + salt).encode()).hexdigest() #Uso la libreria hashlib 
    def _verificar_contraseñ(self, password, password_hash):
        return self._hash_password(password) == password_hash