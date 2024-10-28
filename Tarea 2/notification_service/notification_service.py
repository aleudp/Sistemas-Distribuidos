from kafka import KafkaConsumer
import json
import threading
import smtplib
from email.message import EmailMessage
import ssl
from datetime import datetime

# Email service class
class EmailService:
    def __init__(self, remitente, contraseña):
        self.remitente = remitente
        self.contraseña = contraseña
        self.smtp_server = "smtp.gmail.com"
        self.port = 465
        self.context = ssl.create_default_context()

    def enviar_correo(self, destinatario, asunto, cuerpo):
        em = EmailMessage()
        em["From"] = self.remitente
        em["To"] = destinatario
        em["Subject"] = asunto
        em.set_content(cuerpo)

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as smtp:
                smtp.login(self.remitente, self.contraseña)
                smtp.sendmail(self.remitente, destinatario, em.as_string())
                print(f"[SUCCESS] Email sent to {destinatario}")
        except smtplib.SMTPAuthenticationError:
            print(f"[ERROR] Authentication failed when sending email to {destinatario}. Check credentials.")
        except Exception as e:
            print(f"[ERROR] Failed to send email to {destinatario}: {e}")

# Function to send email notification based on the state
def enviar_notificacion(pedido, estado):
    remitente = "correodetareas11.9@gmail.com"
    contraseña = "wssw jgch kfyc fzyr"  # Securely store this password
    
    email_service = EmailService(remitente, contraseña)
    destinatario = pedido["email"]
    asunto = f"Notificación de cambio de estado: {estado}"
    cuerpo = (
        f"Estimado cliente,\n\n"
        f"Su pedido con ID {pedido['ID']} ha cambiado al estado: {estado}.\n\n"
        f"Detalles del pedido:\n"
        f"- Producto: {pedido['product_name']}\n"
        f"- Precio: ${pedido['price']}\n"
        f"- Método de pago: {pedido['payment_method']}\n"
        f"- Marca de tarjeta: {pedido['card_brand']}\n"
        f"- Banco: {pedido['bank']}\n"
        f"- Región: {pedido['region']}\n"
        f"- Dirección: {pedido['address']}\n\n"
        f"Gracias por su preferencia.\n"
    )
    email_service.enviar_correo(destinatario, asunto, cuerpo)

# Consumer function for each topic
def start_consumer(topic_name):
    kafka_brokers = ["kafka1:9092", "kafka2:9092", "kafka3:9092"]

    try:
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=kafka_brokers,
            group_id=f"notification-{topic_name}",
            value_deserializer=lambda m: json.loads(m.decode("utf-8"))
        )
        print(f"[SUCCESS] Notification consumer connected for topic: {topic_name}")
    except Exception as e:
        print(f"[ERROR] Could not connect to Kafka for topic {topic_name}: {e}")
        return

    # Continuously consume messages and send notifications
    for message in consumer:
        doc = message.value
        print(f"[INFO] Consuming message from topic '{topic_name}' for product ID: {doc['ID']}")
        enviar_notificacion(doc, topic_name)

# Start a consumer for each topic
def start_notification_service():
    topics = ["Procesando", "Preparacion", "Finalizado", "Enviado", "Entregado"]
    
    for topic in topics:
        thread = threading.Thread(target=start_consumer, args=(topic,))
        thread.start()
        print(f"[INFO] Thread started for notification on topic: {topic}")

if __name__ == "__main__":
    print("[INFO] Starting notification service...")
    start_notification_service()
