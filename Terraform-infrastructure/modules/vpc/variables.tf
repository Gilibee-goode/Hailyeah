variable "region" {
  description = "Region to use in aws"
  type        = string
  # default     = var.provider_region
}

# variable "availability_zone" {
#   description = "AZ to use in aws"
#   type        = string
#   default     = "il-central-1a" 
# }

variable "vpc_name" {
  description = "vpc name"
  type        = string
  default     = "mah-vpc" 
}
