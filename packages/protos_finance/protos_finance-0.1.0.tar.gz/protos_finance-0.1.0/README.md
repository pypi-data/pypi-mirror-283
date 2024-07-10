# [grpc_finance_common](grpc_finance_common)



# 生成文件命令
python -m grpc_tools.protoc   --python_out=./   --grpc_python_out=./   -I protos $(find ./protos -name '*.proto')


python -m grpc_tools.protoc   --python_out=./grpc_finance_common   --grpc_python_out=./grpc_finance_common   -I    ./ protos/finance/health.proto 

python -m grpc_tools.protoc -I protos --python_out=grpc_finance_common --pyi_out=grpc_finance_common/protos --grpc_python_out=grpc_finance_common/protos/finance/health.proto



python -m grpc_tools.protoc   -I. --python_out=.


