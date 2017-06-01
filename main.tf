module "task_definition" {
  source                = "github.com/mergermarket/tf_ecs_task_definition?ref=PLAT-71_add_volume_2"
  family                = "${var.family}"
  container_definitions = "${var.container_definitions}"
  task_role_arn         = "${aws_iam_role.task_role.arn}"
  volume                = "${var.volume}"
}

resource "aws_iam_role_policy" "role_policy" {
  name_prefix = "${var.family}"
  role        = "${aws_iam_role.task_role.id}"
  policy      = "${var.policy}"
}

resource "aws_iam_role" "task_role" {
  name_prefix        = "${var.family}"
  assume_role_policy = "${data.aws_iam_policy_document.instance-assume-role-policy.json}"
}

data "aws_iam_policy_document" "instance-assume-role-policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}
