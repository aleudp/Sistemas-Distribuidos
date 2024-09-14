import grpc
import psycopg2
import redis
import time
from concurrent import futures
import dns_pb2_grpc
import dns_pb2
import subprocess

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

# Intentar reconectar a Redis hasta que esté disponible
def connect_redis():
    while True:
        try:
            r = redis.StrictRedis(host='redis', port=6379, decode_responses=True)
            r.ping()  # Comprobar si Redis está listo
            print("Conexión exitosa a Redis")
            return r
        except redis.ConnectionError:
            print("Redis no está listo. Reintentando en 5 segundos...")
            time.sleep(5)

# Función para resolver DNS usando DIG
def resolve_dns(domain):
    result = subprocess.run(['dig', '+short', domain], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip()

# Clase del servicio gRPC
class DNSResolverService(dns_pb2_grpc.DNSResolverServicer):
    def __init__(self, cache, db_conn):
        self.cache = cache
        self.db_conn = db_conn

    def Resolve(self, request, context):
        domain = request.domain
        ip = self.cache.get(domain)

        if not ip:
            print(f"Cache MISS for {domain}")
            ip = resolve_dns(domain)  # Resuelve usando DIG

            if ip:  # Si la IP es válida, almacenarla
                self.cache.set(domain, ip)
                # Registrar la consulta en PostgreSQL solo si hay una IP
                cursor = self.db_conn.cursor()
                cursor.execute("INSERT INTO dns_queries (domain, ip_address) VALUES (%s, %s)", (domain, ip))
                self.db_conn.commit()
                cursor.close()
            else:
                print(f"No se pudo resolver {domain}, no se almacenará en Redis ni en PostgreSQL.")
        else:
            print(f"Cache HIT for {domain}")

        return dns_pb2.DNSResponse(ip=ip if ip else "No IP found")

# Función para iniciar el servidor gRPC
def serve():
    # Conectar a Redis y PostgreSQL con lógica de reconexión
    cache = connect_redis()
    db_conn = connect_postgres()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dns_pb2_grpc.add_DNSResolverServicer_to_server(
        DNSResolverService(cache, db_conn), server
    )
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC iniciado en el puerto 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

