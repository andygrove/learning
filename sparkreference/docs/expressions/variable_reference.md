# VariableReference

## Overview
`VariableReference` is a resolved SQL variable expression that contains complete information about a SQL variable including its catalog, identifier, and current value. It acts as a proxy to access variable values during query execution while maintaining metadata needed for operations like temporary view creation.

## Syntax
```sql
-- SQL variable reference syntax
catalog_name.namespace.variable_name
```

```scala
// Internal Catalyst expression - not directly accessible via DataFrame API
VariableReference(originalNameParts, catalog, identifier, varDef, canFold)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| originalNameParts | Seq[String] | Original name parts of the variable for temp view compatibility |
| catalog | CatalogPlugin | Catalog plugin containing the variable |
| identifier | Identifier | Qualified identifier for the variable |
| varDef | VariableDefinition | Variable definition containing current value and metadata |
| canFold | Boolean | Flag indicating if expression can be constant-folded (default: true) |

## Return Type
The return type matches the data type of the variable's current value as defined in `varDef.currentValue.dataType`.

## Supported Data Types
All data types are supported since the expression delegates to the underlying variable's literal value, which can be of any Spark SQL data type.

## Algorithm

- Resolves variable reference using catalog and identifier information
- Delegates data type and nullability to the underlying variable definition's current value
- Evaluates by returning the literal value stored in the variable definition
- Supports constant folding only when `canFold` flag is true (prevents folding during variable management operations)
- Maintains original name parts for temporary view SQL string reconstruction

## Partitioning Behavior
This expression preserves partitioning since it acts as a constant value:

- Does not affect data partitioning
- No shuffle required
- Behaves like a literal constant during execution

## Edge Cases

- Null handling: Inherits null behavior from the underlying variable's current literal value
- Variable management: When `canFold=false`, prevents constant folding during SET operations
- Temporary views: Preserves original name parts to maintain SQL compatibility when views are recreated
- Code generation: Falls back to the underlying literal's code generation implementation

## Code Generation
Supports Tungsten code generation by delegating to the underlying `varDef.currentValue.doGenCode()` method, inheriting the code generation capabilities of the variable's literal value.

## Examples
```sql
-- Setting and referencing a SQL variable
SET VAR my_catalog.my_schema.threshold = 100;
SELECT * FROM table WHERE amount > my_catalog.my_schema.threshold;
```

```scala
// Internal Catalyst usage (not public API)
val varRef = VariableReference(
  originalNameParts = Seq("my_catalog", "my_schema", "threshold"),
  catalog = catalogPlugin,
  identifier = Identifier.of(Array("my_schema"), "threshold"),
  varDef = variableDefinition,
  canFold = true
)
```

## See Also

- `VariableDefinition` - Defines variable metadata and current value
- `LeafExpression` - Base class for expressions without children
- `Literal` - Expression type used for variable values
- SQL Variables and SET command documentation