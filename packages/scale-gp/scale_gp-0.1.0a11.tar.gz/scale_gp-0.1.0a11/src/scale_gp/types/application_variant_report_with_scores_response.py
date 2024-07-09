# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .evaluation_dataset_response import EvaluationDatasetResponse

__all__ = [
    "ApplicationVariantReportWithScoresResponse",
    "CategoryScore",
    "CategoryScoreApplicationCategoryScoreAccuracy",
    "CategoryScoreApplicationCategoryScoreAccuracyMetricScore",
    "CategoryScoreApplicationCategoryScoreAccuracyMetricScoreApplicationMetricScoreAnswerCorrectness",
    "CategoryScoreApplicationCategoryScoreAccuracyMetricScoreApplicationMetricScoreAnswerRelevance",
    "CategoryScoreApplicationCategoryScoreRetrieval",
    "CategoryScoreApplicationCategoryScoreRetrievalMetricScore",
    "CategoryScoreApplicationCategoryScoreRetrievalMetricScoreApplicationMetricScoreFaithfulness",
    "CategoryScoreApplicationCategoryScoreRetrievalMetricScoreApplicationMetricScoreContextRecall",
    "CategoryScoreApplicationCategoryScoreQuality",
    "CategoryScoreApplicationCategoryScoreQualityMetricScore",
    "CategoryScoreApplicationCategoryScoreQualityMetricScoreApplicationMetricScoreCoherence",
    "CategoryScoreApplicationCategoryScoreQualityMetricScoreApplicationMetricScoreGrammar",
    "CategoryScoreApplicationCategoryScoreTrustAndSafety",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScore",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafety",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScore",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumBiasAndStereotypingSafetyBiasAndStereotyping",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumOpinionsDisputedTopicsSafetyOpinionsDisputedTopics",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumUnethicalHarmfulActivitiesSafetyUnethicalHarmfulActivities",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumCopyrightViolationsSafetyCopyrightViolations",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumHarmfulContentSafetyHarmfulContent",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumPrivacyViolationsSafetyPrivacyViolations",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumProfanitySafetyProfanity",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumSystemInformationSafetySystemInformation",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreModeration",
    "EvaluationDataset",
]


class CategoryScoreApplicationCategoryScoreAccuracyMetricScoreApplicationMetricScoreAnswerCorrectness(BaseModel):
    metric_type: Literal["answer-correctness"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreAccuracyMetricScoreApplicationMetricScoreAnswerRelevance(BaseModel):
    metric_type: Literal["answer-relevance"]

    score: Optional[float] = None


CategoryScoreApplicationCategoryScoreAccuracyMetricScore = Union[
    CategoryScoreApplicationCategoryScoreAccuracyMetricScoreApplicationMetricScoreAnswerCorrectness,
    CategoryScoreApplicationCategoryScoreAccuracyMetricScoreApplicationMetricScoreAnswerRelevance,
]


class CategoryScoreApplicationCategoryScoreAccuracy(BaseModel):
    category: Literal["accuracy"]

    metric_scores: List[CategoryScoreApplicationCategoryScoreAccuracyMetricScore]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreRetrievalMetricScoreApplicationMetricScoreFaithfulness(BaseModel):
    metric_type: Literal["faithfulness"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreRetrievalMetricScoreApplicationMetricScoreContextRecall(BaseModel):
    metric_type: Literal["context-recall"]

    score: Optional[float] = None


CategoryScoreApplicationCategoryScoreRetrievalMetricScore = Union[
    CategoryScoreApplicationCategoryScoreRetrievalMetricScoreApplicationMetricScoreFaithfulness,
    CategoryScoreApplicationCategoryScoreRetrievalMetricScoreApplicationMetricScoreContextRecall,
]


class CategoryScoreApplicationCategoryScoreRetrieval(BaseModel):
    category: Literal["retrieval"]

    metric_scores: List[CategoryScoreApplicationCategoryScoreRetrievalMetricScore]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreQualityMetricScoreApplicationMetricScoreCoherence(BaseModel):
    metric_type: Literal["coherence"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreQualityMetricScoreApplicationMetricScoreGrammar(BaseModel):
    metric_type: Literal["grammar"]

    score: Optional[float] = None


CategoryScoreApplicationCategoryScoreQualityMetricScore = Union[
    CategoryScoreApplicationCategoryScoreQualityMetricScoreApplicationMetricScoreCoherence,
    CategoryScoreApplicationCategoryScoreQualityMetricScoreApplicationMetricScoreGrammar,
]


class CategoryScoreApplicationCategoryScoreQuality(BaseModel):
    category: Literal["quality"]

    metric_scores: List[CategoryScoreApplicationCategoryScoreQualityMetricScore]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumBiasAndStereotypingSafetyBiasAndStereotyping(
    BaseModel
):
    metric_type: Literal["safety-bias-and-stereotyping"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumOpinionsDisputedTopicsSafetyOpinionsDisputedTopics(
    BaseModel
):
    metric_type: Literal["safety-opinions-disputed-topics"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumUnethicalHarmfulActivitiesSafetyUnethicalHarmfulActivities(
    BaseModel
):
    metric_type: Literal["safety-unethical-harmful-activities"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumCopyrightViolationsSafetyCopyrightViolations(
    BaseModel
):
    metric_type: Literal["safety-copyright-violations"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumHarmfulContentSafetyHarmfulContent(
    BaseModel
):
    metric_type: Literal["safety-harmful-content"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumPrivacyViolationsSafetyPrivacyViolations(
    BaseModel
):
    metric_type: Literal["safety-privacy-violations"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumProfanitySafetyProfanity(
    BaseModel
):
    metric_type: Literal["safety-profanity"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumSystemInformationSafetySystemInformation(
    BaseModel
):
    metric_type: Literal["safety-system-information"]

    score: Optional[float] = None


CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScore = Union[
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumBiasAndStereotypingSafetyBiasAndStereotyping,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumOpinionsDisputedTopicsSafetyOpinionsDisputedTopics,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumUnethicalHarmfulActivitiesSafetyUnethicalHarmfulActivities,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumCopyrightViolationsSafetyCopyrightViolations,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumHarmfulContentSafetyHarmfulContent,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumPrivacyViolationsSafetyPrivacyViolations,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumProfanitySafetyProfanity,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralSafetySubMetricTypeEnumSystemInformationSafetySystemInformation,
]


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafety(BaseModel):
    metric_type: Literal["safety"]

    sub_metric_scores: List[
        CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScore
    ]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreModeration(BaseModel):
    metric_type: Literal["moderation"]

    score: Optional[float] = None


CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScore = Union[
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafety,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreModeration,
]


class CategoryScoreApplicationCategoryScoreTrustAndSafety(BaseModel):
    category: Literal["trust-and-safety"]

    metric_scores: List[CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScore]

    score: Optional[float] = None


CategoryScore = Union[
    CategoryScoreApplicationCategoryScoreAccuracy,
    CategoryScoreApplicationCategoryScoreRetrieval,
    CategoryScoreApplicationCategoryScoreQuality,
    CategoryScoreApplicationCategoryScoreTrustAndSafety,
]


class EvaluationDataset(BaseModel):
    evaluation_dataset: EvaluationDatasetResponse

    evaluation_dataset_version_num: int

    generation_status: Literal["Pending", "Running", "Completed", "Failed", "Canceled"]
    """An enumeration."""

    scored_test_case_count: Optional[int] = None


class ApplicationVariantReportWithScoresResponse(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    category_scores: Optional[List[CategoryScore]] = None

    evaluation_datasets: Optional[List[EvaluationDataset]] = None

    score: Optional[float] = None
