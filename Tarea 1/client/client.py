import grpc
import dns_pb2
import dns_pb2_grpc
import random

# Lista de dominios de prueba
domains = ["example.com", "google.com", "github.com", "stackoverflow.com"]

def generate_traffic():
    with grpc.insecure_channel('grpc_server:50051') as channel:
        stub = dns_pb2_grpc.DNSResolverStub(channel)
        for _ in range(10):
            domain = random.choice(domains)
            response = stub.Resolve(dns_pb2.DNSRequest(domain=domain))
            print(f'{domain} resolved to {response.ip}')

if __name__ == '__main__':
    generate_traffic()
