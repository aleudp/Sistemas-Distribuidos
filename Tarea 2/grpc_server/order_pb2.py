# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: order.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'order.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0border.proto\x12\x05order\"\xa9\x01\n\x0cOrderRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x14\n\x0cproduct_name\x18\x02 \x01(\t\x12\r\n\x05price\x18\x03 \x01(\x01\x12\x16\n\x0epayment_method\x18\x04 \x01(\t\x12\x12\n\ncard_brand\x18\x05 \x01(\t\x12\x0c\n\x04\x62\x61nk\x18\x06 \x01(\t\x12\x0e\n\x06region\x18\x07 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x08 \x01(\t\x12\r\n\x05\x65mail\x18\t \x01(\t\"\x1f\n\rOrderResponse\x12\x0e\n\x06status\x18\x01 \x01(\t2G\n\x0cOrderService\x12\x37\n\nPlaceOrder\x12\x13.order.OrderRequest\x1a\x14.order.OrderResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ORDERREQUEST']._serialized_start=23
  _globals['_ORDERREQUEST']._serialized_end=192
  _globals['_ORDERRESPONSE']._serialized_start=194
  _globals['_ORDERRESPONSE']._serialized_end=225
  _globals['_ORDERSERVICE']._serialized_start=227
  _globals['_ORDERSERVICE']._serialized_end=298
# @@protoc_insertion_point(module_scope)