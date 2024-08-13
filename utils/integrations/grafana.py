import urllib.parse

from pydantic import BaseModel, Field, ConfigDict, HttpUrl


class GrafanaDashboardURLBuilder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    var_pod: str = Field(alias="var-pod", default="All")
    to_time: str = Field(alias="to")
    from_time: str = Field(alias="from")
    var_cluster: str = Field(alias="var-cluster", default="dt-dev-euc1")
    dashboard_id: str = "6581e46e4e5c7ba40a07646395ef7b23"
    var_namespace: str = Field(alias="var-namespace")
    var_datasource: str = Field(alias="var-datasource", default="default")
    organization_id: int = Field(alias="orgId", default=1)

    def build_url(self, base_url: HttpUrl) -> HttpUrl:
        query = urllib.parse.urlencode(self.model_dump(by_alias=True))

        return HttpUrl(
            f"{base_url}d/{self.dashboard_id}/kubernetes-compute-resources-pod?{query}"
        )
