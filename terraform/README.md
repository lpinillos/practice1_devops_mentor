# Terraform - DevOps Mentor en Azure

Esta carpeta crea, con Terraform, la infraestructura necesaria para ejecutar la
aplicacion Flask (calculadora de IMC con subida de imagenes) en una maquina
virtual de Microsoft Azure.

## Que se crea

- Un grupo de recursos (Resource Group).
- Una red virtual con una subred.
- Una IP publica.
- Un grupo de seguridad de red (NSG) que abre el puerto 22 (SSH) y el puerto de
  la aplicacion (5000 por defecto).
- Una maquina virtual Ubuntu 22.04.
- Una cuenta de almacenamiento (Storage Account) y un contenedor de Blob para
  guardar las imagenes que sube la aplicacion.

Al arrancar, la maquina virtual instala Docker, clona el repositorio, construye
la imagen y levanta el contenedor automaticamente (mediante cloud-init).

## Archivos

- `providers.tf`: version de Terraform y proveedores de Azure.
- `variables.tf`: variables de entrada y sus valores por defecto.
- `network.tf`: red, IP publica, reglas de seguridad y tarjeta de red.
- `storage.tf`: cuenta de almacenamiento y contenedor de imagenes.
- `vm.tf`: la maquina virtual y su configuracion de arranque.
- `cloud-init.tftpl`: script que instala Docker y arranca la aplicacion.
- `outputs.tf`: datos utiles que se muestran al terminar (IP, URL, comando SSH).
- `terraform.tfvars.example`: ejemplo de valores para tus variables.

## Requisitos previos

1. Tener instalado Terraform (version 1.5 o superior).
2. Tener instalado Azure CLI e iniciar sesion con `az login`.
3. Tener una clave SSH. Si no la tienes, creala con:

   ```
   ssh-keygen -t rsa -b 4096
   ```

4. Subir el proyecto a un repositorio Git accesible (por ejemplo GitHub) y
   anotar su URL.

## Como usarlo

1. Copia el archivo de ejemplo de variables y editalo con tus datos:

   ```
   cp terraform.tfvars.example terraform.tfvars
   ```

   Cambia al menos `repo_url` por la URL de tu repositorio.

2. Inicializa Terraform:

   ```
   terraform init
   ```

3. Revisa lo que se va a crear:

   ```
   terraform plan
   ```

4. Crea la infraestructura:

   ```
   terraform apply
   ```

   Escribe `yes` cuando lo pida.

5. Al terminar, Terraform mostrara la URL de la aplicacion, la IP publica y el
   comando para conectarte por SSH. La aplicacion tarda un par de minutos en
   estar lista mientras la VM instala Docker y construye la imagen.

## Como eliminar todo

Para borrar todos los recursos y no seguir generando costos:

```
terraform destroy
```
