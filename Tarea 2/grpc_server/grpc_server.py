from concurrent import futures
import grpc
import order_pb2
import order_pb2_grpc
from kafka import KafkaProducer
import json

class OrderService(order_pb2_grpc.OrderServiceServicer):
    def PlaceOrder(self, request, context):
        # Configure the Kafka producer
        try:
            producer = KafkaProducer(
                bootstrap_servers=['localhost:9093', 'localhost:9095', 'localhost:9097'],  # Use mapped ports in Docker
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )

            # Create the message to send
            message = {
                "product_name": request.product_name,
                "price": request.price,
                "ID": request.id,
                "payment_method": request.payment_method,
                "card_brand": request.card_brand,
                "bank": request.bank,
                "region": request.region,
                "address": request.address,
                "email": request.email
            }

            # Send the message to the "Procesando" topic
            producer.send('Procesando', value=message)
            producer.flush()
            producer.close()

            # Return a successful response
            return order_pb2.OrderResponse(status="Order received and sent to 'Procesando'")
        except Exception as e:
            # Set error details for the gRPC context
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
            return order_pb2.OrderResponse(status="Order failed")

def serve():
    # Set up the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server is running on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

