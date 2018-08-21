package command

import (
	"bytes"
	"fmt"
	"os/exec"
)

func ExecuteCommand(cmdName string, cwd string, cmdArgs ...string) (string, error) {
	cmd := exec.Command(cmdName, cmdArgs...)
	cmd.Dir = cwd

	var stderr bytes.Buffer
	cmd.Stderr = &stderr

	out, err := cmd.Output()
	if err != nil {
		fmt.Printf("Command [%s %s] failed due to %s, %s [%s]",
			cmdName, cmdArgs, err, string(out), stderr.String())
	}
	return string(out), err
}
