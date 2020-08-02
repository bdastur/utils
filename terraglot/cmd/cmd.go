package cmd


import (
    "fmt"
    "github.com/spf13/cobra"
)


func TerraglotCommand() *cobra.Command {
        cmd := &cobra.Command{
                Use:   "terraglot",
                Short: "",
                Long:  ``,
                Run:   runHelp,
        }

        cmd.AddCommand(RenderTemplates())

        return cmd
}


func runHelp(cmd *cobra.Command, args []string) {
    fmt.Println("Run help called")
    cmd.Help()
}

