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
