module "task_definition" {
  source                = "github.com/mergermarket/tf_ecs_task_definition?ref=secrets"
  family                = "${var.family}"
  container_definitions = "${var.container_definitions}"
  task_role_arn         = "${aws_iam_role.task_role.arn}"
  execution_role_arn    = "${aws_iam_role.ecs_tasks_execution_role.arn}"
  volume                = "${var.volume}"
}

resource "aws_iam_role_policy" "role_policy" {
  name_prefix = "${var.family}"
  role        = "${aws_iam_role.task_role.id}"
  policy      = "${var.policy}"
}

resource "aws_iam_role" "task_role" {
  name_prefix = "${
    length(var.family) <= 32 ?
      var.family :
      format("%.24stf%.4s", var.family, sha1(var.family))
  }"

  assume_role_policy = "${
    var.assume_role_policy == "" ?
      data.aws_iam_policy_document.instance-assume-role-policy.json :
      var.assume_role_policy
  }"
}

data "aws_iam_policy_document" "instance-assume-role-policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_tasks_execution_role" {
  name               = "${var.family}-execution-role"
  assume_role_policy = "${data.aws_iam_policy_document.instance-assume-role-policy.json}"
}

locals {
  team      = "${lookup(var.release, "team", "")}"
  component = "${lookup(var.release, "component", "")}"
}

resource "aws_iam_role_policy" "execution_role_policy" {
  role = "${aws_iam_role.ecs_tasks_execution_role.id}"
  name = "role_policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
          "Effect": "Allow",
          "Action": [
              "ecr:GetAuthorizationToken",
              "ecr:BatchCheckLayerAvailability",
              "ecr:GetDownloadUrlForLayer",
              "ecr:BatchGetImage",
              "logs:CreateLogStream",
              "logs:PutLogEvents"
          ],
          "Resource": "*"
      },
      {
          "Sid": "",
          "Effect": "Allow",
          "Action": [
              "secretsmanager:List*",
              "secretsmanager:DescribeSecret"
          ],
          "Resource": "*"
      },
      {
          "Sid": "",
          "Effect": "Allow",
          "Action": "secretsmanager:GetSecretValue",
          "Resource": "arn:aws:secretsmanager:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:secret:common/*"
      },
      {
          "Sid": "",
          "Effect": "Allow",
          "Action": "secretsmanager:GetSecretValue",
          "Resource": "arn:aws:secretsmanager:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:secret:${local.team}/${var.env}/${local.component}/*"
      }
    ]
}
EOF
}
