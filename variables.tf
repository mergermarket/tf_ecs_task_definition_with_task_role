variable "env" {
  description = "Environment name"
  default     = ""
}

variable "release" {
  type        = "map"
  description = "Metadata about the release"
  default     = {}
}

variable "family" {
  description = "A unique name for your task defintion."
  type        = "string"
}

variable "container_definitions" {
  description = "A list of valid container definitions provided as a single valid JSON document."
  type        = "list"
}

variable "policy" {
  description = "A valid IAM policy for the task"
  type        = "string"
}

variable "volume" {
  description = "Volume block map with 'name' and 'host_path'."
  type        = "map"
  default     = {}
}

variable "assume_role_policy" {
  description = "A valid IAM policy for assuming roles - optional"
  type        = "string"
  default     = ""
}

variable "is_test" {
  description = "For testing only. Stops the call to AWS for sts"
  default     = false
}

variable "network_mode" {
  description = "Network mode valid values are: none, bridge, awsvpc, and host. Default is bridge (See: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html)"
  type        = "string"
  default     = "bridge"
}
