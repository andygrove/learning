# TryMod

## Overview
The `TryMod` expression performs modulo (remainder) operation on two expressions with error-safe evaluation semantics. Unlike the standard `mod` function, `try_mod` returns `NULL` instead of throwing exceptions when encountering errors such as division by zero or invalid operand types.

## Syntax
```sql
try_mod(dividend, divisor)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| dividend | Expression | The left operand (dividend) for the modulo operation |
| divisor | Expression | The right operand (divisor) for the modulo operation |

## Return Type
Returns the same numeric data type as the input operands following standard numeric type promotion rules. Returns `NULL` when errors occur during evaluation.

## Supported Data Types
- All numeric types (ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType, DecimalType)
- Non-numeric types are supported but will be wrapped in `TryEval` for error handling

## Algorithm
- For numeric operand types: Delegates to `Remainder` expression with `EvalMode.TRY` for built-in error handling
- For non-numeric operand types: Wraps standard `Remainder` operation with `TryEval` to catch ANSI mode exceptions
- Returns `NULL` when division by zero occurs or type conversion fails
- Follows standard modulo semantics: `dividend % divisor`
- Preserves sign of dividend in the result (following Scala/Java semantics)

## Partitioning Behavior
- **Preserves partitioning**: This expression does not affect data partitioning as it operates row-by-row
- **No shuffle required**: Each row can be processed independently without data movement
- Can be pushed down to individual partitions during query optimization

## Edge Cases
- **Null handling**: Returns `NULL` if either operand is `NULL`
- **Division by zero**: Returns `NULL` instead of throwing `ArithmeticException`
- **Type mismatch**: Returns `NULL` for incompatible operand types instead of compilation error
- **Overflow behavior**: Follows underlying numeric type overflow semantics but catches exceptions
- **Decimal precision**: Result precision follows standard decimal arithmetic rules

## Code Generation
This expression supports Tungsten code generation through its replacement expression:
- For numeric types: Uses `Remainder` with `EvalMode.TRY` which supports codegen
- For non-numeric types: Falls back to interpreted mode via `TryEval` wrapper
- Code generation efficiency depends on the underlying `Remainder` implementation

## Examples
```sql
-- Basic usage
SELECT try_mod(10, 3);  -- Returns 1
SELECT try_mod(10.5, 3.2);  -- Returns 0.9

-- Error handling - returns NULL instead of throwing exception
SELECT try_mod(10, 0);  -- Returns NULL (division by zero)
SELECT try_mod(NULL, 5);  -- Returns NULL

-- Type handling
SELECT try_mod('invalid', 5);  -- Returns NULL instead of error
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(expr("try_mod(col1, col2)"))

// Using TryMod expression directly
val tryModExpr = TryMod(col("dividend"), col("divisor"))
df.select(tryModExpr)
```

## See Also
- `mod()` - Standard modulo function that throws exceptions on errors
- `remainder()` - Alias for modulo operation
- `try_divide()` - Error-safe division operation
- `TryEval` - Generic wrapper for error-safe expression evaluation