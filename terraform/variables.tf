variable "project_name" {
  description = "The name of the Google Cloud Project"
  type        = string
  default     = "ai-list-assist-collab"
}

variable "org_id" {
  description = "The organization ID."
  type        = string
}

variable "billing_account" {
  description = "The ID of the billing account to associate this project with."
  type        = string
}

variable "folder_id" {
  description = "The ID of a folder to host this project"
  type        = string
  default     = ""
}

variable "region" {
  description = "The region to deploy resources in"
  type        = string
  default     = "us-central1"
}
