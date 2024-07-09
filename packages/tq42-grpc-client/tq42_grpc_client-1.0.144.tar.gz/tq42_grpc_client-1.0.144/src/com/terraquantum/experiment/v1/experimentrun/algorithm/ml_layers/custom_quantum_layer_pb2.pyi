from buf.validate import validate_pb2 as _validate_pb2
from com.terraquantum import default_value_pb2 as _default_value_pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.gate import cnot_pb2 as _cnot_pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.gate import encoding_pb2 as _encoding_pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.gate import hadamard_pb2 as _hadamard_pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.gate import variational_pb2 as _variational_pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.gate import measurement_pb2 as _measurement_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gate(_message.Message):
    __slots__ = ("variational", "encoding", "cnot", "hadamard", "measurement")
    VARIATIONAL_FIELD_NUMBER: _ClassVar[int]
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    CNOT_FIELD_NUMBER: _ClassVar[int]
    HADAMARD_FIELD_NUMBER: _ClassVar[int]
    MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    variational: _variational_pb2.VariationalGate
    encoding: _encoding_pb2.EncodingGate
    cnot: _cnot_pb2.CnotGate
    hadamard: _hadamard_pb2.HadamardGate
    measurement: _measurement_pb2.MeasurementGate
    def __init__(self, variational: _Optional[_Union[_variational_pb2.VariationalGate, _Mapping]] = ..., encoding: _Optional[_Union[_encoding_pb2.EncodingGate, _Mapping]] = ..., cnot: _Optional[_Union[_cnot_pb2.CnotGate, _Mapping]] = ..., hadamard: _Optional[_Union[_hadamard_pb2.HadamardGate, _Mapping]] = ..., measurement: _Optional[_Union[_measurement_pb2.MeasurementGate, _Mapping]] = ...) -> None: ...

class CustomQuantumLayer(_message.Message):
    __slots__ = ("num_qubits", "gates")
    NUM_QUBITS_FIELD_NUMBER: _ClassVar[int]
    GATES_FIELD_NUMBER: _ClassVar[int]
    num_qubits: int
    gates: _containers.RepeatedCompositeFieldContainer[Gate]
    def __init__(self, num_qubits: _Optional[int] = ..., gates: _Optional[_Iterable[_Union[Gate, _Mapping]]] = ...) -> None: ...
