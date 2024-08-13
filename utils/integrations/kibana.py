from pydantic import BaseModel, ConfigDict, HttpUrl, Field


class KibanaDiscoverURLBuilder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    to_time: str
    from_time: str
    namespace: str = Field(alias="var-namespace")

    def build_url(self, base_url: HttpUrl) -> HttpUrl:
        return HttpUrl(
            f"{base_url}s/company/app/discover#/?"
            f"_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:"
            f"(from:'{self.from_time}',to:'{self.to_time}'))&"
            f"_a=(columns:!(),filters:!(('$state':(store:appState),meta:(alias:!n,disabled:!f,"
            f"field:kubernetes.namespace_name,index:'6e52cfe9-6d9e-4017-b87e-7d3e96c8295f',"
            f"key:kubernetes.namespace_name,negate:!f,params:"
            f"(query:{self.namespace}),type:phrase),query:(match_phrase:"
            f"(kubernetes.namespace_name:{self.namespace})))),"
            f"hideChart:!f,index:'6e52cfe9-6d9e-4017-b87e-7d3e96c8295f',"
            f"interval:auto,query:(language:kuery,query:''),sort:!(!('@timestamp',desc)))"
        )
