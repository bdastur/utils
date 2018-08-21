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
		bucket     = "{{ .Region }}-{{ .Account }}-ilm-state"
		key     = "terraform-states/s3backends/{{ .Region }}-{{ .Account }}-ilm-state.tfstate"
		encrypt    = "true"
		dynamodb_table = "{{ .Region }}-{{ .Account }}-dynamodb-table-tf-lock"
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
