# tf_ecs_task_definition_with_task_role

## Usage
Creates a task definition for an ECS service, with an IAM role for the task associated.

```hcl
module "taskdef" {
    source = "github.com/mergermarket/tf_ecs_taskdef_with_task_role"

    family                = "live-service-name"
    container_definitions = [
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
* `volume` - Volume block map with 'name' and 'host_path'. 'name': The name of the volume as is referenced in the sourceVolume. 'host_path' The path on the host container instance that is presented to the container.

### Outputs

* `arn` - the ARN of the task definition.
* `task_role_arn` - the ARN of the Role for this task definition.
