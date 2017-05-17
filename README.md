# tf_ecs_taskdef_with_task_role

## Usage
Creates a task definition for an ECS service, with an IAM role for the task associated.

```hcl
module "taskdef" {
    source = "github.com/mergermarket/tf_ecs_taskdef_with_task_role"

    family               = "live-service-name"
    container_defintions = [
        <<END
{
    ...container definition...
}
        END
    ]

    policy = <<END
{
    ...<IAM Policy>...
}
END

}
```

## API

### Parameters

* `family` - the name of the task definition. For ECS services it is recommended to use the same name as for the service, and for that name to consist of the environment name (e.g. "live"), the comonent name (e.g. "foobar-service"), and an optional suffix (if an environment has multiple services for the component running - e.g. in a multi-tenant setup), separated by hyphens.
* `container_definitions` - list of strings. Each string should be a JSON document describing a single container definition - see https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html.
* `policy` - An IAM policy to control the task's access to AWS services - see http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html

### Outputs

* `arn` - the ARN of the task definition.
