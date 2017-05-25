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
    description = "Volume block map with 'name' and 'host_path'. 'name': The name of the volume as is referenced in the sourceVolume. 'host_path' The path on the host container instance that is presented to the container."
    type = "map"
    default = {}
}
