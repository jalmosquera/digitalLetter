# Git Conventions & Workflow

## 🔄 Git Flow

### Estructura de ramas

```
main (producción)
  ↑
  PR + CI/CD
  ↑
develop (integración)
  ↑
  PR + CI/CD
  ↑
feature/* (desarrollo)
```

### Flujo completo

1. **Crear rama develop** (solo una vez al inicio)
   ```bash
   git checkout -b develop
   git push origin develop
   ```

2. **Nueva feature**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/nombre-descriptivo
   ```

3. **Desarrollar y testear**
   ```bash
   # Desarrollar código
   python manage.py test  # Testear localmente
   git add .
   git commit -m "tipo: descripción"
   python manage.py test  # Test final antes de push
   git push origin feature/nombre-descriptivo
   ```

4. **Pull Request: feature → develop**
   - Crear PR en GitHub
   - CI/CD corre tests automáticamente
   - Si pasa ✅ → Aprobar y hacer merge
   - Borrar rama feature

5. **Actualizar local después del merge**
   ```bash
   git checkout develop
   git pull origin develop
   git branch -d feature/nombre-descriptivo
   ```

6. **Pull Request: develop → main** (cuando esté listo para producción)
   - Crear PR en GitHub
   - CI/CD corre tests completos
   - Si pasa ✅ → Aprobar y hacer merge a main

## 📝 Convenciones de Commits

### Formato estándar

```
tipo(scope): descripción corta

Cuerpo opcional con más detalles

Footer opcional (issues, breaking changes)
```

### Tipos de commits

| Tipo | Uso | Ejemplo |
|------|-----|---------|
| `feat` | Nueva funcionalidad | `feat: agregar sistema de login` |
| `fix` | Corrección de bugs | `fix: corregir validación de email` |
| `docs` | Cambios en documentación | `docs: actualizar README` |
| `style` | Formato (no afecta código) | `style: formatear código con black` |
| `refactor` | Refactorización | `refactor: simplificar lógica de auth` |
| `test` | Agregar o modificar tests | `test: agregar tests para usuario` |
| `chore` | Tareas de mantenimiento | `chore: actualizar dependencias` |
| `perf` | Mejoras de performance | `perf: optimizar query de DB` |
| `ci` | Cambios en CI/CD | `ci: agregar GitHub Actions` |
| `build` | Cambios en build | `build: actualizar webpack config` |

### Reglas importantes

- ✅ Usar minúsculas
- ✅ Modo imperativo ("agregar" no "agregado")
- ✅ Sin punto al final
- ✅ Máximo 50 caracteres en la primera línea
- ✅ Descripción clara y concisa
- ❌ No usar commits vagos como "fix", "update", "changes"

## 🛡️ Protección de ramas

### Configuración recomendada en GitHub

**Rama `main`:**
- ✅ Require pull request reviews
- ✅ Require status checks to pass (CI/CD)
- ✅ No permitir push directo
- ✅ Require linear history

**Rama `develop`:**
- ✅ Require pull request reviews
- ✅ Require status checks to pass (CI/CD)
- ✅ No permitir push directo

## 🔥 Casos especiales

### Hotfix (bug crítico en producción)

```bash
git checkout main
git pull origin main
git checkout -b hotfix/nombre-del-fix
# Arreglar y testear
git push origin hotfix/nombre-del-fix
# PR directo a main (y también a develop después)
```

### Nombres de ramas convencionales

- `feature/nombre` - Nueva funcionalidad
- `bugfix/nombre` - Corrección de bugs
- `hotfix/nombre` - Corrección urgente en producción
- `refactor/nombre` - Refactorización
- `docs/nombre` - Solo documentación

## 📋 Checklist antes de hacer PR

- [ ] Tests locales pasan
- [ ] Código formateado (black, prettier, etc)
- [ ] Sin console.log o prints de debug
- [ ] Sin archivos temporales
- [ ] `.env` no está en el commit
- [ ] requirements.txt actualizado (si agregaste dependencias)
- [ ] Commit messages siguiendo convenciones
- [ ] Branch actualizada con develop

## 🚫 Errores comunes a evitar

- ❌ Push directo a `main` o `develop`
- ❌ Commits con mensajes vagos
- ❌ Mergear sin que pasen los tests del CI/CD
- ❌ No actualizar rama local después de merge
- ❌ No borrar ramas feature después de merge
- ❌ Commitear archivos de configuración local (.env, .vscode)
- ❌ Hacer commits muy grandes

## 💡 Tips

- Haz commits frecuentes y pequeños
- Un commit = una funcionalidad/fix
- Haz pull de develop antes de crear nueva feature
- Usa `.gitignore` apropiadamente
- Borra ramas locales después de merge para mantener limpio
