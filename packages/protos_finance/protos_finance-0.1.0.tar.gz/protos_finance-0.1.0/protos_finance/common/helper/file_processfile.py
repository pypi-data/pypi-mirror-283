import logging
import sys
from typing import Set, Iterator, Tuple
from contextlib import contextmanager

from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest, CodeGeneratorResponse



def process_file(
    proto_file: FileDescriptorProto, response: CodeGeneratorResponse
) -> None:
    options = str(proto_file.options).strip().replace("\n", ", ").replace('"', "")
    file = response.file.add()  # 向响应对象添加并返回一个输出的文件对象
    file.name = proto_file.name + ".json"  # 指定输出文件的名字
    # 指定输出文件的内容
    file.content = json.dumps(
        {
            "package": f"{proto_file.package}",  # protobuf 包名
            "filename": f"{proto_file.name}",    # protobuf 文件名
            "dependencies": list(proto_file.dependency),  # protobuf依赖
            "message_type": [MessageToDict(i) for i in proto_file.message_type],  # protobuf 定义的message
            "service": [MessageToDict(i) for i in proto_file.service],  # protobuf定义的service
            "public_dependency": list(proto_file.public_dependency),    # protobuf定义的依赖
            "enum_type": [MessageToDict(i) for i in proto_file.enum_type],  # protobuf定义的枚举值
            "extension": [MessageToDict(i) for i in proto_file.extension],  # protobuf定义的拓展
            "options": dict(item.split(": ") for item in options.split(", ") if options),  # protobuf定义的options
        },
        indent=2
    ) + "\r\n"


def main() -> None:
    with code_generation() as (request, response):
        # 获取protoc命令中指定的proto路径
        file_name_set: Set[str] = {i for i in request.file_to_generate}
        for proto_file in request.proto_file:
            if proto_file.name not in file_name_set:
                # 排除非开发者编写的proto文件，不做多余的解析
                continue
            process_file(proto_file, response)  # <----修改这里