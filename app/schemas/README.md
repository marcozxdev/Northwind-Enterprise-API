# schemas/

Esquemas Pydantic para validacion y serializacion de datos. Definen la estructura de request/response de cada endpoint.

## Convenciones

- **`XxxCreate`**: Schema para crear un recurso (request body en POST)
- **`XxxUpdate`**: Schema para actualizar un recurso (request body en PUT/PATCH)
- **`XxxResponse`**: Schema de respuesta (response body)
- **`XxxList`**: Schema para respuestas paginadas

## Archivos

| Archivo | Recurso |
|---|---|
| `customers.py` | Esquemas de clientes |
| `orders.py` | Esquemas de ordenes |
| `products.py` | Esquemas de productos |
| `employees.py` | Esquemas de empleados |
| `categories.py` | Esquemas de categorias |
| `suppliers.py` | Esquemas de proveedores |
| `shippers.py` | Esquemas de transportistas |
| `regions.py` | Esquemas de regiones |
