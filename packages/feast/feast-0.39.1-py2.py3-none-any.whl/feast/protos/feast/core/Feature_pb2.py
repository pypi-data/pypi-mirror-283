# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: feast/core/Feature.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from feast.protos.feast.types import Value_pb2 as feast_dot_types_dot_Value__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18\x66\x65\x61st/core/Feature.proto\x12\nfeast.core\x1a\x17\x66\x65\x61st/types/Value.proto\"\xc3\x01\n\rFeatureSpecV2\x12\x0c\n\x04name\x18\x01 \x01(\t\x12/\n\nvalue_type\x18\x02 \x01(\x0e\x32\x1b.feast.types.ValueType.Enum\x12\x31\n\x04tags\x18\x03 \x03(\x0b\x32#.feast.core.FeatureSpecV2.TagsEntry\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42Q\n\x10\x66\x65\x61st.proto.coreB\x0c\x46\x65\x61tureProtoZ/github.com/feast-dev/feast/go/protos/feast/coreb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'feast.core.Feature_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\020feast.proto.coreB\014FeatureProtoZ/github.com/feast-dev/feast/go/protos/feast/core'
  _globals['_FEATURESPECV2_TAGSENTRY']._loaded_options = None
  _globals['_FEATURESPECV2_TAGSENTRY']._serialized_options = b'8\001'
  _globals['_FEATURESPECV2']._serialized_start=66
  _globals['_FEATURESPECV2']._serialized_end=261
  _globals['_FEATURESPECV2_TAGSENTRY']._serialized_start=218
  _globals['_FEATURESPECV2_TAGSENTRY']._serialized_end=261
# @@protoc_insertion_point(module_scope)
