# Measure

## Overview
The `Measure` expression is an unevaluable aggregate function used within the Spark Catalyst optimizer framework. It serves as a placeholder or marker expression that preserves the data type and nullability characteristics of its child expression while being processed through query planning phases.

## Syntax
```sql
MEASURE(expression)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.catalyst.expressions.Measure
Measure(childExpression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The child expression whose characteristics are preserved by the measure wrapper |

## Return Type
The return type is identical to the data type of the child expression (`child.dataType`).

## Supported Data Types
Accepts any data type as input (`AnyDataType`), including:

- Numeric types (IntegerType, LongType, DoubleType, etc.)
- String types
- Date and timestamp types  
- Complex types (arrays, maps, structs)
- Boolean type
- Binary type

## Algorithm
The `Measure` expression follows these evaluation principles:

- Acts as a transparent wrapper around its child expression
- Preserves the exact data type of the child expression
- Maintains the nullability characteristics of the child expression
- Functions as an unevaluable aggregate that cannot be directly executed
- Uses tree pattern matching with the `MEASURE` pattern for optimizer recognition

## Partitioning Behavior
As an unevaluable aggregate function:

- Does not directly affect data partitioning during execution
- May influence partitioning decisions during query planning phases
- Behavior depends on how the optimizer transforms the expression tree

## Edge Cases

- **Null handling**: Inherits null handling behavior from the child expression (`child.nullable`)
- **Unevaluable nature**: Cannot be directly evaluated and will cause runtime errors if execution is attempted
- **Optimizer dependency**: Relies on Catalyst optimizer transformations to be replaced with evaluable expressions
- **Pattern matching**: Must be recognized and handled by appropriate optimizer rules

## Code Generation
This expression does not support code generation as it extends `UnevaluableAggregateFunc`. It is designed to be transformed or eliminated by optimizer rules before the code generation phase.

## Examples
```sql
-- Note: Direct SQL usage may not be supported as this is primarily 
-- an internal Catalyst expression
SELECT MEASURE(column_name) FROM table_name;
```

```scala
// Internal Catalyst usage example
import org.apache.spark.sql.catalyst.expressions._
import org.apache.spark.sql.types._

val childExpr = Literal(42, IntegerType)
val measureExpr = Measure(childExpr)

// The measure expression preserves child characteristics
assert(measureExpr.dataType == IntegerType)
assert(measureExpr.nullable == false)
```

## See Also

- `UnevaluableAggregateFunc` - Base class for non-evaluable aggregate expressions
- `ExpectsInputTypes` - Trait for expressions with specific input type requirements
- `UnaryLike` - Trait for expressions with a single child
- Catalyst optimizer rules that handle `MEASURE` tree patterns