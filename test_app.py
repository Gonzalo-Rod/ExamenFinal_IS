import unittest
from messages import app, BD 


class TestMessages(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    # Caso de éxito: Obtener los contactos de un usuario existente
    def test_ListContactos(self):
        response = self.client.get('/mensajes/contactos?mialias=GRodriguez')
        self.assertEqual(response.status_code, 200)
        self.assertIn("PCesar", response.json)
    
    # Caso de éxito: Agregar un contacto nuevo a un usuario existente
    def test_AddContactos(self):
        response = self.client.post(
            '/mensajes/contactos/GRodriguez',
            json={"contacto": "NU", "nombre": "Nuevo Usuario"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("mensaje", response.json)
        self.assertEqual(response.json["mensaje"], "Contacto agregado exitosamente")

    # Caso de éxito: Enviar un mensaje entre usuarios existentes
    def test_SendMensaje(self):
        
        response = self.client.post(
            '/mensajes/enviar',
            json={
                "usuario": "GRodriguez",
                "contacto": "PCesar",
                "mensaje": "Hola Cesar"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["mensaje"], "Mensaje enviado exitosamente")

    # Caso de éxito: Obtener mensajes recibidos de un usuario
    def test_ListarMensajes(self):
        self.client.post('/mensajes/enviar', json={
            "usuario": "GRodriguez",
            "contacto": "PCesar",
            "mensaje": "Hola Cesar"
        })
        response = self.client.get('/mensajes/recibidos?mialias=PCesar')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json), 0)




    # Caso de error: Usuario no encontrado al obtener contactos
    def test_ContactoNoEncontrado(self):
        response = self.client.get('/mensajes/contactos?mialias=NotExist')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)

    # Caso de error: Intentar agregar un contacto que ya existe
    def test_ContactoExistente(self):
        response = self.client.post(
            '/mensajes/contactos/GRodriguez',
            json={"contacto": "PCesar", "nombre": "Cesar"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("mensaje", response.json)

    # Caso de error: Enviar mensaje a un contacto no registrado
    def test_MensajeAContacto(self):
        response = self.client.post(
            '/mensajes/enviar',
            json={
                "usuario": "GRodriguez",
                "contacto": "NoEnLista",
                "mensaje": "Mensaje de prueba"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "El contacto no está en la lista de contactos")



if __name__ == '__main__':
    unittest.main()
