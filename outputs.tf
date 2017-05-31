output "arn" {
    value = "${module.task_definition.arn}"
}

output "task_role_arn" {
    value = "${aws_iam_role.task_role.arn}"
}
