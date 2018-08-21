package tfhelper

import (
	"bytes"
	"encoding/json"
	"fmt"
	"html/template"
	"os"
	"path"
	"strings"

	"github.com/bdastur/command"
	"github.com/bdastur/templates"
)

const (
	environments_dir = "/tmp/s3backends"
	templates_dir    = "tftemplates"
	terraform_bin    = "/usr/local/bin/terraform"
)

// func checkErr(err error, message string) {
// 	if err != nil {
// 		fmt.Printf("%s\n", message)
// 	}
// }

type ClusterSpec struct {
	Account string `json: "account"`
	Region  string `json: "region"`
}

func parseTemplate(clusterSpec ClusterSpec, templateData string) string {
	tmpl, err := template.New("spec").Parse(templateData)
	if err != nil {
		panic(err)
	}
	renderedData := new(bytes.Buffer)
	err = tmpl.Execute(renderedData, clusterSpec)
	if err != nil {
		panic(err)
	}
	return renderedData.String()
}

func getProviderDefinition(clusterSpec ClusterSpec) string {
	providerTmpl := templates.GetProviderTemplate()
	strings.Trim(providerTmpl, " ")

	renderedData := parseTemplate(clusterSpec, providerTmpl)
	return renderedData
}

func getBackendDefinition(clusterSpec ClusterSpec) string {
	backendTmpl := templates.GetBackendTemplate()
	strings.Trim(backendTmpl, " ")

	renderedData := parseTemplate(clusterSpec, backendTmpl)
	return renderedData
}

func getRemoteStateDefinition(clusterSpec ClusterSpec) string {
	remoteTmpl := templates.GetTfStateRemoteTemplate()
	strings.Trim(remoteTmpl, " ")

	renderedData := parseTemplate(clusterSpec, remoteTmpl)
	return renderedData
}

func buildClusterSpec(clusterSpecString string) (error, ClusterSpec) {
	var clusterSpec ClusterSpec

	fmt.Println("cluster spec string: ", clusterSpecString)
	jsonbytes := []byte(clusterSpecString)
	err := json.Unmarshal(jsonbytes, &clusterSpec)
	if err != nil {
		fmt.Println("Failed to Unmarsh json data: ", err)
		return nil, clusterSpec
	}

	fmt.Println("Region: ", clusterSpec.Region)
	fmt.Println("Account: ", clusterSpec.Account)

	return nil, clusterSpec
}

func setupStagingFolder(region string, account string) string {
	// Make the staging folder.
	mode := os.FileMode(0744)
	if _, err := os.Stat(environments_dir); os.IsNotExist(err) {
		os.Mkdir(environments_dir, mode)
	} else {
		fmt.Printf("Directory %s exists \n", environments_dir)
	}

	// Create a subfolder
	s := []string{region, "-", account}
	envdir_name := strings.Join(s, "")
	fmt.Printf("Env subdirname: %s \n", envdir_name)

	s3StagingFolder := path.Join(environments_dir, envdir_name)
	fmt.Printf("Staging folder: %s \n", s3StagingFolder)

	//Create staging folder.
	if _, err := os.Stat(s3StagingFolder); os.IsNotExist(err) {
		fmt.Printf("Creating new folder %s", s3StagingFolder)
		os.Mkdir(s3StagingFolder, mode)
	} else {
		fmt.Printf("Directory %s exists \n", s3StagingFolder)
	}

	return s3StagingFolder
}

func createTerraformFile(stagingFolder string, tfDefinition string) error {
	// Crete a new tf definition file in the staging environment.
	filePath := path.Join(stagingFolder, "main.tf")
	fileHandle, err := os.Create(filePath)

	count, err := fileHandle.WriteString(tfDefinition)
	if err != nil {
		fmt.Println("Failed to write data to ", filePath)
		return err
	}
	fmt.Println("Bytes written: ", count)

	return err
}

func createTemplateDefinition(clusterSpec ClusterSpec, renderBackend bool) string {
	/*
	 * Render template definitions
	 */

	// Render provider.
	providerDefinition := getProviderDefinition(clusterSpec)

	// Render Remote state.
	remoteStateDefinition := getRemoteStateDefinition(clusterSpec)

	// Render Backend.
	var s []string
	if renderBackend {
		backendDefinition := getBackendDefinition(clusterSpec)
		s = []string{providerDefinition, "\n",
			backendDefinition, "\n", remoteStateDefinition}
	} else {
		s = []string{providerDefinition, "\n", remoteStateDefinition}
	}

	// Concat definitions into a single string.
	templateDefinition := strings.Join(s, "")

	return templateDefinition
}

func deployTerraformState(s3StagingFolder string) error {
	// Terraform init.
	out, err := command.ExecuteCommand(terraform_bin, s3StagingFolder, "init")
	if err != nil {
		fmt.Println("Error executing command: ", err)
		return err
	}
	fmt.Println("out: ", out)

	// Terraform plan
	out, err = command.ExecuteCommand(terraform_bin, s3StagingFolder, "plan")
	if err != nil {
		fmt.Println("Error executing command: ", err)
		return err
	}
	fmt.Println("out: ", out)

	// Terraform apply
	out, err = command.ExecuteCommand(terraform_bin, s3StagingFolder,
		"apply", "-auto-approve")
	if err != nil {
		fmt.Println("Error executing command: ", err)
		return err
	}
	fmt.Println("out: ", out)
	return err
}

/*BootstrapEnvironment ...
 * Invoke the API to Bootstrap New AWS Environment
 */
func BootstrapEnvironment(clusterSpecString string) {
	fmt.Println("tfhelper-go")
	region := "us-west-2"
	account := "dev1"
	fmt.Printf("Account: %s, Region: %s \n", account, region)

	//Build cluster spec object.
	err, clusterSpec := buildClusterSpec(clusterSpecString)
	if err != nil {
		fmt.Println("Failed to build cluster spec!")
		return
	}
	fmt.Println("cluster Spec: ", clusterSpec)

	// Setup staging folder.
	s3StagingFolder := setupStagingFolder(clusterSpec.Region, clusterSpec.Account)
	fmt.Println("Staging fodler ready: ", s3StagingFolder)

	/*
	 * Render template definitions
	 */
	templateDefinition := createTemplateDefinition(clusterSpec, false)
	fmt.Println("Template definition: ", templateDefinition)

	//Create Terraform definition file.
	createTerraformFile(s3StagingFolder, templateDefinition)

	// Deploy terraform state.
	err = deployTerraformState(s3StagingFolder)
	if err != nil {
		fmt.Println("Failed to deploy terraform state.")
	}

}
