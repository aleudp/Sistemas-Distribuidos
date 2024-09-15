import grpc
import psycopg2
import redis
import time
from concurrent import futures
import dns_pb2_grpc
import dns_pb2
import subprocess

# Configuración de particiones y tipo de partición
PARTITION_COUNT = 4 # Máximo de 8 particiones
PARTITION_TYPE = 'range' # Puede ser 'hash' o 'range'

# Intentar reconectar a PostgreSQL hasta que esté disponible
def connect_postgres():
    while True:
        try:
            conn = psycopg2.connect(
                host="postgres",
                database="dns_cache",
                user="user",
                password="password"
            )
            print("Conexión exitosa a PostgreSQL")
            return conn
        except psycopg2.OperationalError:
            print("PostgreSQL no está listo. Reintentando en 5 segundos...")
            time.sleep(5)

# Función para obtener el cliente Redis según el número de particiones
def get_redis_client(partition_count):
    redis_clients = []
    for i in range(1, partition_count + 1):
        redis_clients.append(redis.StrictRedis(host=f'redis{i}', port=6379, decode_responses=True))
    return redis_clients

# Función para obtener el índice de partición basado en el tipo de partición
def get_partition_index(domain, partition_type, partition_count):
    if partition_type == 'hash':
        return hash(domain) % partition_count
    elif partition_type == 'range':
        # Asume que el dominio se distribuye equitativamente
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
        self.redis_clients = get_redis_client(partition_count)
        self.partition_type = partition_type
        self.partition_count = partition_count

    def Resolve(self, request, context):
        domain = request.domain
        partition_index = get_partition_index(domain, self.partition_type, self.partition_count)
        redis_client = self.redis_clients[partition_index]
        ip = redis_client.get(domain)

        if not ip:
            print(f"Cache MISS for {domain}")
            ip = resolve_dns(domain)  # Resuelve usando DIG

            if ip:  # Si la IP es válida, almacenarla
                print(f"Cache HIT for {domain} on partition {partition_index}")
                # Almacenar en el cliente de Redis correspondiente
                redis_client.set(domain, ip)
                # Registrar la consulta en PostgreSQL solo si hay una IP
                cursor = self.db_conn.cursor()
                cursor.execute("INSERT INTO dns_queries (domain, ip_address) VALUES (%s, %s)", (domain, ip))
                self.db_conn.commit()
                cursor.close()
            else:
                print(f"No se pudo resolver {domain}, no se almacenará en Redis ni en PostgreSQL.")
        #else:
            #print(f"Cache HIT for {domain} on partition {partition_index}")

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

