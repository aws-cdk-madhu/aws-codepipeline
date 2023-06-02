from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    Stack,
    CfnOutput,
)


class ECSService(Stack):
    def __init__(self, scope: Construct, id: str, vpc, cluster, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # L3 constructs
        fargate_service = ecs_patterns.NetworkLoadBalancedFargateService(
            self,
            "FargateService",
            cluster=cluster,
            task_image_options={
                "image": ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
            },
        )

        fargate_service.service.connections.security_groups[0].add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(80),
            description="Allow http inbound from VPC",
        )

        CfnOutput(
            self,
            "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name,
        )
        CfnOutput(self, "Service", value=fargate_service.service.service_name)