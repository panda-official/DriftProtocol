set(PROTO_SPEC_ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../proto_specs)

# Generate protoc files
set(PROTOBUF_SPEC_FILES
        ${PROTO_SPEC_ROOT_DIR}/drift_protocol/common/drift_package.proto
        ${PROTO_SPEC_ROOT_DIR}/drift_protocol/common/data_payload.proto
        ${PROTO_SPEC_ROOT_DIR}/drift_protocol/common/status_code.proto
        ${PROTO_SPEC_ROOT_DIR}/drift_protocol/meta/meta_info.proto
        ${PROTO_SPEC_ROOT_DIR}/drift_protocol/trigger_service/trigger_message.proto
        ${PROTO_SPEC_ROOT_DIR}/drift_protocol/trigger_service/interval_trigger_message.proto
        )

set(PROTOBUF_FILES
        ${CMAKE_BINARY_DIR}/drift_protocol/common/drift_package.pb.cc
        ${CMAKE_BINARY_DIR}/drift_protocol/common/data_payload.pb.cc
        ${CMAKE_BINARY_DIR}/drift_protocol/common/status_code.pb.cc
        ${CMAKE_BINARY_DIR}/drift_protocol/meta/meta_info.pb.cc
        ${CMAKE_BINARY_DIR}/drift_protocol/trigger_service/trigger_message.pb.cc
        ${CMAKE_BINARY_DIR}/drift_protocol/trigger_service/interval_trigger_message.pb.cc
        )


add_custom_command(OUTPUT ${PROTOBUF_FILES}
        COMMAND ${Protobuf_PROTOC_EXECUTABLE} -I=${PROTO_SPEC_ROOT_DIR}/
        --cpp_out=${CMAKE_BINARY_DIR} ${PROTO_SPEC_ROOT_DIR}/drift_protocol/common/*

        COMMAND ${Protobuf_PROTOC_EXECUTABLE} -I=${PROTO_SPEC_ROOT_DIR}/
        --cpp_out=${CMAKE_BINARY_DIR} ${PROTO_SPEC_ROOT_DIR}/drift_protocol/meta/*

        COMMAND ${Protobuf_PROTOC_EXECUTABLE} -I=${PROTO_SPEC_ROOT_DIR}/
        --cpp_out=${CMAKE_BINARY_DIR} ${PROTO_SPEC_ROOT_DIR}/drift_protocol/trigger_service/*

        DEPENDS ${PROTOBUF_SPEC_FILES}
        )
