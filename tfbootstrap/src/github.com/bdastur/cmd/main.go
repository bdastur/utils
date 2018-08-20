package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/bdastur/tfhelper"
)

func usage() {
	usageMessage := "Usage: " + "\n" +
		"./bin/tfbootstrap create --account <account alias> --region <region> "
	fmt.Println(usageMessage)
}

func build_nested_cli(args []string) string {
	// Validate cmdline arguments.
	fmt.Println("Args: ", args)
	if len(args) <= 1 {
		fmt.Printf("Arguments not provided!")
		usage()
		os.Exit(1)
	}

	// Create.
	createOperation := flag.NewFlagSet("create", flag.ExitOnError)
	regionOption := createOperation.String("region", "", "AWS Region.")
	accountOption := createOperation.String("account", "", "AWS Account Alias")
	clusterSpecOption := createOperation.String(
		"clusterspec", "", "Provide a json formated cluster spec")

	switch args[1] {
	case "create":
		createOperation.Parse(args[2:])
	default:
		fmt.Printf("%q is not a valid command. \n", args[1])
		os.Exit(1)
	}

	if createOperation.Parsed() {
		if *regionOption == "" || *accountOption == "" || *clusterSpecOption == "" {
			fmt.Println("Region and Account are required!")
			os.Exit(1)
		}
	}
	return *clusterSpecOption
}

func main() {
	fmt.Println("Test! Build ensted cli.")
	clusterSpecString := build_nested_cli(os.Args)
	tfhelper.BootstrapEnvironment(clusterSpecString)
}
