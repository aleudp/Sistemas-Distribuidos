import grpc
import psycopg2
import redis
from concurrent import futures
import dns_pb2_grpc
import dns_pb2
import subprocess

# Conectar a PostgreSQL
def connect_postgres():
    conn = psycopg2.connect(
        host="postgres",
        database="dns_cache",
        user="user",
        password="password"
    )
    return conn

# Conectar a Redis
def connect_redis():
    r = redis.StrictRedis(host='redis', port=6379, decode_responses=True)
    return r

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
            self.cache.set(domain, ip)
            # Registrar la consulta en PostgreSQL
            cursor = self.db_conn.cursor()
            cursor.execute("INSERT INTO dns_queries (domain, ip_address) VALUES (%s, %s)", (domain, ip))
            self.db_conn.commit()
            cursor.close()
        else:
            print(f"Cache HIT for {domain}")

        return dns_pb2.DNSResponse(ip=ip)

# Función para iniciar el servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dns_pb2_grpc.add_DNSResolverServicer_to_server(
        DNSResolverService(connect_redis(), connect_postgres()), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
