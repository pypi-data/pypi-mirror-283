import logging
import sys
from typing import Set, Iterator, Tuple
from contextlib import contextmanager

from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest, CodeGeneratorResponse

# 初始化logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="[%(asctime)s %(levelname)s] %(message)s", datefmt="%y-%m-%d %H:%M:%S", level=logging.INFO
)

@contextmanager
def code_generation() -> Iterator[Tuple[CodeGeneratorRequest, CodeGeneratorResponse]]:
    """模仿mypy-protobuf的代码"""
    # 从程序的标准输入读取对应的数据到 CodeGeneratorRequest对象中
    request: CodeGeneratorResponse = CodeGeneratorRequest.FromString(sys.stdin.buffer.read())
    # 初始化 CodeGeneratorResponse 对象
    response: CodeGeneratorResponse = CodeGeneratorResponse()

    # 声明插件是支持版本为3的protobuf文件也可以使用`OPTIONAL`语法。
    # protoc程序默认是支持的，而插件则是默认不支持的，所以需要开启，避免执行出错。
    response.supported_features |= CodeGeneratorResponse.FEATURE_PROTO3_OPTIONAL

    yield request, response

    # 序列化response对象，并写入到标准输出中
    sys.stdout.buffer.write(response.SerializeToString())


def main() -> None:
    with code_generation() as (request, response):
        # 获取protoc命令中指定的proto路径，也就是开发者编写proto文件的集合
        file_name_set: Set[str] = {i for i in request.file_to_generate}
        for proto_file in request.proto_file:
            if proto_file.name not in file_name_set:
                # 排除非开发者编写的proto文件，不做多余的解析
                continue
            # 打印protobuf文件名
            logger.info(proto_file.name)





if __name__ == "__main__":
    main()