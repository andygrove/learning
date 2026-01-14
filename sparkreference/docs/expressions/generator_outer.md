# GeneratorOuter

## Overview
GeneratorOuter is a wrapper expression around another generator that specifies outer behavior for generator functions. It is primarily used to implement SQL functions like `explode_outer` and gets replaced during the analysis phase of query planning.

## Syntax
```sql
-- Used internally to implement functions like:
SELECT explode_outer(array_column) FROM table_name
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Generator | The underlying generator expression to be wrapped with outer behavior |

## Return Type
Returns the same element schema as the wrapped child generator (`StructType`).

## Supported Data Types
Supports any data types that the underlying child generator supports, as this is purely a wrapper expression.

## Algorithm

- Wraps an existing Generator expression to modify its behavior to outer semantics

- Acts as a placeholder during query analysis and planning phases

- Delegates element schema determination to the wrapped child generator

- Gets replaced with appropriate implementation during analysis, never executed directly

- Maintains the same structural properties as the underlying generator

## Partitioning Behavior
Partitioning behavior depends entirely on the wrapped child generator since this expression is replaced during analysis:

- Does not directly affect partitioning as it's not executed

- Final partitioning behavior determined by the replacement expression created during analysis

## Edge Cases

- Cannot be evaluated directly - throws `QueryExecutionErrors.cannotEvaluateExpressionError`

- Cannot generate code - throws `QueryExecutionErrors.cannotGenerateCodeForExpressionError`

- Always reports as unresolved (`resolved = false`) to ensure analysis phase processing

- Null handling depends on the replacement expression created during analysis

## Code Generation
This expression does not support code generation and will throw an error if code generation is attempted, as it should be replaced during analysis before reaching the code generation phase.

## Examples
```sql
-- This expression is used internally for:
SELECT explode_outer(ARRAY(1, 2, 3)) as value;
SELECT posexplode_outer(ARRAY('a', 'b')) as (pos, value);
```

```scala
// Internal usage during analysis phase
// Not directly accessible via DataFrame API
// Gets created when parsing outer generator functions
```

## See Also

- `Generator` - Base trait for generator expressions
- `Explode` - Standard explode generator implementation
- `PosExplode` - Position-aware explode generator
- `UnaryExpression` - Base class for single-child expressions