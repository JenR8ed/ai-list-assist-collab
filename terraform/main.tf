module "project-factory" {
  source  = "terraform-google-modules/project-factory/google"
  version = "~> 17.0"

  name              = var.project_name
  random_project_id = true
  org_id            = var.org_id
  billing_account   = var.billing_account
  folder_id         = var.folder_id

  # Add essential APIs that you might need
  activate_apis = [
    "compute.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "serviceusage.googleapis.com"
  ]
}

output "project_id" {
  value       = module.project-factory.project_id
  description = "The ID of the created project"
}

output "project_name" {
  value       = module.project-factory.project_name
  description = "The assigned name of the created project"
}

output "project_number" {
  value       = module.project-factory.project_number
  description = "The numeric ID of the created project"
}
