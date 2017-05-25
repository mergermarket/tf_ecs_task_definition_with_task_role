provider "aws" {
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_get_ec2_platforms      = true
  skip_region_validation      = true
  skip_requesting_account_id  = true
  max_retries                 = 1
  access_key                  = "a"
  secret_key                  = "a"
  region                      = "eu-west-1"
}

variable "task_volume_param" {
    description = "Allow the test to pass this in"
    type = "map"
    default = {}
}

module "taskdef_with_role" {
    source = "../.."

    family                = "tf_ecs_task_def_test_family"
    container_definitions = [
        <<END
{
  "name": "web",
  "image": "hello-world:latest",
  "cpu": 10,
  "memory": 128,
  "essential": true
}
END
    ]
    policy                = <<END
{
  "Version": "2012-10-17",
  "Statement": {
    "Effect": "Allow",
    "Action": "s3:ListBucket",
    "Resource": "arn:aws:s3:::example_bucket"
  }
}
END

    volume = "${var.task_volume_param}"
}
