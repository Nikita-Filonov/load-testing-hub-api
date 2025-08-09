from diagrams import Cluster, Diagram
from diagrams.elastic.elasticsearch import Kibana
from diagrams.k8s.controlplane import API as K8SAPI
from diagrams.onprem.client import User
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.monitoring import Grafana
from diagrams.programming.framework import React
from diagrams.programming.language import Python

with Diagram(
        name="Load Testing Hub Architecture",
        show=False,
        filename="architecture",
        direction="LR",
        outformat="png",
):
    user = User("QA Engineer")

    with Cluster("Load Testing Hub"):
        api = Python("load-testing-hub-api")
        panel = React("load-testing-hub-panel")
        postgres = PostgreSQL("postgres")

        panel >> api
        api >> postgres

    k8dash = K8SAPI("k8dash")
    kibana = Kibana("Kibana")
    grafana = Grafana("Grafana")

    user >> panel
    api >> grafana
    api >> kibana
    api >> k8dash
