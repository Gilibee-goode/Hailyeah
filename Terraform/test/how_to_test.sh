#!/bin/bash

go mod init tf_test.go

go mod tidy

 go test -v -timeout 30m

