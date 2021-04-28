#!/usr/bin/env python3

from aws_cdk import (aws_certificatemanager as cert_manager,
                     aws_cloudfront as cloudfront,
                     aws_route53 as route53,
                     aws_route53_targets as targets,
                     aws_s3 as s3,
                     aws_s3_deployment as s3_deployment,
                     core)

HOSTED_ZONE_ID = "Z15QG5MXBR7WXN"


class WebsiteStack(core.Stack):

    def __init__(self, scope: core.Construct, _id: str, domain: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        self.zone = domain
        self.web_domain = f'www.{self.zone}'
        self.web()

    def web(self):
        zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            'hosted_zone',
            hosted_zone_id=HOSTED_ZONE_ID,
            zone_name=self.zone)
        cert = cert_manager.DnsValidatedCertificate(
            self,
            'domain_cert',
            domain_name=self.zone,
            subject_alternative_names=[
                self.web_domain
            ],
            hosted_zone=zone,
            validation_method=cert_manager.ValidationMethod.DNS)
        # cert = cert_manager.Certificate.from_certificate_arn(self, 'certificateDomainForAll',
        #                                                      "arn:aws:acm:us-east-1:134764946504:certificate/f74613d7-8cc5-4de1-a2ed-467d5321839d")
        site_bucket = s3.Bucket(self, 'site_bucket',
                                bucket_name=self.web_domain,
                                website_index_document='index.html',
                                website_error_document='404.html',
                                public_read_access=True)
        core.CfnOutput(self, 'bucket_name', value=site_bucket.bucket_name)
        source_behavior = cloudfront.Behavior(
            is_default_behavior=True,
            cached_methods=cloudfront.CloudFrontAllowedCachedMethods.GET_HEAD_OPTIONS,
            allowed_methods=cloudfront.CloudFrontAllowedMethods.GET_HEAD_OPTIONS,
            compress=True)
        s3_origin_source = cloudfront.S3OriginConfig(s3_bucket_source=site_bucket)
        origin_source_config = cloudfront.SourceConfiguration(
            s3_origin_source=s3_origin_source,
            behaviors=[source_behavior])
        alias_configuration = cloudfront.AliasConfiguration(
            acm_cert_ref=cert.certificate_arn,
            names=[self.zone],
            ssl_method=cloudfront.SSLMethod.SNI,
            security_policy=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2019)

        distribution = cloudfront.CloudFrontWebDistribution(
            self, 'cf-web-distro',
            alias_configuration=alias_configuration,
            origin_configs=[origin_source_config],
            error_configurations=[
                cloudfront.CfnDistribution.CustomErrorResponseProperty(
                    error_code=404,
                    response_code=404,
                    response_page_path='/404.html'
                ),
                cloudfront.CfnDistribution.CustomErrorResponseProperty(
                    error_code=403,
                    response_code=404,
                    response_page_path='/404.html',
                )
            ],
            http_version=cloudfront.HttpVersion.HTTP2,
            viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
        )

        core.CfnOutput(self, 'Distribution ID', value=distribution.distribution_id)
        core.CfnOutput(self, 'Distribution domain name', value=distribution.domain_name)
        core.CfnOutput(self, 'SiteBucketWebsiteDomain', value=site_bucket.bucket_website_domain_name)
        # noinspection PyTypeChecker
        target_alias = route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution))
        route53.ARecord(self, 'arecord-web',
                        record_name=self.zone,
                        target=target_alias,
                        zone=zone,
                        ttl=core.Duration.minutes(60))
        s3_deployment.BucketDeployment(self, "deploy-with-invalidation",
                                       sources=[
                                           s3_deployment.Source.asset('./../website')
                                       ],
                                       destination_bucket=site_bucket,
                                       distribution=distribution,
                                       content_language='en-US',
                                       distribution_paths=['/*'])


app = core.App(auto_synth=True)
WebsiteStack(app, "jbirdDev", "jbird.dev",
             env=core.Environment(region='us-east-1'))

app.synth()
