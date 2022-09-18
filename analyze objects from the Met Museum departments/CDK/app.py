from aws_cdk import (core as cdk,
                     aws_s3 as s3,
                     aws_lambda as lambda_,
                     aws_iam as iam,
                     aws_stepfunctions as sfn,
                     aws_stepfunctions_tasks as tasks,
                     aws_glue as glue
                     )


app = cdk.App()
stack_name = "damn-stack2"
bucket_name = "damn-buckettask2"
lambda_name = "damn-getdepartmentids2"
lambda_name_2 = "damn-getobjects2"


class StepStack(cdk.Stack):
    def __init__(self, app: cdk.App, id: str) -> None:
        super().__init__(app, id)


        # Step function
        new_bucket = s3.Bucket(self, bucket_name, bucket_name=bucket_name, removal_policy=cdk.RemovalPolicy.DESTROY)

        getdepartmentids_lambda = lambda_.Function(self, lambda_name,
                    runtime=lambda_.Runtime.PYTHON_3_9,
                    code=lambda_.Code.from_asset("damn-getdepartmentids2.zip"),
                    handler="damn-getdepartmentids2.lambda_handler",
                    timeout=cdk.Duration.seconds(300),
                    memory_size=512
                    )

        getobjects_lambda = lambda_.Function(self, lambda_name_2,
                    runtime=lambda_.Runtime.PYTHON_3_9,
                    code=lambda_.Code.from_asset("damn-getobjects2.zip"),
                    handler="damn-getobjects2.lambda_handler",
                    timeout=cdk.Duration.seconds(600),
                    memory_size=512
                    )

        getdepartmentids_task = tasks.LambdaInvoke(
            self, "GetDepartmentIds",
            lambda_function=getdepartmentids_lambda,
            output_path="$.Payload"
        )

        getobjects_task = tasks.LambdaInvoke(
            self, "GetObjects",
            lambda_function=getobjects_lambda,
            output_path="$.Payload"
        )

        map = sfn.Map(self, 'Map',
                        items_path=sfn.JsonPath.string_at("$.departmentIds")
            )
        map.iterator(getobjects_task)

        definition = getdepartmentids_task \
            .next(map)
                
        state_machine = sfn.StateMachine(self, "damn-cdk-state-machine",
                                definition=definition,
                                timeout = cdk.Duration.minutes(5)
                                )

        new_bucket.grant_read_write(getobjects_lambda)



        # Glue Job
        new_job = glue.CfnJob(self,
                              "damn-etl-job",
                              name="damn-etl-job",
                              # role=glue_role.role_arn,
                              command=glue.CfnJob.JobCommandProperty(
                                  name='glueetl',
                                  python_version='3',
                                  script_location="s3://" + bucket_name + "/scripts/gluejob-teamepsilon.py"
                              ),
                              glue_version="3.0",
                              max_retries=0,
                              number_of_workers=10,
                              worker_type="G.2X"
                              )



StepStack(app, stack_name)
app.synth()