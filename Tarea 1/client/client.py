import grpc
import dns_pb2
import dns_pb2_grpc
import psycopg2
import time
from concurrent import futures

# Función para conectarse a PostgreSQL y obtener los primeros 50000 dominios
def get_domains_from_db():
    try:
        # Conexión a la base de datos PostgreSQL
        conn = psycopg2.connect(
            dbname="domains_db",
            user="user",
            password="password",
            host="postgres_memory",  # Cambia a 'postgres' si el cliente está en un contenedor separado
            port="5433"
        )
        cursor = conn.cursor()
        
        # Consulta para obtener los primeros 50000 dominios de la tabla 'domains'
        cursor.execute("SELECT domain FROM domains LIMIT 50000")
        domains = cursor.fetchall()
        return [domain[0] for domain in domains]  # Devuelve solo los nombres de dominio
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Función para resolver un dominio usando gRPC
def resolve_domain(stub, domain):
    response = stub.Resolve(dns_pb2.DNSRequest(domain=domain))
    print(f'{domain} resolved to {response.ip}')
    return response

# Función para generar tráfico de consultas DNS en paralelo
def generate_traffic(stub, domains):
    # Limitar a los primeros 50,000 dominios
    limited_domains = domains[:100]

    # Usar un ThreadPoolExecutor para ejecutar las consultas en paralelo
    with futures.ThreadPoolExecutor(max_workers=20) as executor:
        # Hacer una consulta por cada uno de los 50,000 dominios en paralelo
        futures_list = [executor.submit(resolve_domain, stub, domain) for domain in limited_domains]
        # Esperar a que se completen todas las consultas
        futures.wait(futures_list)
    
        # Repetir los primeros 25 dominios 999 veces cada uno (total de 1000 consultas por dominio) en paralelo
        first_25_domains = limited_domains[:25]
        for domain in first_25_domains:
            futures_list = [executor.submit(resolve_domain, stub, domain) for _ in range(2)]
            futures.wait(futures_list)  # Esperar a que todas las repeticiones de cada dominio terminen

# Función para intentar conectar con reintentos
def connect_with_retries(stub, max_retries=5, wait_time=5):
    retries = 0
    while retries < max_retries:
        try:
            # Intentar realizar una consulta de prueba para verificar la conexión
            response = stub.Resolve(dns_pb2.DNSRequest(domain="google.com"))
            print(f"Connection successful. google.com resolved to {response.ip}")
            return True
        except grpc.RpcError as e:
            print(f"Attempt {retries + 1} failed: {e}")
            retries += 1
            time.sleep(wait_time)
    print("Max retries reached, exiting.")
    return False

# Función principal
def main():
    # Conexión al servidor gRPC
    with grpc.insecure_channel('grpc_server:50051') as channel:
        stub = dns_pb2_grpc.DNSResolverStub(channel)

        # Reintentar la conexión al servidor gRPC
        if connect_with_retries(stub):
            # Obtener los dominios desde la base de datos PostgreSQL
            domains = get_domains_from_db()

            # Si se encontraron dominios, generar el tráfico
            if domains:
                generate_traffic(stub, domains)
            else:
                print("No se encontraron dominios en la base de datos.")
        else:
            print("No se pudo establecer conexión con el servidor gRPC.")

if __name__ == '__main__':
    main()

