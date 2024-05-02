package test

import (
    "testing"

    "github.com/gruntwork-io/terratest/modules/terraform"
)

func TestTerraformValidation(t *testing.T) {
    terraformOptions := &terraform.Options{
        // Path to the Terraform code directory
        TerraformDir: "..",
    }

    // Run terraform init and terraform validate
    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndValidate(t, terraformOptions)
}