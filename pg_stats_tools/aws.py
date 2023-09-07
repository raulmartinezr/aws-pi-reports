""""AWS boto functions for pi_reports"""

from datetime import datetime
from typing import Any, List, Literal

from boto3.session import Session
from mypy_boto3_pi.client import PIClient
from mypy_boto3_pi.type_defs import GetResourceMetricsResponseTypeDef, MetricQueryTypeDef
from mypy_boto3_rds.client import RDSClient
from mypy_boto3_rds.type_defs import DBInstanceMessageTypeDef

from pg_stats_tools.time import parse_time


class PIAwsClient:
    """PI AWS Client"""

    def __init__(self) -> None:
        self._pi_client: PIClient

    def pi_get_resource_metrics(
        self,
        service_type: Literal["DOCDB", "RDS"],
        identifier: str,
        metric_queries: List[MetricQueryTypeDef],
        start_time: datetime,
        end_time: datetime,
        period_in_seconds: int = 3600,
        max_results: int = 100,
        next_token: str = "string",
        period_alignment: Literal["END_TIME", "START_TIME"] = "END_TIME",
    ) -> GetResourceMetricsResponseTypeDef:
        result: GetResourceMetricsResponseTypeDef = self._pi_client.get_resource_metrics(
            ServiceType=service_type,
            Identifier=identifier,
            MetricQueries=metric_queries,
            StartTime=start_time,
            EndTime=end_time,
            PeriodInSeconds=period_in_seconds,
            MaxResults=max_results,
            NextToken=next_token,
            PeriodAlignment=period_alignment,
        )
        return result


class RDSAwsCClient:
    """RDS AWS Client"""

    def __init__(self) -> None:
        self._rds_client: RDSClient

    def _rds_get_attribute(self, db_instance_identifier: str, attr_name: str) -> Any:
        response: DBInstanceMessageTypeDef = self._rds_client.describe_db_instances(
            DBInstanceIdentifier=db_instance_identifier
        )
        return response["DBInstances"][0][attr_name]  # type: ignore # pyright: ignore[reportUnknownVariableType]

    def rds_get_database_instance_resource_id(self, db_instance_identifier: str) -> str:
        return str(
            self._rds_get_attribute(
                db_instance_identifier=db_instance_identifier, attr_name="DbiResourceId"
            )
        )


class AWSClient(PIAwsClient, RDSAwsCClient):
    """AWS Client"""

    def __init__(self, aws_profile: str, aws_region: str) -> None:
        super().__init__()
        self._session: Session = Session(profile_name=aws_profile, region_name=aws_region)
        self._pi_client: PIClient = self._session.client(
            "pi"
        )  # pyright: ignore[reportUnknownMemberType]
        self._rds_client: RDSClient = self._session.client(
            "rds"
        )  # pyright: ignore[reportUnknownMemberType]

    def get_resource_metrics_for_db_instance(
        self,
        db_instance_identifier: str,
        service_type: Literal["DOCDB", "RDS"],
        metric_queries: List[MetricQueryTypeDef],
        time: datetime,
        time_delta: str,
        period_in_seconds: int = 3600,
        max_results: int = 100,
        next_token: str = "string",
        period_alignment: Literal["END_TIME", "START_TIME"] = "END_TIME",
    ) -> GetResourceMetricsResponseTypeDef:
        start_time, end_time = parse_time(time, time_delta)

        if service_type == "RDS":
            resource_identifier: str = RDSAwsCClient.rds_get_database_instance_resource_id(
                self, db_instance_identifier=db_instance_identifier
            )
        else:
            raise NotImplementedError(f"Service type {service_type} not implemented")

        return self.pi_get_resource_metrics(
            service_type=service_type,
            identifier=resource_identifier,
            metric_queries=metric_queries,
            start_time=start_time,
            end_time=end_time,
            period_in_seconds=period_in_seconds,
            max_results=max_results,
            next_token=next_token,
            period_alignment=period_alignment,
        )
