# Backend remoto de Terraform: el estado (tfstate) vive en Azure Storage,
# no en tu disco local. Esto habilita colaboración, bloqueo automático
# (blob lease), durabilidad y almacenamiento seguro de secretos.
#
# El Storage Account y el contenedor se crean UNA vez con scripts/bootstrap-tfstate.sh
# (fuera de Terraform), en un Resource Group SEPARADO del que Terraform administra.
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate"
    storage_account_name = "sttfstatebf4b6d"
    container_name       = "tfstate"
    key                  = "devops-mentor.terraform.tfstate"
  }
}
