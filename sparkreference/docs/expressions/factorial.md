# Factorial

## Overview
The Factorial expression computes the factorial of a given integer input. It returns the product of all positive integers less than or equal to the input value, with special handling for edge cases and range limitations.

## Syntax
```sql
SELECT factorial(column_name) FROM table_name;
SELECT factorial(5);
```

```scala
import org.apache.spark.sql.functions._
df.select(factorial(col("column_name")))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Integer | The input integer value for which to calculate the factorial |

## Return Type
LongType - Returns a 64-bit long integer containing the factorial result.

## Supported Data Types

- IntegerType (input is implicitly cast to integer if needed)

## Algorithm

- Accepts an integer input and validates it is within the supported range [0, 20]
- Returns null for inputs outside the valid range (< 0 or > 20) to prevent overflow
- Delegates the actual factorial computation to `Factorial.factorial()` helper method
- Uses null-safe evaluation to handle null inputs appropriately
- Supports both interpreted and code-generated execution paths

## Partitioning Behavior
This expression preserves partitioning as it operates on individual rows without requiring data movement:

- Does not require shuffle operations
- Maintains existing data partitioning
- Can be executed independently on each partition

## Edge Cases

- Returns null for negative integers (< 0)
- Returns null for integers greater than 20 to prevent long integer overflow
- Returns null when input is null (null-intolerant behavior)
- Returns 1 for factorial(0) as per mathematical definition
- Expression is marked as nullable due to range validation constraints

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method, which generates optimized Java code for runtime execution rather than falling back to interpreted mode.

## Examples
```sql
-- Basic factorial calculation
SELECT factorial(5);
-- Result: 120

-- Factorial with column reference
SELECT name, factorial(value) as fact_value FROM numbers;

-- Edge cases
SELECT factorial(0);   -- Result: 1
SELECT factorial(-1);  -- Result: null
SELECT factorial(21);  -- Result: null (overflow protection)
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

df.select(factorial(col("number_column")))

// With column alias
df.select(factorial(col("n")).alias("n_factorial"))

// Filtering out null results
df.select(factorial(col("n"))).filter(col("factorial(n)").isNotNull)
```

## See Also

- Mathematical functions: `pow`, `sqrt`, `exp`
- Other integer operations: `abs`, `signum`
- Aggregate functions: `sum`, `product` (if available)