import grpc
import order_pb2
import order_pb2_grpc
import pandas as pd

def place_order(stub, order):
    try:
        response = stub.PlaceOrder(order_pb2.OrderRequest(
            id=order['ID'],
            product_name=order['Product Name'],
            price=order['Unit Price'],
            payment_method=order['Payment Gateway'],
            card_brand=order['Card Brand'],
            bank=order['Bank'],
            region=order['Region'],
            address=order['Address'],
            email=order['Email']
        ))
        print(f"Order status: {response.status}")
    except grpc.RpcError as e:
        print(f"gRPC failed with error: {e.details()} (code: {e.code()})")

def run():
    # Connect to the gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = order_pb2_grpc.OrderServiceStub(channel)

        # Read the resulting CSV file
        df = pd.read_csv('ds.csv')

        # Iterate over each row in the DataFrame and send the order
        for _, row in df.iterrows():
            order = {
                "ID": row['ID'],
                "Product Name": row['Product Name'],
                "Unit Price": row['Unit Price'],
                "Payment Gateway": row['Payment Gateway'],
                "Card Brand": row['Card Brand'],
                "Bank": row['Bank'],
                "Region": row['Region'],
                "Address": row['Address'],
                "Email": row['Email']
            }
            place_order(stub, order)

if __name__ == "__main__":
    run()

