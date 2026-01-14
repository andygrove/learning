# NullIfZero

## Overview
NullIfZero is a conditional expression that returns null when the input value equals zero, otherwise returns the original input value unchanged. This expression is implemented as a RuntimeReplaceable that transforms into an If-EqualTo conditional expression during analysis.

## Syntax
```sql
nullifzero(input)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| input | Expression | The input expression to evaluate against zero |

## Return Type
Returns the same data type as the input expression, or null if the input equals zero.

## Supported Data Types
Supports numeric data types that can be compared to zero:

- Byte
- Short  
- Integer
- Long
- Float
- Double
- Decimal

## Algorithm
The expression is evaluated using the following logic:

- Compare the input value to the literal value 0 using EqualTo comparison
- If the comparison returns true (input equals zero), return null
- If the comparison returns false (input does not equal zero), return the original input value
- The transformation occurs at analysis time, replacing NullIfZero with If(EqualTo(input, Literal(0)), Literal(null), input)
- Runtime evaluation follows standard If-Then-Else conditional logic

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations
- Maintains existing data partitioning scheme
- Can be safely pushed down to individual partitions for parallel execution

## Edge Cases

- **Null input**: If input is null, the EqualTo comparison with 0 returns null, causing the If expression to return the original null input
- **Zero input**: Any numeric zero value (0, 0.0, 0.00, etc.) will be converted to null
- **Type coercion**: Input values must be comparable to integer literal 0, following Spark's type coercion rules
- **Floating point precision**: Exact equality comparison is used, so values very close to zero but not exactly zero will not be converted to null

## Code Generation
This expression supports Tungsten code generation since it transforms into standard If/EqualTo expressions that have full codegen support. No fallback to interpreted mode is required for supported data types.

## Examples
```sql
-- Basic usage with integer
SELECT nullifzero(0);  -- Returns NULL
SELECT nullifzero(5);  -- Returns 5

-- Usage with decimal values  
SELECT nullifzero(0.0);  -- Returns NULL
SELECT nullifzero(3.14); -- Returns 3.14

-- Usage in table queries
SELECT customer_id, nullifzero(discount_amount) as discount 
FROM orders;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(col("value"), expr("nullifzero(value)").as("result"))

// Direct expression usage
val nullIfZeroExpr = NullIfZero(col("amount").expr)
df.select(Column(nullIfZeroExpr).as("processed_amount"))
```

## See Also

- If - Conditional if-then-else expression
- IsNull - Check for null values
- Coalesce - Handle null value replacement
- NullIf - General null-if conditional (opposite behavior)