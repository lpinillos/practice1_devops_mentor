# Guía de contribución

Este documento define **cómo se trabaja** en este repositorio: la estrategia de
ramas, el estándar de commits y el ciclo de vida de un cambio. El objetivo es que
`main` esté **siempre desplegable** y que todo cambio pase por controles de calidad
antes de llegar a producción.

---

## 1. Estrategia de ramas (Feature Branching + rama de integración)

Usamos tres niveles de ramas:

| Rama         | Rol                          | Regla                                             |
|--------------|------------------------------|---------------------------------------------------|
| `main`       | **Producción**               | Siempre estable y desplegable. Solo entra vía PR desde `dev`. |
| `dev`        | **Integración**              | Aquí se juntan y prueban todas las features. Solo entra vía PR. |
| `feature/*`  | **Trabajo del día a día**    | Ramas cortas que parten de `dev` y vuelven a `dev`. |

```
feature/xxx ──►  dev  ──►  main
  (trabajo)   (integra   (PROD:
              y prueba)  siempre arriba)
```

### Flujo de un cambio

1. Actualiza `dev`:  `git switch dev && git pull`
2. Crea tu rama:     `git switch -c feature/mi-cambio`
3. Trabaja y haz commits pequeños (ver sección 2).
4. Abre un **Pull Request** hacia `dev`.
5. El pipeline valida el PR (tests / `terraform plan`).
6. Se revisa, se aprueba y se hace **merge** a `dev`.
7. Borra la rama:    `git branch -d feature/mi-cambio`

Cuando `dev` está estable y verde, se abre un PR **`dev` → `main`** para promover
a producción. Ese es el paso extra de calidad: `main` nunca recibe código que no
haya vivido y pasado pruebas en `dev`.

### Convención de nombres de rama

| Prefijo     | Para qué                        | Ejemplo                     |
|-------------|---------------------------------|-----------------------------|
| `feature/`  | funcionalidad nueva             | `feature/app-insights`      |
| `fix/`      | corrección de bug               | `fix/requirements-encoding` |
| `chore/`    | mantenimiento / configuración   | `chore/gunicorn-dockerfile` |
| `test/`     | pruebas                         | `test/imc-unit-tests`       |
| `infra/`    | cambios de infraestructura      | `infra/remote-tfstate`      |
| `docs/`     | documentación                   | `docs/branching-strategy`   |

---

## 2. Estándar de commits (Conventional Commits)

Cada mensaje de commit sigue el formato:

```
<tipo>(<ámbito opcional>): <descripción en imperativo>
```

Tipos permitidos:

| Tipo       | Cuándo usarlo                                        |
|------------|------------------------------------------------------|
| `feat`     | nueva funcionalidad                                  |
| `fix`      | corrección de un bug                                 |
| `docs`     | solo documentación                                   |
| `test`     | agregar o corregir pruebas                           |
| `chore`    | tareas de mantenimiento (deps, config)               |
| `ci`       | cambios en pipelines / CI                            |
| `infra`    | cambios de infraestructura (Terraform)               |
| `refactor` | cambio de código que no altera comportamiento        |

Ejemplos:

```
feat(upload): validar tamaño máximo de imagen
fix(requirements): convertir archivo a UTF-8
infra(tfstate): mover el estado a Azure Storage
test(imc): agregar casos límite de categorías
```

Un cambio que rompe compatibilidad se marca con `!` y/o footer `BREAKING CHANGE:`:

```
feat(api)!: cambiar formato de respuesta de /upload
```

Este estándar nos permite (a) leer el historial de un vistazo, (b) **disparar
pipelines según el tipo de cambio** y (c) generar versiones y releases
automáticamente (ver la estrategia de tags/releases).

---

## 3. Controles de calidad (quality gates)

| Transición                | Qué se ejecuta                              |
|---------------------------|---------------------------------------------|
| `feature/*` → `dev` (PR)  | Tests unitarios + lint + `terraform plan`   |
| `dev` → `main` (PR)       | Suite completa de tests + validaciones      |

Ningún merge se hace si el pipeline está en rojo.
