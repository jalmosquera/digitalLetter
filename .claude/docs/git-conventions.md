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
tipo: emoji descripción corta
- Detalle específico 1
- Detalle específico 2
- Detalle específico 3
- Linear issue: TEAM-123

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Tipos de commits con emojis

| Tipo | Emoji | Uso | Ejemplo |
|------|-------|-----|---------|
| `feat` | ✨ | Nueva funcionalidad | `feat: ✨ add user authentication system` |
| `fix` | 🔧 | Corrección de bugs | `fix: 🔧 correct email validation logic` |
| `docs` | 📚 | Cambios en documentación | `docs: 📚 update README with setup guide` |
| `style` | 💄 | Formato (no afecta código) | `style: 💄 format code with black` |
| `refactor` | ♻️ | Refactorización | `refactor: ♻️ simplify auth logic` |
| `test` | 🧪 | Agregar o modificar tests | `test: 🧪 add user model tests` |
| `chore` | 🔨 | Tareas de mantenimiento | `chore: 🔨 update dependencies` |
| `perf` | ⚡ | Mejoras de performance | `perf: ⚡ optimize database queries` |
| `ci` | 👷 | Cambios en CI/CD | `ci: 👷 add GitHub Actions workflow` |
| `build` | 📦 | Cambios en build | `build: 📦 update webpack config` |

### Ejemplo completo de commit

```bash
feat: ✨ add Product model with inventory management
- Create Product model with name, price, stock fields
- Add price validation (must be positive)
- Implement is_available() method
- Add stock management methods
- Configure admin interface for Product
- Linear issue: JALTEAM-42

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Reglas importantes

- ✅ Usar formato: `tipo: emoji descripción`
- ✅ Agregar bullets (-) con detalles específicos
- ✅ Mencionar Linear issue si existe
- ✅ Incluir firma de Claude Code al final
- ✅ Modo imperativo ("add" no "added")
- ✅ Primera línea máximo 72 caracteres
- ✅ Descripción clara y concisa en bullets
- ❌ No usar commits vagos como "fix", "update", "changes"
- ❌ No olvidar el emoji después del tipo

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
