import os
import shutil
import tempfile
import unittest

from subprocess import check_call, check_output
from textwrap import dedent


class TestTaskdefWithRole(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.module_path = os.path.join(os.getcwd(), 'test', 'infra')

        check_call(
            ['terraform', 'get', self.module_path],
            cwd=self.workdir)

    def tearDown(self):
        if os.path.isdir(self.workdir):
            shutil.rmtree(self.workdir)

    def test_task_definition_is_created(self):
        output = check_output(
            ['terraform', 'plan', '-no-color', self.module_path],
            cwd=self.workdir
        ).decode('utf-8')

        expected = dedent("""
            + module.taskdef_with_role.task_definition.aws_ecs_task_definition.taskdef
                arn:                         "<computed>"
                container_definitions:       "a173db30ec08bc3c9ca77b5797aeae40987c1ef7"
                family:                      "tf_ecs_task_def_test_family"
                network_mode:                "<computed>"
                revision:                    "<computed>"
                task_role_arn:               "${var.task_role_arn}"
                volume.#:                    "1"
                volume.3039886685.host_path: "/tmp/dummy_volume"
                volume.3039886685.name:      "dummy"
        """).strip()

        assert expected in output

    def test_task_definition_passes_volume(self):
        output = check_output([
            'terraform',
            'plan', '-no-color',
            '-var', 'task_volume_param={name="data_volume",host_path="/mnt/data"}',
            self.module_path],
            cwd=self.workdir
        ).decode('utf-8')

        expected = dedent("""
            + module.taskdef_with_role.task_definition.aws_ecs_task_definition.taskdef
                arn:                       "<computed>"
                container_definitions:     "a173db30ec08bc3c9ca77b5797aeae40987c1ef7"
                family:                    "tf_ecs_task_def_test_family"
                network_mode:              "<computed>"
                revision:                  "<computed>"
                task_role_arn:             "${var.task_role_arn}"
                volume.#:                  "1"
                volume.27251535.host_path: "/mnt/data"
                volume.27251535.name:      "data_volume"
        """).strip()

        assert expected in output

    def test_task_role_is_created(self):
        output = check_output(
            ['terraform', 'plan', '-no-color', self.module_path],
            cwd=self.workdir
        ).decode('utf-8')

        expected = dedent("""
            + module.taskdef_with_role.aws_iam_role.task_role
                arn:                "<computed>"
                assume_role_policy: "{\\n  \\"Version\\": \\"2012-10-17\\",\\n  \\"Statement\\": [\\n    {\\n      \\"Sid\\": \\"\\",\\n      \\"Effect\\": \\"Allow\\",\\n      \\"Action\\": \\"sts:AssumeRole\\",\\n      \\"Principal\\": {\\n        \\"Service\\": \\"ecs-tasks.amazonaws.com\\"\\n      }\\n    }\\n  ]\\n}"
                create_date:        "<computed>"
                name:               "<computed>"
                name_prefix:        "tf_ecs_task_def_test_family"
                path:               "/"
                unique_id:          "<computed>"
        """).strip()

        assert expected in output

    def test_task_policy_is_created(self):
        output = check_output(
            ['terraform', 'plan', '-no-color', self.module_path],
            cwd=self.workdir
        ).decode('utf-8')

        expected = dedent("""
            + module.taskdef_with_role.aws_iam_role_policy.role_policy
                name:        "<computed>"
                name_prefix: "tf_ecs_task_def_test_family"
                policy:      "{\\n  \\"Version\\": \\"2012-10-17\\",\\n  \\"Statement\\": {\\n    \\"Effect\\": \\"Allow\\",\\n    \\"Action\\": \\"s3:ListBucket\\",\\n    \\"Resource\\": \\"arn:aws:s3:::example_bucket\\"\\n  }\\n}\\n"
                role:        "${aws_iam_role.task_role.id}"
        """).strip()

        assert expected in output
