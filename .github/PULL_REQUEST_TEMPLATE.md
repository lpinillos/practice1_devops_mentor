<!--
  Antes de abrir el PR, revisa la guía en CONTRIBUTING.md.
  Recuerda: los commits deben seguir Conventional Commits
  (feat, fix, docs, test, chore, ci, infra, refactor).
-->

## Descripción

<!-- ¿Qué cambia y por qué? Explica el contexto en 1-3 frases. -->


## Tipo de cambio

<!-- Marca con una X lo que aplique. Esto define qué pipeline debería correr. -->

- [ ] `feat` — nueva funcionalidad (código de la app)
- [ ] `fix` — corrección de un bug
- [ ] `infra` — cambio de infraestructura (Terraform)
- [ ] `test` — pruebas
- [ ] `docs` — solo documentación
- [ ] `chore` / `ci` — mantenimiento o pipelines
- [ ] `refactor` — cambio interno sin alterar comportamiento

## ¿Qué toca este PR?

- [ ] Código de la aplicación (`app.py`, `templates/`, `Dockerfile`, `requirements.txt`)
- [ ] Infraestructura (`terraform/`)
- [ ] Documentación / configuración

## Rama destino

- [ ] `dev` (integración — flujo normal de una feature)
- [ ] `main` (promoción a producción desde `dev`)

## Checklist

- [ ] Los commits siguen Conventional Commits.
- [ ] La rama parte de `dev` y sigue la convención de nombres (`feature/`, `fix/`, `infra/`, ...).
- [ ] Si toca código: se agregaron o actualizaron pruebas.
- [ ] Si toca infra: revisé el `terraform plan` del pipeline.
- [ ] El pipeline del PR está en verde.

## Notas para el revisor

<!-- Cualquier cosa que el mentor deba saber al revisar. -->
