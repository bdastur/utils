package tfhelper

import (
	"encoding/json"
	"fmt"
	"html/template"
	"log"
	"os"
	"path"
	"path/filepath"
	"strings"

	"github.com/bdastur/templates"
)

const (
	environments_dir = "/tmp/s3backends"
	templates_dir    = "tftemplates"
)

func checkErr(err error, message string) {
	if err != nil {
		fmt.Printf("%s\n", message)
	}
}

type ClusterSpec struct {
	Region  string `json: "region"`
	Profile string `json: "account"`
}

func RenderProvider(clusterSpec ClusterSpec) {

	dir, err := filepath.Abs(filepath.Dir(os.Args[0]))
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Current working dir: ", dir)

	// fmt.Println("template file: ", template_file)
	// template_file_path := path.Join(templates_dir, template_file)

	// result, err := os.Stat(template_file_path)
	// fmt.Println("Result: ", result, "  Err: ", err)
	// data, err := ioutil.ReadFile(template_file_path)
	// fmt.Println("Data: ", string(data[:]))

	provider_tmpl := templates.GetProviderTemplate()
	fmt.Println("Provider Template: ", provider_tmpl)

	// var clusterSpec ClusterSpec
	// clusterSpec.Region = region

	tmpl, err := template.New("spec").Parse(provider_tmpl)
	if err != nil {
		panic(err)
	}

	err = tmpl.Execute(os.Stdout, clusterSpec)
	if err != nil {
		panic(err)
	}

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

	return nil, clusterSpec
}

func setupStagingFolder(region string, account string) {
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

	s3_staging_folder := path.Join(environments_dir, envdir_name)
	fmt.Printf("Staging folder: %s \n", s3_staging_folder)

	//Create staging folder.
	if _, err := os.Stat(s3_staging_folder); os.IsNotExist(err) {
		fmt.Printf("Creating new folder %s", s3_staging_folder)
		os.Mkdir(s3_staging_folder, mode)
	} else {
		fmt.Printf("Directory %s exists \n", s3_staging_folder)
	}

}

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
	fmt.Println("cluster SPec: ", clusterSpec)

	// Get cwd.
	dir, err := os.Getwd()
	if err != nil {
		fmt.Printf("Failed to get Wd.!")
	}

	fmt.Printf("Cwd: %s \n", dir)

	setupStagingFolder(clusterSpec.Region, clusterSpec.Profile)

	//Render provieder.
	RenderProvider(clusterSpec)
}
