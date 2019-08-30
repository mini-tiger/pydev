 1.
 pip install grpcio
 pip install grpcio-tools
 
 2. 生成 hello_pb2*.py
 C:\pydev\grpc\hello> python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. ./hello.proto
 
 3.先运行server.py
 在运行client.py