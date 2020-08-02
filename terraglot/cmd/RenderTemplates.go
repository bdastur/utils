package cmd

import (
    "fmt"
    "github.com/spf13/cobra"
)

/* RenderTemplate ...
 * RenderTemplate command to render a go/hcl tmpl file to it's final .tf 
 * version.
 */
func RenderTemplates () *cobra.Command {
    cmd := & cobra.Command {
        Use: "render",
        Short: "Render a hcl/go template",
        Run: func(cmd *cobra.Command, args []string) {
            fmt.Println("Render templates")
        },
    }

    return cmd
}
