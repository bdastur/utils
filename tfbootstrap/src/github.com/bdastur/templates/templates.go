package templates

const (
	/* Provider template */
	providerTemplate = `
provider "aws" {
	region  = "{{ .Region }}"
}
`

	/* Terraform Backend */
	backendTemplate = `
terraform {
	required_version = ">= v0.11.7"
	backend "s3" {
		region     = "{{ .Region }}"
		profile    = "{{ .Profile }}"
		bucket     = "{{ .Region }}-{{ .Profile }}-ilm-state"
		key     = "/terraform-states/s3backends/{{ .Region }}-{{ .Profile }}-ilm-state.tfstate"
		encrypt    = "true"
		dynamodb_table = "{{ .Region }}-{{ .Profile }}-dynamodb-table-tf-lock"
		acl        = "bucket-owner-full-control"
	}
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
