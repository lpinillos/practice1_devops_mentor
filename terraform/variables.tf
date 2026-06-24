variable "project_name" {
  type        = string
  description = "Nombre corto del proyecto. Se usa como prefijo para nombrar los recursos."
  default     = "devopsmentor"
}

variable "location" {
  type        = string
  description = "Region de Azure donde se crean los recursos."
  default     = "East US"
}

variable "vm_size" {
  type        = string
  description = "Tamano (SKU) de la maquina virtual."
  default     = "Standard_B1s"
}

variable "admin_username" {
  type        = string
  description = "Usuario administrador de la maquina virtual."
  default     = "azureuser"
}

variable "ssh_public_key_path" {
  type        = string
  description = "Ruta a tu clave publica SSH para entrar a la VM."
  default     = "~/.ssh/id_rsa.pub"
}

variable "repo_url" {
  type        = string
  description = "URL del repositorio Git que contiene la aplicacion."
}

variable "app_port" {
  type        = number
  description = "Puerto en el que escucha la aplicacion Flask."
  default     = 5000
}

variable "blob_container_name" {
  type        = string
  description = "Nombre del contenedor de Blob Storage para las imagenes."
  default     = "imagenes"
}
