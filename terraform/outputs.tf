output "vm_public_ip" {
  description = "Direccion IP publica de la maquina virtual."
  value       = azurerm_public_ip.main.ip_address
}

output "app_url" {
  description = "URL para abrir la aplicacion en el navegador."
  value       = "http://${azurerm_public_ip.main.ip_address}:${var.app_port}"
}

output "ssh_command" {
  description = "Comando para conectarse a la VM por SSH."
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.main.ip_address}"
}

output "storage_account_name" {
  description = "Nombre del Storage Account creado para las imagenes."
  value       = azurerm_storage_account.main.name
}
