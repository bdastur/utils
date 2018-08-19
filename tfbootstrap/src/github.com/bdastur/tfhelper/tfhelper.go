package tfhelper

import (
	"fmt"
	"os"
	"path"
	"strings"
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

func BootstrapEnvironment(region string, account string) {
	fmt.Println("tfhelper-go")
	fmt.Printf("Account: %s, Region: %s \n", account, region)

	// Get cwd.
	dir, err := os.Getwd()
	if err != nil {
		fmt.Printf("Failed to get Wd.!")
	}

	fmt.Printf("Cwd: %s \n", dir)

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
