resource "random_string" "storage_suffix" {
  length  = 6
  upper   = false
  special = false
}

resource "azurerm_storage_account" "main" {
  name                     = "${var.project_name}${random_string.storage_suffix.result}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "images" {
  name                  = var.blob_container_name
  storage_account_id    = azurerm_storage_account.main.id
  container_access_type = "private"
}
