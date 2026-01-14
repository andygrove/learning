# TryAdd

## Overview
TryAdd is a Spark Catalyst expression that performs addition operations with error handling, returning null instead of throwing exceptions when overflow or other arithmetic errors occur. It serves as a runtime-replaceable wrapper that adapts its behavior based on input data types, using either direct arithmetic operations or TryEval wrapping for different scenarios.

## Syntax
```sql
try_add(expr1, expr2)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("try_add(col1, col2)"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | Left operand for the addition operation |
| right | Expression | Right operand for the addition operation |
| replacement | Expression | Internal replacement expression that performs the actual computation |

## Return Type
Returns the same numeric type as would be returned by standard addition, following Spark's type promotion rules. Returns null when arithmetic errors occur instead of throwing exceptions.

## Supported Data Types
- **Numeric Types**: All numeric types (ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType, DecimalType)
- **Date/Time Types**: Supported through TryEval wrapping (future direct support planned based on TODO comment)
- **Type Promotion**: Follows standard Spark arithmetic type promotion rules

## Algorithm
- Extends `RuntimeReplaceable`, meaning it gets replaced during analysis phase with actual implementation
- For numeric types: Creates `Add(left, right, EvalMode.TRY)` for direct try-mode evaluation
- For non-numeric types: Wraps standard ANSI-mode addition with `TryEval` for error handling
- Inherits analysis rules from child expressions through `InheritAnalysisRules`
- Replacement expression handles the actual computation logic

## Partitioning Behavior
- **Preserves Partitioning**: Yes, as it's a deterministic row-level operation
- **Requires Shuffle**: No, operates on individual rows without requiring data movement
- **Partition-wise Operation**: Can be executed independently on each partition

## Edge Cases
- **Null Handling**: Returns null if either operand is null (standard SQL null propagation)
- **Overflow Behavior**: Returns null instead of throwing overflow exceptions (key difference from regular addition)
- **Type Mismatch**: Handled during analysis phase with appropriate type promotion or error reporting
- **Underflow Behavior**: Returns null for underflow conditions in try-mode evaluation

## Code Generation
This expression supports Spark's Tungsten code generation through its replacement expressions:
- Numeric operations with `EvalMode.TRY` generate optimized code with null-return error handling
- TryEval-wrapped expressions fall back to interpreted mode for the error handling wrapper
- Code generation efficiency depends on the underlying replacement expression type

## Examples
```sql
-- Basic numeric addition with overflow protection
SELECT try_add(2147483647, 1) as result;  -- Returns null instead of overflow error

-- Handling null inputs
SELECT try_add(null, 5) as result;  -- Returns null

-- Decimal precision handling
SELECT try_add(CAST(999.99 AS DECIMAL(5,2)), CAST(0.01 AS DECIMAL(5,2))) as result;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic usage
df.select(expr("try_add(salary, bonus)").alias("total_compensation"))

// Handling potential overflows in aggregations
df.select(expr("try_add(very_large_number, increment)").alias("safe_sum"))

// Chaining with other try functions
df.select(
  expr("try_add(try_multiply(base, rate), fixed_amount)").alias("calculated_value")
)
```

## See Also
- **Add**: Standard addition expression that throws exceptions on errors
- **TryEval**: Generic wrapper for converting exceptions to null returns
- **TrySubtract**, **TryMultiply**, **TryDivide**: Related try-mode arithmetic operations
- **EvalMode**: Enumeration defining evaluation modes (ANSI, TRY, LEGACY)