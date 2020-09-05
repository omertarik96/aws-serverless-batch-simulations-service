from aws_cdk import core, aws_lambda_event_sources
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_dynamodb as aws_dynamodb
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_batch as batch
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_iam as iam


class SimulationsServiceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        stack_role = iam.Role(
            self,
            "SimulationServiceRole",
            assumed_by=iam.ServicePrincipal("batch.amazonaws.com"),
        )

        stack_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        )

        job_role = iam.Role(
            self,
            "SimulationJobServiceRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )

        job_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        )

        lambda_role = iam.Role(
            self,
            "SimulationLambdaServiceRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        )

        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        )

        # Create Input S3
        input_bucket = s3.Bucket(self, "InputS3Bucket")

        # Create Output S3
        output_bucket = s3.Bucket(self, "OutputS3Bucket")

        # admin_policy = iam.from_policy_name("AdministratorAccess", "AdministratorAccess")

        job_table = aws_dynamodb.Table(
            self,
            id="JobTable",
            partition_key=aws_dynamodb.Attribute(
                name="PK", type=aws_dynamodb.AttributeType.STRING
            ),
            stream=aws_dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        orchestration_handler_lambda = aws_lambda.Function(
            self,
            id="JobOrchestrationHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="orchestration_handler_lambda.handler",
            code=aws_lambda.Code.asset("./simulations_service/functions/"),
        )

        # Give only write access to the post handler
        job_table.grant_write_data(orchestration_handler_lambda)

        # Pass table_name as env variable
        orchestration_handler_lambda.add_environment("TABLE_NAME", job_table.table_name)

        # Create lambda function for processing dynamodb streams
        dynamodb_streams_processor_lambda = aws_lambda.Function(
            self,
            id="JobsDynamoDBStreamsProcessor",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="dynamodb_streams_processor_lambda.handler",
            code=aws_lambda.Code.asset("./simulations_service/functions/"),
            role=lambda_role,
        )

        # Add dynamo db as lambda event source
        dynamodb_streams_processor_lambda.add_event_source(
            aws_lambda_event_sources.DynamoEventSource(
                job_table,
                starting_position=aws_lambda.StartingPosition.LATEST,
                batch_size=1,
            )
        )

        dynamodb_streams_processor_lambda.add_environment(
            "S3_OUTPUT_BUCKET", output_bucket.bucket_name
        )

        dynamodb_streams_processor_lambda.add_environment(
            "TABLE_NAME", job_table.table_name
        )

        vpc = ec2.Vpc(self, "VPC")

        spot_environment = batch.ComputeEnvironment(
            self,
            "MyComputedEnvironment",
            compute_resources={"vpc": vpc,},
            service_role=stack_role.without_policy_updates(),
        )

        job_queue = batch.JobQueue(
            self,
            "JobQueue",
            compute_environments=[
                batch.JobQueueComputeEnvironment(
                    compute_environment=spot_environment, order=1
                )
            ],
        )

        dynamodb_streams_processor_lambda.add_environment(
            "JOB_QUEUE", job_queue.job_queue_name
        )

        job_definition = batch.JobDefinition(
            self,
            "batch-job-def-from-local",
            container={
                "image": ecs.ContainerImage.from_asset("./simulations_service/job/"),
                "memory_limit_mib": 500,
                "privileged": True,
                "job_role": job_role,
            },
        )

        dynamodb_streams_processor_lambda.add_environment(
            "JOB_DEFINITION", job_definition.job_definition_name
        )

        orchestration_handler_lambda.add_event_source(
            aws_lambda_event_sources.S3EventSource(
                bucket=input_bucket, events=[s3.EventType.OBJECT_CREATED],
            )
        )

        # output_bucket.grant_put(spot_environment.service_role)
