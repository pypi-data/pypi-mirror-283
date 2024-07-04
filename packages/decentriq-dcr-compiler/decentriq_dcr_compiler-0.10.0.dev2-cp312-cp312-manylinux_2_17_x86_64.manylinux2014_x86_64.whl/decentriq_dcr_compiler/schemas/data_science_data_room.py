# generated by datamodel-codegen:
#   filename:  data_science_data_room.json

from __future__ import annotations

from enum import Enum
from typing import Optional, Sequence, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, conint


class AnalystPermission(BaseModel):
    nodeId: str


class AwsConfig(BaseModel):
    bucket: str
    objectKey: Optional[str] = None
    region: str


class ColumnDataType(Enum):
    integer = 'integer'
    float = 'float'
    string = 'string'


class ColumnTuple(BaseModel):
    columns: Sequence[conint(ge=0)]


class DataOwnerPermission(AnalystPermission):
    pass


class DatasetSinkEncryptionKeyDependency(BaseModel):
    dependency: str
    isKeyHexEncoded: bool


class EnclaveSpecification(BaseModel):
    attestationProtoBase64: str
    id: str
    workerProtocol: conint(ge=0)


class ExportConnectorKind(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    aws: AwsConfig


class ExportConnectorKind2(RootModel[ExportConnectorKind]):
    root: ExportConnectorKind


class ExportType4(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    raw: Sequence = Field(..., max_length=0, min_length=0)


class ExportType5(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    zipSingleFile: str


class ExportType6(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    zipAllFiles: Sequence = Field(..., max_length=0, min_length=0)


class ExportType(RootModel[Union[ExportType4, ExportType5, ExportType6]]):
    root: Union[ExportType4, ExportType5, ExportType6]


class FormatType(Enum):
    STRING = 'STRING'
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    EMAIL = 'EMAIL'
    DATE_ISO8601 = 'DATE_ISO8601'
    PHONE_NUMBER_E164 = 'PHONE_NUMBER_E164'
    HASH_SHA256_HEX = 'HASH_SHA256_HEX'


class HashingAlgorithm(Enum):
    SHA256_HEX = 'SHA256_HEX'


class ImportConnectorKind(ExportConnectorKind):
    pass


class ImportConnectorKind2(RootModel[ImportConnectorKind]):
    root: ImportConnectorKind


class ImportConnectorNode(BaseModel):
    credentialsDependency: str
    kind: ImportConnectorKind2
    specificationId: str


class InputDataType3(ExportType4):
    pass


class ManagerPermission(BaseModel):
    pass


class MaskType(Enum):
    genericString = 'genericString'
    genericNumber = 'genericNumber'
    name = 'name'
    address = 'address'
    postcode = 'postcode'
    phoneNumber = 'phoneNumber'
    socialSecurityNumber = 'socialSecurityNumber'
    email = 'email'
    date = 'date'
    timestamp = 'timestamp'
    iban = 'iban'


class MatchingComputationNode(BaseModel):
    config: str
    dependencies: Sequence[str]
    enableLogsOnError: bool
    enableLogsOnSuccess: bool
    output: str
    specificationId: str
    staticContentSpecificationId: str


class NumRowsValidationRule(BaseModel):
    atLeast: Optional[conint(ge=0)] = None
    atMost: Optional[conint(ge=0)] = None


class NumericRangeRule(BaseModel):
    greaterThan: Optional[float] = None
    greaterThanEquals: Optional[float] = None
    lessThan: Optional[float] = None
    lessThanEquals: Optional[float] = None


class ParticipantPermission1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    dataOwner: DataOwnerPermission


class ParticipantPermission2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    analyst: AnalystPermission


class ParticipantPermission3(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    manager: ManagerPermission


class ParticipantPermission(
    RootModel[
        Union[ParticipantPermission1, ParticipantPermission2, ParticipantPermission3]
    ]
):
    root: Union[ParticipantPermission1, ParticipantPermission2, ParticipantPermission3]


class PostComputationNode(BaseModel):
    dependency: str
    specificationId: str
    useMockBackend: bool


class PreviewComputationNode(BaseModel):
    dependency: str
    quotaBytes: conint(ge=0)


class RawLeafNode(ManagerPermission):
    pass


class S3Provider(Enum):
    Aws = 'Aws'
    Gcs = 'Gcs'


class S3SinkComputationNode(BaseModel):
    credentialsDependencyId: str
    endpoint: str
    region: Optional[str] = ''
    s3Provider: Optional[S3Provider] = 'Aws'
    specificationId: str
    uploadDependencyId: str


class Script(BaseModel):
    content: str
    name: str


class ScriptingLanguage(Enum):
    python = 'python'
    r = 'r'


class SqlNodePrivacyFilter(BaseModel):
    minimumRowsCount: int


class TableMapping(BaseModel):
    nodeId: str
    tableName: str


class UniquenessValidationRule(BaseModel):
    uniqueKeys: Sequence[ColumnTuple]


class ZipInputDataType3(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    all: Sequence = Field(..., max_length=0, min_length=0)


class ZipInputDataType4(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    files: Sequence[str]


class ZipInputDataType(RootModel[Union[ZipInputDataType3, ZipInputDataType4]]):
    root: Union[ZipInputDataType3, ZipInputDataType4]


class ColumnDataFormat(BaseModel):
    dataType: ColumnDataType
    isNullable: bool


class ColumnValidationV0(BaseModel):
    allowNull: bool
    formatType: FormatType
    hashWith: Optional[HashingAlgorithm] = None
    inRange: Optional[NumericRangeRule] = None
    name: Optional[str] = None


class ComputationNodeKind9(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    s3Sink: S3SinkComputationNode


class ComputationNodeKind10(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    match: MatchingComputationNode


class ComputationNodeKindV2(ComputationNodeKind9):
    pass


class ComputationNodeKindV214(ComputationNodeKind10):
    pass


class ComputationNodeKindV215(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    post: PostComputationNode


class ComputationNodeKindV6(ComputationNodeKind9):
    pass


class ComputationNodeKindV618(ComputationNodeKind10):
    pass


class ComputationNodeKindV619(ComputationNodeKindV215):
    pass


class ComputationNodeKindV620(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    preview: PreviewComputationNode


class ComputationNodeKindV621(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    importConnector: ImportConnectorNode


class ExportNodeDependency(BaseModel):
    exportType: ExportType
    name: str


class InputDataType4(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    zip: ZipInputDataType


class InputDataType(RootModel[Union[InputDataType3, InputDataType4]]):
    root: Union[InputDataType3, InputDataType4]


class LeafNodeKind3(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    raw: RawLeafNode


class LeafNodeKindV2(LeafNodeKind3):
    pass


class Participant(BaseModel):
    permissions: Sequence[ParticipantPermission]
    user: str


class ScriptingComputationNode(BaseModel):
    additionalScripts: Sequence[Script]
    dependencies: Sequence[str]
    enableLogsOnError: bool
    enableLogsOnSuccess: bool
    extraChunkCacheSizeToAvailableMemoryRatio: Optional[float] = None
    mainScript: Script
    minimumContainerMemorySize: Optional[conint(ge=0)] = None
    output: str
    scriptingLanguage: ScriptingLanguage
    scriptingSpecificationId: str
    staticContentSpecificationId: str


class SqlComputationNode(BaseModel):
    dependencies: Sequence[TableMapping]
    privacyFilter: Optional[SqlNodePrivacyFilter] = None
    specificationId: str
    statement: str


class SqliteComputationNode(BaseModel):
    dependencies: Sequence[TableMapping]
    enableLogsOnError: bool
    enableLogsOnSuccess: bool
    sqliteSpecificationId: str
    statement: str
    staticContentSpecificationId: str


class SyntheticNodeColumn(BaseModel):
    dataFormat: ColumnDataFormat
    index: int
    maskType: MaskType
    name: Optional[str] = None
    shouldMaskColumn: bool


class TableLeafNodeColumn(BaseModel):
    dataFormat: ColumnDataFormat
    name: str


class TableLeafNodeColumnV2(BaseModel):
    dataFormat: ColumnDataFormat
    name: str
    validation: ColumnValidationV0


class TableValidationV0(BaseModel):
    allowEmpty: Optional[bool] = None
    numRows: Optional[NumRowsValidationRule] = None
    uniqueness: Optional[UniquenessValidationRule] = None


class ValidationNodeV2(BaseModel):
    pythonSpecificationId: str
    staticContentSpecificationId: str
    validation: TableValidationV0


class ComputationNodeKind6(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    sql: SqlComputationNode


class ComputationNodeKind7(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    scripting: ScriptingComputationNode


class ComputationNodeKindV29(ComputationNodeKind6):
    pass


class ComputationNodeKindV210(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    sqlite: SqliteComputationNode


class ComputationNodeKindV211(ComputationNodeKind7):
    pass


class ComputationNodeKindV613(ComputationNodeKind6):
    pass


class ComputationNodeKindV614(ComputationNodeKindV210):
    pass


class ComputationNodeKindV615(ComputationNodeKind7):
    pass


class DatasetSinkInput(BaseModel):
    datasetName: str
    dependency: str
    inputDataType: InputDataType


class ExportConnectorNode(BaseModel):
    credentialsDependency: str
    dependency: ExportNodeDependency
    kind: ExportConnectorKind2
    specificationId: str


class SyntheticDataComputationNode(BaseModel):
    columns: Sequence[SyntheticNodeColumn]
    dependency: str
    enableLogsOnError: bool
    enableLogsOnSuccess: bool
    epsilon: float
    outputOriginalDataStatistics: bool
    staticContentSpecificationId: str
    synthSpecificationId: str


class TableLeafNode(BaseModel):
    columns: Sequence[TableLeafNodeColumn]
    sqlSpecificationId: str


class TableLeafNodeV2(BaseModel):
    columns: Sequence[TableLeafNodeColumnV2]
    validationNode: ValidationNodeV2


class ComputationNodeKind8(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    syntheticData: SyntheticDataComputationNode


class ComputationNodeKind(
    RootModel[
        Union[
            ComputationNodeKind6,
            ComputationNodeKind7,
            ComputationNodeKind8,
            ComputationNodeKind9,
            ComputationNodeKind10,
        ]
    ]
):
    root: Union[
        ComputationNodeKind6,
        ComputationNodeKind7,
        ComputationNodeKind8,
        ComputationNodeKind9,
        ComputationNodeKind10,
    ]


class ComputationNodeKindV212(ComputationNodeKind8):
    pass


class ComputationNodeKindV28(
    RootModel[
        Union[
            ComputationNodeKindV29,
            ComputationNodeKindV210,
            ComputationNodeKindV211,
            ComputationNodeKindV212,
            ComputationNodeKindV2,
            ComputationNodeKindV214,
            ComputationNodeKindV215,
        ]
    ]
):
    root: Union[
        ComputationNodeKindV29,
        ComputationNodeKindV210,
        ComputationNodeKindV211,
        ComputationNodeKindV212,
        ComputationNodeKindV2,
        ComputationNodeKindV214,
        ComputationNodeKindV215,
    ]


class ComputationNodeKindV616(ComputationNodeKind8):
    pass


class ComputationNodeKindV622(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    exportConnector: ExportConnectorNode


class ComputationNodeV2(BaseModel):
    kind: ComputationNodeKindV28


class DatasetSinkComputationNode(BaseModel):
    datasetImportId: Optional[str] = None
    encryptionKeyDependency: DatasetSinkEncryptionKeyDependency
    input: DatasetSinkInput
    specificationId: str


class LeafNodeKind4(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    table: TableLeafNode


class LeafNodeKind(RootModel[Union[LeafNodeKind3, LeafNodeKind4]]):
    root: Union[LeafNodeKind3, LeafNodeKind4]


class LeafNodeKindV25(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    table: TableLeafNodeV2


class LeafNodeKindV23(RootModel[Union[LeafNodeKindV2, LeafNodeKindV25]]):
    root: Union[LeafNodeKindV2, LeafNodeKindV25]


class LeafNodeV2(BaseModel):
    isRequired: bool
    kind: LeafNodeKindV23


class NodeKindV2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    leaf: LeafNodeV2


class NodeKindV25(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    computation: ComputationNodeV2


class NodeKindV23(RootModel[Union[NodeKindV2, NodeKindV25]]):
    root: Union[NodeKindV2, NodeKindV25]


class NodeKindV6(NodeKindV2):
    pass


class NodeV2(BaseModel):
    id: str
    kind: NodeKindV23
    name: str


class AddComputationCommitV2(BaseModel):
    analysts: Sequence[str]
    enclaveSpecifications: Sequence[EnclaveSpecification]
    node: NodeV2


class ComputationNode(BaseModel):
    kind: ComputationNodeKind


class ComputationNodeKindV623(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    datasetSink: DatasetSinkComputationNode


class ComputationNodeKindV612(
    RootModel[
        Union[
            ComputationNodeKindV613,
            ComputationNodeKindV614,
            ComputationNodeKindV615,
            ComputationNodeKindV616,
            ComputationNodeKindV6,
            ComputationNodeKindV618,
            ComputationNodeKindV619,
            ComputationNodeKindV620,
            ComputationNodeKindV621,
            ComputationNodeKindV622,
            ComputationNodeKindV623,
        ]
    ]
):
    root: Union[
        ComputationNodeKindV613,
        ComputationNodeKindV614,
        ComputationNodeKindV615,
        ComputationNodeKindV616,
        ComputationNodeKindV6,
        ComputationNodeKindV618,
        ComputationNodeKindV619,
        ComputationNodeKindV620,
        ComputationNodeKindV621,
        ComputationNodeKindV622,
        ComputationNodeKindV623,
    ]


class ComputationNodeV6(BaseModel):
    kind: ComputationNodeKindV612


class DataScienceCommitKindV2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    addComputation: AddComputationCommitV2


class DataScienceCommitKindV22(RootModel[DataScienceCommitKindV2]):
    root: DataScienceCommitKindV2


class DataScienceCommitV2(BaseModel):
    enclaveDataRoomId: str
    historyPin: str
    id: str
    kind: DataScienceCommitKindV22
    name: str


class DataScienceCommitV3(DataScienceCommitV2):
    pass


class DataScienceCommitV4(DataScienceCommitV2):
    pass


class DataScienceCommitV5(DataScienceCommitV2):
    pass


class DataScienceDataRoomConfigurationV2(BaseModel):
    dcrSecretIdBase64: Optional[str] = None
    description: str
    enableDevelopment: bool
    enablePostWorker: bool
    enableServersideWasmValidation: bool
    enableSqliteWorker: bool
    enableTestDatasets: bool
    enclaveRootCertificatePem: str
    enclaveSpecifications: Sequence[EnclaveSpecification]
    id: str
    nodes: Sequence[NodeV2]
    participants: Sequence[Participant]
    title: str


class DataScienceDataRoomConfigurationV3(BaseModel):
    dcrSecretIdBase64: Optional[str] = None
    description: str
    enableDevelopment: bool
    enablePostWorker: bool
    enableSafePythonWorkerStacktrace: bool
    enableServersideWasmValidation: bool
    enableSqliteWorker: bool
    enableTestDatasets: bool
    enclaveRootCertificatePem: str
    enclaveSpecifications: Sequence[EnclaveSpecification]
    id: str
    nodes: Sequence[NodeV2]
    participants: Sequence[Participant]
    title: str


class DataScienceDataRoomConfigurationV4(DataScienceDataRoomConfigurationV3):
    pass


class DataScienceDataRoomConfigurationV5(BaseModel):
    dcrSecretIdBase64: Optional[str] = None
    description: str
    enableAllowEmptyFilesInValidation: bool
    enableDevelopment: bool
    enablePostWorker: bool
    enableSafePythonWorkerStacktrace: bool
    enableServersideWasmValidation: bool
    enableSqliteWorker: bool
    enableTestDatasets: bool
    enclaveRootCertificatePem: str
    enclaveSpecifications: Sequence[EnclaveSpecification]
    id: str
    nodes: Sequence[NodeV2]
    participants: Sequence[Participant]
    title: str


class DataScienceDataRoomV21(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    static: DataScienceDataRoomConfigurationV2


class DataScienceDataRoomV31(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    static: DataScienceDataRoomConfigurationV3


class DataScienceDataRoomV41(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    static: DataScienceDataRoomConfigurationV4


class DataScienceDataRoomV51(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    static: DataScienceDataRoomConfigurationV5


class InteractiveDataScienceDataRoomV2(BaseModel):
    commits: Sequence[DataScienceCommitV2]
    enableAutomergeFeature: bool
    initialConfiguration: DataScienceDataRoomConfigurationV2


class InteractiveDataScienceDataRoomV3(BaseModel):
    commits: Sequence[DataScienceCommitV3]
    enableAutomergeFeature: bool
    initialConfiguration: DataScienceDataRoomConfigurationV3


class InteractiveDataScienceDataRoomV4(BaseModel):
    commits: Sequence[DataScienceCommitV4]
    enableAutomergeFeature: bool
    initialConfiguration: DataScienceDataRoomConfigurationV4


class InteractiveDataScienceDataRoomV5(BaseModel):
    commits: Sequence[DataScienceCommitV5]
    enableAutomergeFeature: bool
    initialConfiguration: DataScienceDataRoomConfigurationV5


class LeafNode(BaseModel):
    isRequired: bool
    kind: LeafNodeKind


class NodeKind3(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    leaf: LeafNode


class NodeKind4(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    computation: ComputationNode


class NodeKind(RootModel[Union[NodeKind3, NodeKind4]]):
    root: Union[NodeKind3, NodeKind4]


class NodeKindV65(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    computation: ComputationNodeV6


class NodeKindV63(RootModel[Union[NodeKindV6, NodeKindV65]]):
    root: Union[NodeKindV6, NodeKindV65]


class NodeV6(BaseModel):
    id: str
    kind: NodeKindV63
    name: str


class AddComputationCommitV6(BaseModel):
    analysts: Sequence[str]
    enclaveSpecifications: Sequence[EnclaveSpecification]
    node: NodeV6


class DataScienceCommitKindV6(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    addComputation: AddComputationCommitV6


class DataScienceCommitKindV62(RootModel[DataScienceCommitKindV6]):
    root: DataScienceCommitKindV6


class DataScienceCommitV6(BaseModel):
    enclaveDataRoomId: str
    historyPin: str
    id: str
    kind: DataScienceCommitKindV62
    name: str


class DataScienceDataRoomConfigurationV6(BaseModel):
    dcrSecretIdBase64: Optional[str] = None
    description: str
    enableAirlock: bool
    enableAllowEmptyFilesInValidation: bool
    enableDevelopment: bool
    enablePostWorker: bool
    enableSafePythonWorkerStacktrace: bool
    enableServersideWasmValidation: bool
    enableSqliteWorker: bool
    enableTestDatasets: bool
    enclaveRootCertificatePem: str
    enclaveSpecifications: Sequence[EnclaveSpecification]
    id: str
    nodes: Sequence[NodeV6]
    participants: Sequence[Participant]
    title: str


class DataScienceDataRoomV22(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    interactive: InteractiveDataScienceDataRoomV2


class DataScienceDataRoomV2(
    RootModel[Union[DataScienceDataRoomV21, DataScienceDataRoomV22]]
):
    root: Union[DataScienceDataRoomV21, DataScienceDataRoomV22]


class DataScienceDataRoomV32(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    interactive: InteractiveDataScienceDataRoomV3


class DataScienceDataRoomV3(
    RootModel[Union[DataScienceDataRoomV31, DataScienceDataRoomV32]]
):
    root: Union[DataScienceDataRoomV31, DataScienceDataRoomV32]


class DataScienceDataRoomV42(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    interactive: InteractiveDataScienceDataRoomV4


class DataScienceDataRoomV4(
    RootModel[Union[DataScienceDataRoomV41, DataScienceDataRoomV42]]
):
    root: Union[DataScienceDataRoomV41, DataScienceDataRoomV42]


class DataScienceDataRoomV52(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    interactive: InteractiveDataScienceDataRoomV5


class DataScienceDataRoomV5(
    RootModel[Union[DataScienceDataRoomV51, DataScienceDataRoomV52]]
):
    root: Union[DataScienceDataRoomV51, DataScienceDataRoomV52]


class DataScienceDataRoomV61(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    static: DataScienceDataRoomConfigurationV6


class InteractiveDataScienceDataRoomV6(BaseModel):
    commits: Sequence[DataScienceCommitV6]
    enableAutomergeFeature: bool
    initialConfiguration: DataScienceDataRoomConfigurationV6


class Node(BaseModel):
    id: str
    kind: NodeKind
    name: str


class DataScienceDataRoom3(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v2: DataScienceDataRoomV2


class DataScienceDataRoom4(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v3: DataScienceDataRoomV3


class DataScienceDataRoom5(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v4: DataScienceDataRoomV4


class DataScienceDataRoom6(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v5: DataScienceDataRoomV5


class AddComputationCommit(BaseModel):
    analysts: Sequence[str]
    enclaveSpecifications: Sequence[EnclaveSpecification]
    node: Node


class DataScienceCommitKind(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    addComputation: AddComputationCommit


class DataScienceCommitKind2(RootModel[DataScienceCommitKind]):
    root: DataScienceCommitKind


class DataScienceCommitV0(BaseModel):
    enclaveDataRoomId: str
    historyPin: str
    id: str
    kind: DataScienceCommitKind2
    name: str


class DataScienceCommitV1(DataScienceCommitV0):
    pass


class DataScienceDataRoomConfiguration(BaseModel):
    dcrSecretIdBase64: Optional[str] = None
    description: str
    enableDevelopment: bool
    enclaveRootCertificatePem: str
    enclaveSpecifications: Sequence[EnclaveSpecification]
    id: str
    nodes: Sequence[Node]
    participants: Sequence[Participant]
    title: str


class DataScienceDataRoomV01(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    static: DataScienceDataRoomConfiguration


class DataScienceDataRoomV11(DataScienceDataRoomV01):
    pass


class DataScienceDataRoomV62(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    interactive: InteractiveDataScienceDataRoomV6


class DataScienceDataRoomV6(
    RootModel[Union[DataScienceDataRoomV61, DataScienceDataRoomV62]]
):
    root: Union[DataScienceDataRoomV61, DataScienceDataRoomV62]


class InteractiveDataScienceDataRoomV0(BaseModel):
    commits: Sequence[DataScienceCommitV0]
    initialConfiguration: DataScienceDataRoomConfiguration


class InteractiveDataScienceDataRoomV1(BaseModel):
    commits: Sequence[DataScienceCommitV1]
    enableAutomergeFeature: bool
    initialConfiguration: DataScienceDataRoomConfiguration


class DataScienceDataRoom7(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v6: DataScienceDataRoomV6


class DataScienceDataRoomV02(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    interactive: InteractiveDataScienceDataRoomV0


class DataScienceDataRoomV0(
    RootModel[Union[DataScienceDataRoomV01, DataScienceDataRoomV02]]
):
    root: Union[DataScienceDataRoomV01, DataScienceDataRoomV02]


class DataScienceDataRoomV12(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    interactive: InteractiveDataScienceDataRoomV1


class DataScienceDataRoomV1(
    RootModel[Union[DataScienceDataRoomV11, DataScienceDataRoomV12]]
):
    root: Union[DataScienceDataRoomV11, DataScienceDataRoomV12]


class DataScienceDataRoom1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v0: DataScienceDataRoomV0


class DataScienceDataRoom2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v1: DataScienceDataRoomV1


class DataScienceDataRoom(
    RootModel[
        Union[
            DataScienceDataRoom1,
            DataScienceDataRoom2,
            DataScienceDataRoom3,
            DataScienceDataRoom4,
            DataScienceDataRoom5,
            DataScienceDataRoom6,
            DataScienceDataRoom7,
        ]
    ]
):
    root: Union[
        DataScienceDataRoom1,
        DataScienceDataRoom2,
        DataScienceDataRoom3,
        DataScienceDataRoom4,
        DataScienceDataRoom5,
        DataScienceDataRoom6,
        DataScienceDataRoom7,
    ] = Field(..., title='DataScienceDataRoom')

