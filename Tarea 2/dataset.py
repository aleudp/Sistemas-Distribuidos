import pandas as pd
import random

# Cargar el dataset original
df = pd.read_csv('/home/alejandro/Documents/Tarea 2/Online Sales Data.csv')

# Mantener solo las columnas "Product Name" y "Unit Price"
df = df[['Product Name', 'Unit Price']]

# Listas de datos para generar valores aleatorios
payment_gateways = ['MercadoPago', 'Webpay', 'EtPay', 'Kiphu']
card_brands = ['VISA', 'Mastercard', 'AMEX']
banks = ['Santander', 'Banco de Chile', 'Banco Estado', 'Banco BCI', 'Banco Falabella']
regions = [
    'Región de Arica y Parinacota', 'Región de Tarapacá', 'Región de Antofagasta', 
    'Región de Atacama', 'Región de Coquimbo', 'Región de Valparaíso', 
    'Región Metropolitana de Santiago', 'Región del Libertador General Bernardo O\'Higgins', 
    'Región del Maule', 'Región de Ñuble', 'Región del Biobío', 
    'Región de La Araucanía', 'Región de Los Ríos', 'Región de Los Lagos', 
    'Región de Aysén del General Carlos Ibáñez del Campo', 'Región de Magallanes y de la Antártica Chilena'
]
addresses = [
    'Av. Siempre Viva 742', 'Calle Falsa 123', 'Los Alerces 456', 
    'La Florida 789', 'Camino del Inca 1010', 'Providencia 234', 
    'Gran Avenida 567', 'Paseo Ahumada 890', 'Av. O\'Higgins 678',
    'Plaza Italia 111', 'Cerro Alegre 222', 'Puerto Varas 333',
    'Villarrica 444', 'Valdivia 555', 'La Serena 666'
]
email_domains = ['example.com', 'email.com', 'mail.com', 'test.com', 'random.org', 'fake.co']

# Función para generar un correo electrónico aleatorio
def generate_random_email():
    name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=7))
    domain = random.choice(email_domains)
    return f'{name}@{domain}'

# Generar nuevas columnas con datos aleatorios
df['ID'] = range(1, len(df) + 1)  # Añadir ID único y correlativo
df['Payment Gateway'] = [random.choice(payment_gateways) for _ in range(len(df))]
df['Card Brand'] = [random.choice(card_brands) for _ in range(len(df))]
df['Bank'] = [random.choice(banks) for _ in range(len(df))]
df['Region'] = [random.choice(regions) for _ in range(len(df))]
df['Address'] = [random.choice(addresses) for _ in range(len(df))]
df['Email'] = [generate_random_email() for _ in range(len(df))]

# Guardar el nuevo dataset modificado
df.to_csv('ds.csv', index=False)

print("Dataset modificado y guardado con éxito.")

