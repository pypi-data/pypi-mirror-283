# generated by datamodel-codegen:
#   filename:  analytics/reportData.json
#   timestamp: 2024-07-04T09:01:46+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field

from ..type import basic
from .reportDataType import (
    aggregatedCostAnalysisReportData,
    entityReportData,
    rawCostAnalysisReportData,
    webAnalyticEntityViewReportData,
    webAnalyticUserActivityReportData,
)


class ReportDataType(Enum):
    entityReportData = 'entityReportData'
    webAnalyticUserActivityReportData = 'webAnalyticUserActivityReportData'
    webAnalyticEntityViewReportData = 'webAnalyticEntityViewReportData'
    rawCostAnalysisReportData = 'rawCostAnalysisReportData'
    aggregatedCostAnalysisReportData = 'aggregatedCostAnalysisReportData'


class ReportData(BaseModel):
    id: Optional[basic.Uuid] = Field(
        None, description='Unique identifier for a result.'
    )
    timestamp: basic.Timestamp = Field(
        ..., description='timestamp for of a result ingestion.'
    )
    reportDataType: Optional[ReportDataType] = Field(None, description='Type of data')
    data: Optional[
        Union[
            entityReportData.EntityReportData,
            webAnalyticUserActivityReportData.WebAnalyticUserActivityReportData,
            webAnalyticEntityViewReportData.WebAnalyticEntityViewReportData,
            rawCostAnalysisReportData.RawCostAnalysisReportData,
            aggregatedCostAnalysisReportData.AggregatedCostAnalysisReportData,
        ]
    ] = Field(None, description='Data captured')
