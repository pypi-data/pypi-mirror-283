# generated by datamodel-codegen:
#   filename:  create_media_insights_dcr.json

from __future__ import annotations

from enum import Enum
from typing import Optional, Sequence, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, conint


class EnclaveSpecificationV0(BaseModel):
    attestationProtoBase64: str
    id: str
    workerProtocol: conint(ge=0)


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


class ModelEvaluationType(Enum):
    ROC_CURVE = 'ROC_CURVE'
    DISTANCE_TO_EMBEDDING = 'DISTANCE_TO_EMBEDDING'
    JACCARD = 'JACCARD'


class ModelEvaluationConfig(BaseModel):
    postScopeMerge: Sequence[ModelEvaluationType]
    preScopeMerge: Sequence[ModelEvaluationType]


class CreateMediaInsightsV0(BaseModel):
    advertiserEmails: Sequence[str]
    agencyEmails: Sequence[str]
    authenticationRootCertificatePem: str
    driverEnclaveSpecification: EnclaveSpecificationV0
    enableDebugMode: bool
    enableInsights: bool
    enableLookalike: bool
    enableRateLimitingOnPublishDataset: Optional[bool] = None
    enableRetargeting: bool
    hashMatchingIdWith: Optional[HashingAlgorithm] = None
    id: str
    mainAdvertiserEmail: str
    mainPublisherEmail: str
    matchingIdFormat: FormatType
    modelEvaluation: Optional[ModelEvaluationConfig] = None
    name: str
    observerEmails: Sequence[str]
    publisherEmails: Sequence[str]
    pythonEnclaveSpecification: EnclaveSpecificationV0
    rateLimitPublishDataNumPerWindow: Optional[conint(ge=0)] = None
    rateLimitPublishDataWindowSeconds: Optional[conint(ge=0)] = None


class CreateMediaInsightsV1(BaseModel):
    advertiserEmails: Sequence[str]
    agencyEmails: Sequence[str]
    authenticationRootCertificatePem: str
    driverEnclaveSpecification: EnclaveSpecificationV0
    enableDebugMode: bool
    enableInsights: bool
    enableLookalike: bool
    enableRateLimitingOnPublishDataset: Optional[bool] = None
    enableRetargeting: bool
    hashMatchingIdWith: Optional[HashingAlgorithm] = None
    hideAbsoluteValuesFromInsights: bool
    id: str
    mainAdvertiserEmail: str
    mainPublisherEmail: str
    matchingIdFormat: FormatType
    modelEvaluation: Optional[ModelEvaluationConfig] = None
    name: str
    observerEmails: Sequence[str]
    publisherEmails: Sequence[str]
    pythonEnclaveSpecification: EnclaveSpecificationV0
    rateLimitPublishDataNumPerWindow: Optional[conint(ge=0)] = None
    rateLimitPublishDataWindowSeconds: Optional[conint(ge=0)] = None


class CreateMediaInsightsV2(BaseModel):
    advertiserEmails: Sequence[str]
    agencyEmails: Sequence[str]
    authenticationRootCertificatePem: str
    dataPartnerEmails: Optional[Sequence[str]] = None
    driverEnclaveSpecification: EnclaveSpecificationV0
    enableAdvertiserAudienceDownload: Optional[bool] = None
    enableDataPartner: bool
    enableDebugMode: bool
    enableInsights: bool
    enableLookalike: bool
    enableRateLimitingOnPublishDataset: Optional[bool] = None
    enableRetargeting: bool
    hashMatchingIdWith: Optional[HashingAlgorithm] = None
    hideAbsoluteValuesFromInsights: bool
    id: str
    mainAdvertiserEmail: str
    mainPublisherEmail: str
    matchingIdFormat: FormatType
    modelEvaluation: Optional[ModelEvaluationConfig] = None
    name: str
    observerEmails: Sequence[str]
    publisherEmails: Sequence[str]
    pythonEnclaveSpecification: EnclaveSpecificationV0
    rateLimitPublishDataNumPerWindow: Optional[conint(ge=0)] = None
    rateLimitPublishDataWindowSeconds: Optional[conint(ge=0)] = None


class CreateMediaInsightsV3(BaseModel):
    advertiserEmails: Sequence[str]
    agencyEmails: Sequence[str]
    authenticationRootCertificatePem: str
    dataPartnerEmails: Optional[Sequence[str]] = None
    driverEnclaveSpecification: EnclaveSpecificationV0
    enableAdvertiserAudienceDownload: Optional[bool] = None
    enableDataPartner: bool
    enableDebugMode: bool
    enableExclusionTargeting: bool
    enableInsights: bool
    enableLookalike: bool
    enableRateLimitingOnPublishDataset: Optional[bool] = None
    enableRetargeting: bool
    hashMatchingIdWith: Optional[HashingAlgorithm] = None
    hideAbsoluteValuesFromInsights: bool
    id: str
    mainAdvertiserEmail: str
    mainPublisherEmail: str
    matchingIdFormat: FormatType
    modelEvaluation: Optional[ModelEvaluationConfig] = None
    name: str
    observerEmails: Sequence[str]
    publisherEmails: Sequence[str]
    pythonEnclaveSpecification: EnclaveSpecificationV0
    rateLimitPublishDataNumPerWindow: Optional[conint(ge=0)] = None
    rateLimitPublishDataWindowSeconds: Optional[conint(ge=0)] = None


class CreateMediaInsightsDcr1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v0: CreateMediaInsightsV0


class CreateMediaInsightsDcr2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v1: CreateMediaInsightsV1


class CreateMediaInsightsDcr3(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v2: CreateMediaInsightsV2


class CreateMediaInsightsDcr4(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    v3: CreateMediaInsightsV3


class CreateMediaInsightsDcr(
    RootModel[
        Union[
            CreateMediaInsightsDcr1,
            CreateMediaInsightsDcr2,
            CreateMediaInsightsDcr3,
            CreateMediaInsightsDcr4,
        ]
    ]
):
    root: Union[
        CreateMediaInsightsDcr1,
        CreateMediaInsightsDcr2,
        CreateMediaInsightsDcr3,
        CreateMediaInsightsDcr4,
    ] = Field(
        ...,
        description='Arguments for creating a specific version of a MIDCR.',
        title='CreateMediaInsightsDcr',
    )
