import grpc
import psycopg2
import redis
from concurrent import futures
import dns_pb2_grpc
import dns_pb2
import subprocess
import os

# Configuración de particiones y tipo de partición
PARTITION_COUNT = 1  # Máximo de 8 particiones
PARTITION_TYPE = 'hash'  # Puede ser 'hash' o 'range'

# Conectar a PostgreSQL
def connect_postgres():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        database=os.getenv("POSTGRES_DB", "dns_cache"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password")
    )
    print("Conexión exitosa a PostgreSQL")
    return conn

# Función para obtener el cliente Redis según el número de particiones
def get_redis_client(partition_type, partition_count):
    redis_clients = []
    for i in range(1, partition_count + 1):
        redis_clients.append(redis.StrictRedis(host=f'redis{i}', port=6379, decode_responses=True))
    print(f"Conexión a {partition_count} instancias de Redis completada.")
    return redis_clients

# Función para obtener el índice de partición basado en el tipo de partición
def get_partition_index(domain, partition_type, partition_count):
    if partition_type == 'hash':
        # Usar hash del dominio para distribuir entre particiones
        return hash(domain) % partition_count
    elif partition_type == 'range':
        # Usar un enfoque basado en la suma de los valores ASCII de los caracteres del dominio
        return sum([ord(c) for c in domain]) % partition_count
    else:
        raise ValueError("Invalid partition type. Use 'hash' or 'range'.")

# Función para resolver DNS usando DIG
def resolve_dns(domain):
    result = subprocess.run(['dig', '+short', domain], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip()

# Clase del servicio gRPC
class DNSResolverService(dns_pb2_grpc.DNSResolverServicer):
    def __init__(self, db_conn, partition_type, partition_count):
        self.db_conn = db_conn
        self.redis_clients = get_redis_client(partition_type, partition_count)
        self.partition_type = partition_type
        self.partition_count = partition_count

    def Resolve(self, request, context):
        domain = request.domain
        # Obtener el índice de partición
        partition_index = get_partition_index(domain, self.partition_type, self.partition_count)
        redis_client = self.redis_clients[partition_index]
        
        # Intentar obtener la IP desde Redis
        ip = redis_client.get(domain)
        if ip:
            print(f"Cache HIT for {domain} on partition {partition_index}")
        else:
            print(f"Cache MISS for {domain} on partition {partition_index}")
            ip = resolve_dns(domain)  # Resuelve usando DIG
            
            if ip:  # Si la IP es válida, almacenarla en Redis
                redis_client.set(domain, ip)

        # Registrar la consulta en PostgreSQL, incluyendo el número de partición
        cursor = self.db_conn.cursor()
        cursor.execute("""
            INSERT INTO dns_queries (domain, ip_address, partition_number) 
            VALUES (%s, %s, %s)
        """, (domain, ip if ip else 'No IP found', partition_index))
        self.db_conn.commit()
        cursor.close()

        return dns_pb2.DNSResponse(ip=ip if ip else "No IP found")

# Función para iniciar el servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dns_pb2_grpc.add_DNSResolverServicer_to_server(
        DNSResolverService(connect_postgres(), PARTITION_TYPE, PARTITION_COUNT), server
    )
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC iniciado en el puerto 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

