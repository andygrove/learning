# CheckOverflow

## Overview
CheckOverflow is a Spark Catalyst expression that rounds a decimal value to a specified scale and validates whether it can fit within the provided precision constraints. If the decimal cannot fit and overflow occurs, it either returns null or throws an ArithmeticException based on the nullOnOverflow parameter.

## Syntax
This is an internal Catalyst expression primarily used during query planning and optimization. It's typically inserted automatically by Spark's analyzer when decimal precision needs to be enforced.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression that evaluates to a Decimal value |
| dataType | DecimalType | Target decimal type with specific precision and scale constraints |
| nullOnOverflow | Boolean | If true, returns null on overflow; if false, throws ArithmeticException |

## Return Type
Returns a DecimalType with the precision and scale specified in the dataType parameter. The expression is always nullable regardless of the child's nullability.

## Supported Data Types
This expression specifically works with:

- Decimal input types (from child expression)
- Returns DecimalType as specified in the dataType parameter

## Algorithm
The expression evaluation follows these steps:

- Takes the input decimal value from the child expression
- Applies ROUND_HALF_UP rounding mode to adjust to target scale
- Validates if the rounded value fits within the target precision
- Returns the adjusted decimal if it fits, or null/exception based on nullOnOverflow setting
- Maintains query context information for error reporting when nullOnOverflow is false

## Partitioning Behavior
CheckOverflow is a data transformation expression that:

- Preserves partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be applied per-partition independently

## Edge Cases

- **Null Input**: If child expression returns null, CheckOverflow returns null
- **Precision Overflow**: When nullOnOverflow=true, returns null; when false, throws ArithmeticException with query context
- **Scale Adjustment**: Always rounds using ROUND_HALF_UP mode regardless of input scale
- **Error Context**: Maintains query context for meaningful error messages only when nullOnOverflow=false

## Code Generation
This expression supports Tungsten code generation through the doGenCode method. It generates optimized Java code that calls the Decimal.toPrecision method directly, avoiding interpreted evaluation overhead.

## Examples
```sql
-- CheckOverflow is typically inserted automatically by Spark
-- For example, when casting or performing decimal arithmetic:
SELECT CAST(123.456 AS DECIMAL(5,2));
-- Internally may use CheckOverflow to ensure precision/scale compliance
```

```scala
// Internal usage in Catalyst expressions
val checkOverflow = CheckOverflow(
  child = Literal(Decimal("123.456")),
  dataType = DecimalType(5, 2),
  nullOnOverflow = true
)

// DataFrame operations that may trigger CheckOverflow internally
df.select(col("decimal_col").cast(DecimalType(10, 2)))
```

## See Also

- UnaryExpression - Base class for single-child expressions
- DecimalType - Decimal data type with precision and scale
- Decimal.toPrecision - Core method for decimal precision adjustment
- SupportQueryContext - Interface for error context management