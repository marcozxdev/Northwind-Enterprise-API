# tests/

Tests unitarios y de integracion para la API.

## Estructura

- `conftest.py` - Fixtures compartidos (cliente de prueba, sesion de BD mock, datos de ejemplo).
- `test_*.py` - Tests por recurso, siguiendo la misma estructura que `routers/`.

## Ejecucion

```bash
pytest
```
