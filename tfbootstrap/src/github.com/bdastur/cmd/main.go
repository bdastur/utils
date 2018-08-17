package main

import (
	"fmt"
	"flag"
	"github.com/bdastur/tfhelper"
	"os"
)

func usage() {
	usageMessage := "Usage: " + "\n" +
		"./bin/tfbootstrap create --account <account alias> --region <region> "
	fmt.Println(usageMessage)
}


func build_nested_cli(args []string) {
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

	switch args[1] {
	case "create":
		createOperation.Parse(args[2:])
	default:
		fmt.Printf("%q is not a valid command. \n", args[1])
		os.Exit(1)
	}

	if createOperation.Parsed() {
		if *regionOption == "" || *accountOption == "" {
			fmt.Println("Region and Account are required!")
			os.Exit(1)
		}
	}

}

func main() {
	fmt.Println("Test! Build ensted cli.")
	build_nested_cli(os.Args)
	tfhelper.BootstrapEnvironment("us-west-2", "dev1")
}
