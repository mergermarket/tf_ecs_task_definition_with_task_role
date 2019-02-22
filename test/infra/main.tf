provider "aws" {
  version                     = "~> 1.16"
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
  description = "The test can set this var to be passed to the module"
  type        = "map"
  default     = {}
}

variable "family_param" {
  description = "The test can set this var to be passed to the module"
  default     = "tf_ecs_task_def_test_family"
}

variable "assume_role_policy" {
  description = "A valid IAM policy for assuming roles - optional"
  type        = "string"
  default     = ""
}

variable "release" {
  type        = "map"
  description = "Metadata about the release"
  default     = {}
}

variable "env" {
  description = "Environment name"
  default     = ""
}

module "taskdef_with_role" {
  source = "../.."

  family = "${var.family_param}"

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
    ,
  ]

  policy = <<END
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

module "taskdef_with_role_and_assume_role" {
  source = "../.."

  family = "${var.family_param}"

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
    ,
  ]

  policy = <<END
{
  "Version": "2012-10-17",
  "Statement": {
    "Effect": "Allow",
    "Action": "s3:ListBucket",
    "Resource": "arn:aws:s3:::example_bucket"
  }
}
END

  volume             = "${var.task_volume_param}"
  assume_role_policy = "${data.aws_iam_policy_document.assume-role-policy.json}"
}

data "aws_iam_policy_document" "assume-role-policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type = "Service"

      identifiers = [
        "ecs-tasks.amazonaws.com",
        "ec2.amazonaws.com",
        "ecs.amazonaws.com",
        "autoscaling.amazonaws.com",
      ]
    }
  }

  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type = "AWS"

      identifiers = [
        "arn:aws:iam::371640587010:role/autoscaler",
        "arn:aws:iam::733578946173:role/autoscaler",
      ]
    }
  }
}
