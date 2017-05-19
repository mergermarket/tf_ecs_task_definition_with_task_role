import unittest

from subprocess import check_output, check_call
from textwrap import dedent


class TestTaskdefWithRole(unittest.TestCase):

    def setUp(self):
        check_call(['terraform', 'get', 'test/infra'])

    def test_task_definition_is_created(self):
        output = check_output(
            ['terraform', 'plan', '-no-color', 'test/infra']
        ).decode('utf-8')

        print(output)

        expected = dedent("""
            + module.taskdef_with_role.task_definition.aws_ecs_task_definition.taskdef
                arn:                   "<computed>"
                container_definitions: "a173db30ec08bc3c9ca77b5797aeae40987c1ef7"
                family:                "tf_ecs_task_def_test_family"
                network_mode:          "<computed>"
                revision:              "<computed>"
                task_role_arn:         "${var.task_role_arn}"
        """).strip()

        assert expected in output

    def test_task_role_is_created(self):
        output = check_output(
            ['terraform', 'plan', '-no-color', 'test/infra']
        ).decode('utf-8')

        expected = dedent("""
            + module.taskdef_with_role.aws_iam_role.task_role
                arn:                "<computed>"
                assume_role_policy: "{\\n  \\"Version\\": \\"2012-10-17\\",\\n  \\"Statement\\": [\\n    {\\n      \\"Sid\\": \\"\\",\\n      \\"Effect\\": \\"Allow\\",\\n      \\"Action\\": \\"sts:AssumeRole\\",\\n      \\"Principal\\": {\\n        \\"Service\\": \\"ec2.amazonaws.com\\"\\n      }\\n    }\\n  ]\\n}"
                create_date:        "<computed>"
                name:               "<computed>"
                name_prefix:        "tf_ecs_task_def_test_family"
                path:               "/"
                unique_id:          "<computed>"
        """).strip()

        assert expected in output

    def test_task_policy_is_created(self):
        output = check_output(
            ['terraform', 'plan', '-no-color', 'test/infra']
        ).decode('utf-8')

        expected = dedent("""
            + module.taskdef_with_role.aws_iam_role_policy.role_policy
                name:        "<computed>"
                name_prefix: "tf_ecs_task_def_test_family"
                policy:      "{\\n  \\"Version\\": \\"2012-10-17\\",\\n  \\"Statement\\": {\\n    \\"Effect\\": \\"Allow\\",\\n    \\"Action\\": \\"s3:ListBucket\\",\\n    \\"Resource\\": \\"arn:aws:s3:::example_bucket\\"\\n  }\\n}\\n"
                role:        "${aws_iam_role.task_role.arn}"
        """).strip()

        assert expected in output
