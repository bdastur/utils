package command

import (
	"fmt"
	"os/exec"
)

func ExecuteCommand(cmdName string, cwd string, cmdArgs ...string) (string, error) {
	cmd := exec.Command(cmdName, cmdArgs...)
	cmd.Dir = cwd

	out, err := cmd.Output()
	if err != nil {
		fmt.Printf("Command [%s %s] failed due to %s", cmdName, cmdArgs, err, string(out))
	}
	return string(out), err
}
