# Claude Code - Agentes Personalizados

Este directorio contiene los agentes personalizados y guías para el proyecto digitalLetter.

## 📁 Estructura

```
.claude/
├── agents/          # Agentes especializados
│   ├── build.md            # Constructor de código nuevo
│   ├── project-manager.md  # Gestor del proyecto
│   ├── setup.md            # Inicializador de proyectos
│   ├── test.md             # Creador de tests
│   ├── fix.md              # Corrector de código
│   ├── review.md           # Revisor de código
│   └── doc.md              # Documentador
├── docs/            # Guías y convenciones
│   ├── documentation-guidelines.md
│   ├── git-conventions.md
│   └── testing-guidelines.md
└── README.md        # Este archivo
```

## 🤖 Agentes Disponibles

### 1. PROJECT MANAGER
**Uso:** Planificación y coordinación del proyecto
```
@project-manager Necesito planificar [descripción del proyecto]
```
- Hace preguntas sobre el proyecto
- Crea roadmap en Linear
- Genera PROJECT_CONTEXT.md
- Coordina otros agentes

### 2. SETUP
**Uso:** Inicializar estructura del proyecto
```
@setup Configura el proyecto según PROJECT_CONTEXT.md
```
- Crea estructura de carpetas
- Genera archivos de configuración
- Settings multi-entorno
- .gitignore completo

### 3. BUILD
**Uso:** Crear código nuevo
```
@build Crea modelo Product con campos name y price
@build Necesito sistema de favoritos (modo consultor)
```
- Modo EJECUCIÓN: Instrucciones claras
- Modo CONSULTOR: Ideas vagas
- Desarrollo incremental
- Una funcionalidad a la vez

### 4. REVIEW
**Uso:** Analizar y detectar problemas
```
@review Revisa el modelo Product
@review Analiza esta vista
```
- Detecta bugs y problemas
- Clasifica por severidad
- Sugiere mejoras
- NO implementa (solo analiza)

### 5. FIX
**Uso:** Implementar correcciones
```
@fix Corrige el bug en la validación
@fix Aplica las sugerencias de REVIEW
```
- Implementa correcciones
- Refactoriza código
- Optimiza performance
- NO crea funcionalidades nuevas

### 6. TEST
**Uso:** Crear tests pragmáticos
```
@test Crea tests para Product
@test Verifica cobertura del proyecto
```
- Cobertura objetivo: 60-80%
- Tests útiles y mantenibles
- NO busca 100% cobertura

### 7. DOC
**Uso:** Crear documentación concisa
```
@doc Documenta el proyecto
@doc Actualiza el README
```
- README de 200-400 líneas
- Quick Start en 5 minutos
- Bilingüe (inglés/español)
- NO documentación exhaustiva

## 🔄 Flujos de Trabajo

### Flujo 1: Nuevo Proyecto
```
1. @project-manager → Planifica el proyecto
2. @setup → Crea estructura
3. @build → Implementa features
4. @test → Crea tests
5. @doc → Documenta
```

### Flujo 2: Desarrollo de Feature
```
1. @build → Crea la feature
2. @review → Analiza el código
3. @fix → Corrige problemas
4. @test → Valida con tests
5. @doc → Actualiza docs
```

### Flujo 3: Corrección de Bug
```
1. @review → Detecta el problema
2. @fix → Implementa corrección
3. @test → Verifica con tests
```

## 📚 Guías Disponibles

### Documentation Guidelines
- Filosofía de documentación
- Estructura de README
- Qué incluir/excluir
- Bilingüismo

### Git Conventions
- Git Flow
- Convenciones de commits
- Protección de ramas
- Checklist de PR

### Testing Guidelines
- Cobertura 60-80%
- Qué testear/no testear
- Templates de tests
- Comandos útiles

## 💡 Tips de Uso

1. **Usa el agente correcto para cada tarea**
   - BUILD para crear
   - REVIEW para analizar
   - FIX para corregir
   - TEST para testear
   - DOC para documentar

2. **Flujo secuencial recomendado**
   - BUILD → REVIEW → FIX → TEST → DOC

3. **REVIEW + FIX trabajan juntos**
   - REVIEW detecta → FIX implementa

4. **BUILD tiene dos modos**
   - EJECUCIÓN: Para instrucciones claras
   - CONSULTOR: Para ideas vagas

5. **Tests pragmáticos**
   - 60-80% cobertura es suficiente

6. **Docs concisas**
   - README de 300 líneas > 10 archivos

## 🎯 Tabla de Decisión Rápida

| Necesidad | Agente |
|-----------|--------|
| Planificar proyecto | PROJECT MANAGER |
| Inicializar estructura | SETUP |
| Crear algo nuevo | BUILD |
| Revisar código | REVIEW |
| Corregir problemas | FIX |
| Crear tests | TEST |
| Documentar | DOC |

## 📖 Más Información

- Cada agente tiene su propio archivo .md con instrucciones detalladas
- Las guías en docs/ tienen convenciones y mejores prácticas
- Lee PROJECT_CONTEXT.md (cuando exista) para entender el proyecto

## 🚀 Inicio Rápido

1. **Nuevo proyecto:**
   ```
   @project-manager Quiero crear [descripción]
   ```

2. **Código existente:**
   ```
   @review Analiza [archivo/función]
   @fix Corrige [problema]
   ```

3. **Documentación:**
   ```
   @doc Documenta el proyecto
   ```

---

**Nota:** Estos agentes están diseñados para trabajar juntos de forma coordinada. Usa cada uno para su especialidad y obtén los mejores resultados.
