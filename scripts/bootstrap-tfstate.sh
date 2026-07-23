#!/usr/bin/env bash

set -euo pipefail

# ── Configuración ────────────────────────────────────────────────────────────
RG_STATE="rg-tfstate"          # RG dedicado al estado (NO lo toca Terraform)
LOCATION="centralus"           # misma región que el resto del proyecto
CONTAINER="tfstate"            # contenedor de blobs para el/los estados

SUFFIX="$(printf '%06x' $(( (RANDOM * RANDOM) % 16777216 )))"
STORAGE="sttfstate${SUFFIX}"

echo "==> Suscripción activa:"
az account show --query "{subscription:name, id:id}" -o table

echo "==> Creando Resource Group '${RG_STATE}' en '${LOCATION}'..."
az group create --name "${RG_STATE}" --location "${LOCATION}" -o none

echo "==> Creando Storage Account '${STORAGE}'..."
az storage account create \
  --name "${STORAGE}" \
  --resource-group "${RG_STATE}" \
  --location "${LOCATION}" \
  --sku Standard_LRS \
  --kind StorageV2 \
  --encryption-services blob \
  --min-tls-version TLS1_2 \
  --allow-blob-public-access false \
  -o none

echo "==> Obteniendo la clave de acceso de la cuenta..."
ACCOUNT_KEY="$(az storage account keys list \
  --account-name "${STORAGE}" \
  --resource-group "${RG_STATE}" \
  --query '[0].value' -o tsv)"

echo "==> Creando contenedor '${CONTAINER}'..."
az storage container create \
  --name "${CONTAINER}" \
  --account-name "${STORAGE}" \
  --account-key "${ACCOUNT_KEY}" \
  -o none

echo ""
echo "============================================================"
echo " Backend creado. Copia estos valores en terraform/backend.tf:"
echo "============================================================"
cat <<EOF

terraform {
  backend "azurerm" {
    resource_group_name  = "${RG_STATE}"
    storage_account_name = "${STORAGE}"
    container_name       = "${CONTAINER}"
    key                  = "devops-mentor.terraform.tfstate"
  }
}
EOF
echo "============================================================"
echo "Guarda el nombre del Storage Account: ${STORAGE}"
