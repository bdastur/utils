###############################################
# Terraglot Makefile
###############################################

BUILD_USER := 2111
BUILD_GROUP := 4111
BUILD_IMAGE ?= gobuildagent:0.1


ARCH := amd64
OS := $(shell uname -s | tr A-Z a-z)
GOOS := $(OS)
PKG := $(shell echo $$PKG)
SRC_DIRS := ./go/src


CYCLOMATIC_COMPLEXITY := 10


help:
	@echo "======================================="
	@echo "Terra glot make."
	@echo "options: "
	@echo "---------"
	@echo "make pullimage : Pull the go agent image"
	@echo "make build     : Build the terraglot binary"

pullimage:
	@echo "Pulling $(BUILD_IMAGE)"
	docker pull bdastur/gobuildagent:0.1


gocyclo: print-params pullimage
	@echo "running code checking tools..."
	@echo "Check for cyclomatic complexity > $(CYCLOMATIC_COMPLEXITY)..."
	@docker run                                                               \
		-t                                                                    \
		--rm                                                                  \
		-u $(BUILD_USER):$(BUILD_GROUP)                                       \
		-v "$$(pwd)/.go:/go"                                                  \
		-v "$$(pwd):/go/src/$(PKG)"                                           \
		-v "$$(pwd)/bin/$(ARCH):/go/bin"                                      \
		-v "$$(pwd)/bin/$(ARCH):/go/bin/$$(go env GOOS)_$(ARCH)"              \
		-v "$$(pwd)/.go/std/$(ARCH):/usr/local/go/pkg/linux_$(ARCH)_static"   \
		-e "GOPATH=/go"                                                       \
		--entrypoint /projects/bin/gocyclo                                    \
		$(BUILD_IMAGE)                                                        \
		-over $(CYCLOMATIC_COMPLEXITY) $(SRC_DIRS)




print-params:
	@echo "======================================="
	@echo "Go make - build/lint/cyclomatic complexity"
	@echo "PKG: $(PKG)"
	@echo "Build User: $(BUILD_USER):$(BUILD_GROUP)"
	@echo "GO OS: $(GOOS)"
	@echo "======================================="
