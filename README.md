# ExamenFinal_IS
# Integrantes 
## Michel Marcelo Jaramillo Alfaro
## Gonzalo Alonso Rodrigues Gutierrez


# Ejemplos de ENDPOINTS a utlizar 
### 1. Obtener Contactos
- **Endpoint:** `GET /mensajeria/contactos`
- **Ejemplo de petición:**
  ```bash
  curl -X GET "http://127.0.0.1:5000/mensajeria/contactos?mialias=GRodriguez"
  ```


### 2. Agregar Contacto
- **Endpoint:** `POST /mensajeria/contactos/<alias>`
- **Ejemplo de petición:**
  ```bash
  curl -X POST "http://127.0.0.1:5000/mensajeria/contactos/GRodriguez" \
  -H "Content-Type: application/json" \
  -d '{"contacto": "JNuevo", "nombre": "Nuevo Usuario"}'
  ```

### 3. Enviar Mensaje
- **Endpoint:** `POST /mensajeria/enviar`
- **Ejemplo de petición:**
  ```bash
  curl -X POST "http://127.0.0.1:5000/mensajeria/enviar" \
  -H "Content-Type: application/json" \
  -d '{"usuario": "GRodriguez", "contacto": "PEddison", "mensaje": "Hola, Eddison!"}'
  ```


### 4. Verificar Mensajes Recibidos
- **Endpoint:** `GET /mensajeria/recibidos`
- **Ejemplo de petición:**
  ```bash
  curl -X GET "http://127.0.0.1:5000/mensajeria/recibidos?mialias=PEddison"
  ```






# Pregunta 3 
# Implementación de Cambios en el Código

## Cambios Requeridos

### 1. Clases y Métodos

#### Validación del número máximo de contactos:
- Modificar el método `adicionar_contacto` para incluir una validación con un límite de cantidad de contactos que un usuario pueda tener.
- Agregar una constante global, como `MAX_CONTACTOS`, para definir el límite máximo.

#### Eliminación de contactos:
- Crear un endpoint `/mensajeria/contacto/<alias>/delete` (DELETE) para eliminar contactos específicos.
- Modificar la lista de contactos del usuario para mantener los mensajes previamente enviados.

#### Eliminación de usuarios:
- Crear un nuevo endpoint `/mensajeria/usuario/<alias>/delete` (DELETE) para eliminar usuarios.
- Al eliminar un usuario, mantener los mensajes existentes, pero evitar referencias a usuarios eliminados.



### 2. Nuevos Casos de Prueba

#### Casos de éxito:
- Validar que un contacto se pueda eliminar correctamente y que no aparezca en la lista de contactos.
- Verificar que un usuario se pueda eliminar y que los mensajes enviados sigan siendo accesibles.
- Probar que se pueden agregar contactos hasta alcanzar el límite máximo permitido.
- Verificar que un mensaje enviado a un contacto eliminado no genere errores.

#### Casos de error:
- Intentar agregar un contacto cuando se haya alcanzado el límite permitido.
- Intentar eliminar un contacto que no existe.
- Intentar eliminar un usuario que no existe.
- Acceder a los contactos o mensajes de un usuario eliminado.



### 3. Riesgo de Romper Funcionalidades Existentes

#### Riesgo:
- **Riesgo menor:** La implementación de nuevas validaciones y endpoints podría introducir errores si no son manejados adecuadamente, como usuarios eliminados o validaciones del límite de contactos.

#### Medidas de mitigación:
- Realizar pruebas unitarias exhaustivas con una cobertura completa.
- Revisar y validar las modificaciones para asegurar la compatibilidad con las funcionalidades existentes.
- Documentar los cambios realizados para facilitar el mantenimiento y la futura expansión del código.

