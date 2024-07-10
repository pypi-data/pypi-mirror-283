from grpc_tools import protoc

def generate():
    protoc.main((
        '',
        '-I ./protos_finance --python_out=./  --grpc_python_out=. ./protos_finance/health.proto'
    ))

generate()

if __name__ == '__main__':

    print('start-----1')
    generate()
    # print("python -m grpc_tools.protoc -I./protos_finance --python_out=./ --grpc_python_out=. ./protos_finance/finance/reqData.proto ")







