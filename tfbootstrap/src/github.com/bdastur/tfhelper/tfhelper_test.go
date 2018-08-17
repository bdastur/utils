package tfhelper

import (
	"flag"
	"fmt"
	"testing"
)

var account = flag.String("account", "", "AWS Account Alias")
var region = flag.String("region", "", "AWS Region")

func TestBootstrapBasic(t *testing.T) {
	fmt.Println("Testing")
	BootstrapEnvironment(*region, *account)

}
