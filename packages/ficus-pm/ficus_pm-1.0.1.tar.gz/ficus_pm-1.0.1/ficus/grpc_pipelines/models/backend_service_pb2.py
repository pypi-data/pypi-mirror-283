# -*- coding: utf-8 -*-

# Generated by the protocol buffer compiler.  DO NOT EDIT!

# source: backend_service.proto

"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor

from google.protobuf import descriptor_pool as _descriptor_pool

from google.protobuf import symbol_database as _symbol_database

from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)



_sym_db = _symbol_database.Default()





import ficus.grpc_pipelines.models.pipelines_and_context_pb2 as pipelines__and__context__pb2

import ficus.grpc_pipelines.models.util_pb2 as util__pb2

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2





DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x62\x61\x63kend_service.proto\x12\x05\x66icus\x1a\x1bpipelines_and_context.proto\x1a\nutil.proto\x1a\x1bgoogle/protobuf/empty.proto\"f\n\x1aGrpcGetContextValueRequest\x12$\n\x0b\x65xecutionId\x18\x02 \x01(\x0b\x32\x0f.ficus.GrpcGuid\x12\"\n\x03key\x18\x01 \x01(\x0b\x32\x15.ficus.GrpcContextKey\"y\n\x1cGrpcPipelineExecutionRequest\x12%\n\x08pipeline\x18\x01 \x01(\x0b\x32\x13.ficus.GrpcPipeline\x12\x32\n\x0einitialContext\x18\x02 \x03(\x0b\x32\x1a.ficus.GrpcContextKeyValue\"\xd8\x01\n\x1fGrpcPipelinePartExecutionResult\x12\x35\n\x0b\x66inalResult\x18\x01 \x01(\x0b\x32\x1e.ficus.GrpcPipelineFinalResultH\x00\x12;\n\x12pipelinePartResult\x18\x02 \x01(\x0b\x32\x1d.ficus.GrpcPipelinePartResultH\x00\x12\x37\n\nlogMessage\x18\x03 \x01(\x0b\x32!.ficus.GrpcPipelinePartLogMessageH\x00\x42\x08\n\x06result\"-\n\x1aGrpcPipelinePartLogMessage\x12\x0f\n\x07message\x18\x01 \x01(\t\"r\n\x16GrpcPipelinePartResult\x12\x39\n\rcontextValues\x18\x01 \x03(\x0b\x32\".ficus.GrpcContextValueWithKeyName\x12\x1d\n\x04uuid\x18\x02 \x01(\x0b\x32\x0f.ficus.GrpcUuid\"W\n\x1bGrpcContextValueWithKeyName\x12\x10\n\x08key_name\x18\x01 \x01(\t\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.ficus.GrpcContextValue\"a\n\x17GrpcPipelineFinalResult\x12\"\n\x07success\x18\x01 \x01(\x0b\x32\x0f.ficus.GrpcGuidH\x00\x12\x0f\n\x05\x65rror\x18\x02 \x01(\tH\x00\x42\x11\n\x0f\x65xecutionResult\"l\n\x19GrpcGetContextValueResult\x12(\n\x05value\x18\x01 \x01(\x0b\x32\x17.ficus.GrpcContextValueH\x00\x12\x0f\n\x05\x65rror\x18\x02 \x01(\tH\x00\x42\x14\n\x12\x63ontextValueResult2\x8e\x02\n\x12GrpcBackendService\x12`\n\x0f\x45xecutePipeline\x12#.ficus.GrpcPipelineExecutionRequest\x1a&.ficus.GrpcPipelinePartExecutionResult0\x01\x12V\n\x0fGetContextValue\x12!.ficus.GrpcGetContextValueRequest\x1a .ficus.GrpcGetContextValueResult\x12>\n\x13\x44ropExecutionResult\x12\x0f.ficus.GrpcGuid\x1a\x16.google.protobuf.Emptyb\x06proto3')



_globals = globals()

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)

_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'backend_service_pb2', _globals)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None

  _globals['_GRPCGETCONTEXTVALUEREQUEST']._serialized_start=102

  _globals['_GRPCGETCONTEXTVALUEREQUEST']._serialized_end=204

  _globals['_GRPCPIPELINEEXECUTIONREQUEST']._serialized_start=206

  _globals['_GRPCPIPELINEEXECUTIONREQUEST']._serialized_end=327

  _globals['_GRPCPIPELINEPARTEXECUTIONRESULT']._serialized_start=330

  _globals['_GRPCPIPELINEPARTEXECUTIONRESULT']._serialized_end=546

  _globals['_GRPCPIPELINEPARTLOGMESSAGE']._serialized_start=548

  _globals['_GRPCPIPELINEPARTLOGMESSAGE']._serialized_end=593

  _globals['_GRPCPIPELINEPARTRESULT']._serialized_start=595

  _globals['_GRPCPIPELINEPARTRESULT']._serialized_end=709

  _globals['_GRPCCONTEXTVALUEWITHKEYNAME']._serialized_start=711

  _globals['_GRPCCONTEXTVALUEWITHKEYNAME']._serialized_end=798

  _globals['_GRPCPIPELINEFINALRESULT']._serialized_start=800

  _globals['_GRPCPIPELINEFINALRESULT']._serialized_end=897

  _globals['_GRPCGETCONTEXTVALUERESULT']._serialized_start=899

  _globals['_GRPCGETCONTEXTVALUERESULT']._serialized_end=1007

  _globals['_GRPCBACKENDSERVICE']._serialized_start=1010

  _globals['_GRPCBACKENDSERVICE']._serialized_end=1280

# @@protoc_insertion_point(module_scope)
