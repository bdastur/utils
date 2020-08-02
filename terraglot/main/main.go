package main

import (
    "os"
    "fmt"
    "github.com/bdastur/utils/terraglot/cmd"
)

func main () {
    fmt.Println("Main. Terraglot")


    if err := cmd.TerraglotCommand().Execute(); err != nil {
        os.Exit(1)
    }

}
