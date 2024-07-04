# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: feast/serving/ServingService.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from feast.protos.feast.types import Value_pb2 as feast_dot_types_dot_Value__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"feast/serving/ServingService.proto\x12\rfeast.serving\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x17\x66\x65\x61st/types/Value.proto\"\x1c\n\x1aGetFeastServingInfoRequest\".\n\x1bGetFeastServingInfoResponse\x12\x0f\n\x07version\x18\x01 \x01(\t\"E\n\x12\x46\x65\x61tureReferenceV2\x12\x19\n\x11\x66\x65\x61ture_view_name\x18\x01 \x01(\t\x12\x14\n\x0c\x66\x65\x61ture_name\x18\x02 \x01(\t\"\xfd\x02\n\x1aGetOnlineFeaturesRequestV2\x12\x33\n\x08\x66\x65\x61tures\x18\x04 \x03(\x0b\x32!.feast.serving.FeatureReferenceV2\x12H\n\x0b\x65ntity_rows\x18\x02 \x03(\x0b\x32\x33.feast.serving.GetOnlineFeaturesRequestV2.EntityRow\x12\x0f\n\x07project\x18\x05 \x01(\t\x1a\xce\x01\n\tEntityRow\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12O\n\x06\x66ields\x18\x02 \x03(\x0b\x32?.feast.serving.GetOnlineFeaturesRequestV2.EntityRow.FieldsEntry\x1a\x41\n\x0b\x46ieldsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12!\n\x05value\x18\x02 \x01(\x0b\x32\x12.feast.types.Value:\x02\x38\x01\"\x1a\n\x0b\x46\x65\x61tureList\x12\x0b\n\x03val\x18\x01 \x03(\t\"\xc8\x03\n\x18GetOnlineFeaturesRequest\x12\x19\n\x0f\x66\x65\x61ture_service\x18\x01 \x01(\tH\x00\x12.\n\x08\x66\x65\x61tures\x18\x02 \x01(\x0b\x32\x1a.feast.serving.FeatureListH\x00\x12G\n\x08\x65ntities\x18\x03 \x03(\x0b\x32\x35.feast.serving.GetOnlineFeaturesRequest.EntitiesEntry\x12\x1a\n\x12\x66ull_feature_names\x18\x04 \x01(\x08\x12T\n\x0frequest_context\x18\x05 \x03(\x0b\x32;.feast.serving.GetOnlineFeaturesRequest.RequestContextEntry\x1aK\n\rEntitiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12)\n\x05value\x18\x02 \x01(\x0b\x32\x1a.feast.types.RepeatedValue:\x02\x38\x01\x1aQ\n\x13RequestContextEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12)\n\x05value\x18\x02 \x01(\x0b\x32\x1a.feast.types.RepeatedValue:\x02\x38\x01\x42\x06\n\x04kind\"\xd2\x02\n\x19GetOnlineFeaturesResponse\x12\x42\n\x08metadata\x18\x01 \x01(\x0b\x32\x30.feast.serving.GetOnlineFeaturesResponseMetadata\x12G\n\x07results\x18\x02 \x03(\x0b\x32\x36.feast.serving.GetOnlineFeaturesResponse.FeatureVector\x12\x0e\n\x06status\x18\x03 \x01(\x08\x1a\x97\x01\n\rFeatureVector\x12\"\n\x06values\x18\x01 \x03(\x0b\x32\x12.feast.types.Value\x12,\n\x08statuses\x18\x02 \x03(\x0e\x32\x1a.feast.serving.FieldStatus\x12\x34\n\x10\x65vent_timestamps\x18\x03 \x03(\x0b\x32\x1a.google.protobuf.Timestamp\"V\n!GetOnlineFeaturesResponseMetadata\x12\x31\n\rfeature_names\x18\x01 \x01(\x0b\x32\x1a.feast.serving.FeatureList*[\n\x0b\x46ieldStatus\x12\x0b\n\x07INVALID\x10\x00\x12\x0b\n\x07PRESENT\x10\x01\x12\x0e\n\nNULL_VALUE\x10\x02\x12\r\n\tNOT_FOUND\x10\x03\x12\x13\n\x0fOUTSIDE_MAX_AGE\x10\x04\x32\xe6\x01\n\x0eServingService\x12l\n\x13GetFeastServingInfo\x12).feast.serving.GetFeastServingInfoRequest\x1a*.feast.serving.GetFeastServingInfoResponse\x12\x66\n\x11GetOnlineFeatures\x12\'.feast.serving.GetOnlineFeaturesRequest\x1a(.feast.serving.GetOnlineFeaturesResponseBZ\n\x13\x66\x65\x61st.proto.servingB\x0fServingAPIProtoZ2github.com/feast-dev/feast/go/protos/feast/servingb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'feast.serving.ServingService_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\023feast.proto.servingB\017ServingAPIProtoZ2github.com/feast-dev/feast/go/protos/feast/serving'
  _globals['_GETONLINEFEATURESREQUESTV2_ENTITYROW_FIELDSENTRY']._loaded_options = None
  _globals['_GETONLINEFEATURESREQUESTV2_ENTITYROW_FIELDSENTRY']._serialized_options = b'8\001'
  _globals['_GETONLINEFEATURESREQUEST_ENTITIESENTRY']._loaded_options = None
  _globals['_GETONLINEFEATURESREQUEST_ENTITIESENTRY']._serialized_options = b'8\001'
  _globals['_GETONLINEFEATURESREQUEST_REQUESTCONTEXTENTRY']._loaded_options = None
  _globals['_GETONLINEFEATURESREQUEST_REQUESTCONTEXTENTRY']._serialized_options = b'8\001'
  _globals['_FIELDSTATUS']._serialized_start=1560
  _globals['_FIELDSTATUS']._serialized_end=1651
  _globals['_GETFEASTSERVINGINFOREQUEST']._serialized_start=111
  _globals['_GETFEASTSERVINGINFOREQUEST']._serialized_end=139
  _globals['_GETFEASTSERVINGINFORESPONSE']._serialized_start=141
  _globals['_GETFEASTSERVINGINFORESPONSE']._serialized_end=187
  _globals['_FEATUREREFERENCEV2']._serialized_start=189
  _globals['_FEATUREREFERENCEV2']._serialized_end=258
  _globals['_GETONLINEFEATURESREQUESTV2']._serialized_start=261
  _globals['_GETONLINEFEATURESREQUESTV2']._serialized_end=642
  _globals['_GETONLINEFEATURESREQUESTV2_ENTITYROW']._serialized_start=436
  _globals['_GETONLINEFEATURESREQUESTV2_ENTITYROW']._serialized_end=642
  _globals['_GETONLINEFEATURESREQUESTV2_ENTITYROW_FIELDSENTRY']._serialized_start=577
  _globals['_GETONLINEFEATURESREQUESTV2_ENTITYROW_FIELDSENTRY']._serialized_end=642
  _globals['_FEATURELIST']._serialized_start=644
  _globals['_FEATURELIST']._serialized_end=670
  _globals['_GETONLINEFEATURESREQUEST']._serialized_start=673
  _globals['_GETONLINEFEATURESREQUEST']._serialized_end=1129
  _globals['_GETONLINEFEATURESREQUEST_ENTITIESENTRY']._serialized_start=963
  _globals['_GETONLINEFEATURESREQUEST_ENTITIESENTRY']._serialized_end=1038
  _globals['_GETONLINEFEATURESREQUEST_REQUESTCONTEXTENTRY']._serialized_start=1040
  _globals['_GETONLINEFEATURESREQUEST_REQUESTCONTEXTENTRY']._serialized_end=1121
  _globals['_GETONLINEFEATURESRESPONSE']._serialized_start=1132
  _globals['_GETONLINEFEATURESRESPONSE']._serialized_end=1470
  _globals['_GETONLINEFEATURESRESPONSE_FEATUREVECTOR']._serialized_start=1319
  _globals['_GETONLINEFEATURESRESPONSE_FEATUREVECTOR']._serialized_end=1470
  _globals['_GETONLINEFEATURESRESPONSEMETADATA']._serialized_start=1472
  _globals['_GETONLINEFEATURESRESPONSEMETADATA']._serialized_end=1558
  _globals['_SERVINGSERVICE']._serialized_start=1654
  _globals['_SERVINGSERVICE']._serialized_end=1884
# @@protoc_insertion_point(module_scope)
