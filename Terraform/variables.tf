variable "region" {
  description = "Region to use in aws"
  type        = string
  default     = "il-central-1" 
}

variable "subnet_ids" {
  description = "list of subnet ids"
  type = list
  default = []
  
}

