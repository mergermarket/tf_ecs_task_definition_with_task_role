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

        check_call(['terraform', 'get', self.module_path], cwd=self.workdir)
        check_call(['terraform', 'init', self.module_path], cwd=self.workdir)

    def tearDown(self):
        if os.path.isdir(self.workdir):
            shutil.rmtree(self.workdir)

    def test_task_definition_is_created(self):
        output = check_output(
            ['terraform', 'plan', '-no-color', self.module_path],
            cwd=self.workdir
        ).decode('utf-8')
        expected = dedent("""
module.taskdef_with_role_and_assume_role.module.task_definition.aws_ecs_task_definition.taskdef
      id:                                              <computed>
      arn:                                             <computed>
      container_definitions:                           "[{\\"cpu\\":10,\\"essential\\":true,\\"image\\":\\"hello-world:latest\\",\\"memory\\":128,\\"name\\":\\"web\\"}]"
      execution_role_arn:                              "${var.execution_role_arn}"
      family:                                          "tf_ecs_task_def_test_family"
      network_mode:                                    "bridge"
      revision:                                        <computed>
      task_role_arn:                                   "${var.task_role_arn}"
      volume.#:                                        "1"
      volume.3039886685.docker_volume_configuration.#: "0"
      volume.3039886685.host_path:                     "/tmp/dummy_volume"
      volume.3039886685.name:                          "dummy"
Plan: 10 to add, 0 to change, 0 to destroy.
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
module.taskdef_with_role.module.task_definition.aws_ecs_task_definition.taskdef
      id:                                            <computed>
      arn:                                           <computed>
      container_definitions:                         "[{\\"cpu\\":10,\\"essential\\":true,\\"image\\":\\"hello-world:latest\\",\\"memory\\":128,\\"name\\":\\"web\\"}]"
      execution_role_arn:                            "${var.execution_role_arn}"
      family:                                        "tf_ecs_task_def_test_family"
      network_mode:                                  "bridge"
      revision:                                      <computed>
      task_role_arn:                                 "${var.task_role_arn}"
      volume.#:                                      "1"
      volume.27251535.docker_volume_configuration.#: "0"
      volume.27251535.host_path:                     "/mnt/data"
      volume.27251535.name:                          "data_volume"
        """).strip()
        assert expected in output

    def test_task_role_is_created(self):
        output = check_output(
            [
                'terraform',
                'plan', '-no-color',
                self.module_path],
            cwd=self.workdir
        ).decode('utf-8')

        expected = dedent("""
+ module.taskdef_with_role.aws_iam_role.task_role
      id:                                              <computed>
      arn:                                             <computed>
      assume_role_policy:                              "{\\n  \\"Version\\": \\"2012-10-17\\",\\n  \\"Statement\\": [\\n    {\\n      \\"Sid\\": \\"\\",\\n      \\"Effect\\": \\"Allow\\",\\n      \\"Action\\": \\"sts:AssumeRole\\",\\n      \\"Principal\\": {\\n        \\"Service\\": \\"ecs-tasks.amazonaws.com\\"\\n      }\\n    }\\n  ]\\n}"
      create_date:                                     <computed>
      description:                                     "Task role for tf_ecs_task_def_test_family"
      force_detach_policies:                           "false"
      max_session_duration:                            "3600"
      name:                                            <computed>
      name_prefix:                                     "tf_ecs_task_def_test_family"
      path:                                            "/"
      unique_id:                                       <computed>
        """).strip()
        assert expected in output

    def test_task_policy_is_created(self):
        output = check_output(
            ['terraform', 'plan', '-no-color', self.module_path],
            cwd=self.workdir
        ).decode('utf-8')

        expected = dedent("""
+ module.taskdef_with_role.aws_iam_role_policy.role_policy
      id:                                              <computed>
      name:                                            <computed>
      name_prefix:                                     "tf_ecs_task_def_test_family"
      policy:                                          "{\\n  \\"Version\\": \\"2012-10-17\\",\\n  \\"Statement\\": {\\n    \\"Effect\\": \\"Allow\\",\\n    \\"Action\\": \\"s3:ListBucket\\",\\n    \\"Resource\\": \\"arn:aws:s3:::example_bucket\\"\\n  }\\n}\\n"
      role:                                            "${aws_iam_role.task_role.id}"
        """).strip()

        assert expected in output

    def test_task_definition_is_created_when_long_family_name(self):

        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-var', 'family_param=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            self.module_path
        ], cwd=self.workdir
        ).decode('utf-8')

        expected = dedent("""
+ module.taskdef_with_role.aws_iam_role.task_role
      id:                                              <computed>
      arn:                                             <computed>
      assume_role_policy:                              "{\\n  \\"Version\\": \\"2012-10-17\\",\\n  \\"Statement\\": [\\n    {\\n      \\"Sid\\": \\"\\",\\n      \\"Effect\\": \\"Allow\\",\\n      \\"Action\\": \\"sts:AssumeRole\\",\\n      \\"Principal\\": {\\n        \\"Service\\": \\"ecs-tasks.amazonaws.com\\"\\n      }\\n    }\\n  ]\\n}"
      create_date:                                     <computed>
      description:                                     "Task role for aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
      force_detach_policies:                           "false"
      max_session_duration:                            "3600"
      name:                                            <computed>
      name_prefix:                                     "aaaaaaaaaaaaaaaaaaaaaaaatf2368"
      path:                                            "/"
      unique_id:                                       <computed>
        """).strip()
        assert expected in output

    def test_task_role_is_created_with_custom_assume_role_policy(self):
        output = check_output(
            [
                'terraform',
                'plan', '-no-color',
                self.module_path],
            cwd=self.workdir
        ).decode('utf-8')

        print ("============================================================")
        print (output)
        print ("============================================================")
        expected = dedent("""
+ module.taskdef_with_role_and_assume_role.aws_iam_role.task_role
      id:                                              <computed>
      arn:                                             <computed>
      assume_role_policy:                              "{\\n  \\"Version\\": \\"2012-10-17\\",\\n  \\"Statement\\": [\\n    {\\n      \\"Sid\\": \\"\\",\\n      \\"Effect\\": \\"Allow\\",\\n      \\"Action\\": \\"sts:AssumeRole\\",\\n      \\"Principal\\": {\\n        \\"Service\\": [\\n          \\"ecs.amazonaws.com\\",\\n          \\"ecs-tasks.amazonaws.com\\",\\n          \\"ec2.amazonaws.com\\",\\n          \\"autoscaling.amazonaws.com\\"\\n        ]\\n      }\\n    },\\n    {\\n      \\"Sid\\": \\"\\",\\n      \\"Effect\\": \\"Allow\\",\\n      \\"Action\\": \\"sts:AssumeRole\\",\\n      \\"Principal\\": {\\n        \\"AWS\\": [\\n          \\"arn:aws:iam::733578946173:role/autoscaler\\",\\n          \\"arn:aws:iam::371640587010:role/autoscaler\\"\\n        ]\\n      }\\n    }\\n  ]\\n}"
      create_date:                                     <computed>
      description:                                     "Task role for tf_ecs_task_def_test_family"
      force_detach_policies:                           "false"
      max_session_duration:                            "3600"
      name:                                            <computed>
      name_prefix:                                     "tf_ecs_task_def_test_family"
      path:                                            "/"
      unique_id:                                       <computed>
        """).strip()
        assert expected in output
