package templates

const (
	/* Provider template */
	providerTemplate = `
provider "aws" {
	region  = "{{ .Region }}"
	profile = "{{ .Account }}"
}
`

	/* Terraform Backend */
	backendTemplate = `
terraform {
	required_version = ">= v0.11.7"
	backend "s3" {
		region     = "{{ .Region }}"
		profile    = "{{ .Account }}"
		bucket     = "{{ .Region }}-{{ .Account }}-tfstate-state"
		key     = "terraform-states/s3backends/{{ .Region }}-{{ .Account }}-tfstate-state.tfstate"
		encrypt    = "true"
		dynamodb_table = "{{ .Region }}-{{ .Account }}-dynamodb-table-tf-lock"
		acl        = "bucket-owner-full-control"
	}
}
`
/ * TF State S3 Backend Definition */
	tfstateBackendTemplate = `
	resource "aws_dynamodb_table" "terraform_statelock" {
		name           = "{{ .Region }}-{{ .Account }}-dynamodb-table-tf-lock"
		read_capacity  = 1 
		write_capacity = 1
		hash_key       = "LockID"
	
		attribute {
			name = "LockID"
			type = "S"
		}
	
		lifecycle {
			prevent_destroy = false
		}
	}
	
	resource "aws_s3_bucket" "tfstate_state_bucket" {
	  bucket = "{{ .Region }}-{{ .Account }}-tfstate-state"
	
	}
	
	`
)

/*
 * Return the provider template
 */
func GetProviderTemplate() string {
	return providerTemplate
}

/* Return Backend template */
func GetBackendTemplate() string {
	return backendTemplate
}
