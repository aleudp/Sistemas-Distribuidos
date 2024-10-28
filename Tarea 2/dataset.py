import pandas as pd
import random
import os

# Load the original dataset from the script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))
input_filename = os.path.join(script_directory, 'Online Sales Data.csv')
df = pd.read_csv(input_filename)

# Keep only "Product Name" and "Unit Price" columns
df = df[['Product Name', 'Unit Price']]

# Lists of data for generating random values
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

# Function to generate a random email
def generate_random_email():
    name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=7))
    domain = random.choice(email_domains)
    return f'{name}@{domain}'

# Function to create dataset with specified number of rows
def create_dataset(size, filename):
    sample_df = df.sample(n=size, replace=True).reset_index(drop=True)
    sample_df['ID'] = range(1, size + 1)
    sample_df['Payment Gateway'] = [random.choice(payment_gateways) for _ in range(size)]
    sample_df['Card Brand'] = [random.choice(card_brands) for _ in range(size)]
    sample_df['Bank'] = [random.choice(banks) for _ in range(size)]
    sample_df['Region'] = [random.choice(regions) for _ in range(size)]
    sample_df['Address'] = [random.choice(addresses) for _ in range(size)]
    sample_df['Email'] = [generate_random_email() for _ in range(size)]

    # Save file in the grpc_server directory inside the script's location
    output_directory = os.path.join(script_directory, 'grpc_server')
    output_path = os.path.join(output_directory, filename)
    
    sample_df.to_csv(output_path, index=False)
    print(f"Dataset with {size} rows saved as {output_path}.")

# Generate datasets of different sizes in the grpc_server directory
create_dataset(1000, 'ds_low.csv')
create_dataset(10000, 'ds_medium.csv')
create_dataset(100000, 'ds_high.csv')
