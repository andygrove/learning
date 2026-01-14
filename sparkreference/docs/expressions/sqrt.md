# Sqrt

## Overview
The `Sqrt` expression computes the square root of a numeric value. It wraps the standard `math.sqrt` function to provide square root functionality in Spark SQL expressions.

## Syntax
```sql
SQRT(expr)
```

```scala
sqrt(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric expression to compute the square root of |

## Return Type
Returns `DoubleType` - the square root result as a double-precision floating-point number.

## Supported Data Types
Supports all numeric data types:

- ByteType
- ShortType  
- IntegerType
- LongType
- FloatType
- DoubleType
- DecimalType

## Algorithm
The expression evaluation follows these steps:

- Input value is converted to Double type if necessary
- The standard `math.sqrt` function from Scala/Java Math library is applied
- Result is returned as a Double value
- Inherits null propagation behavior from UnaryMathExpression
- Invalid inputs (negative numbers) return NaN according to IEEE 754 standard

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffle as it operates on individual rows
- Maintains existing partitioning scheme since it's a row-level transformation
- Can be pushed down to individual partitions for parallel execution

## Edge Cases

- **Null handling**: Returns null when input is null (standard null propagation)
- **Negative numbers**: Returns NaN (Not a Number) for negative input values following IEEE 754 specification
- **Zero input**: Returns 0.0 for input value of 0
- **Positive infinity**: Returns positive infinity for positive infinity input
- **NaN input**: Returns NaN when input is already NaN

## Code Generation
This expression supports Tungsten code generation for optimal performance. It extends `UnaryMathExpression` which provides code generation capabilities, avoiding interpreted mode execution in most cases.

## Examples
```sql
-- Basic square root calculation
SELECT SQRT(4);
-- Result: 2.0

-- Square root of column values
SELECT name, SQRT(area) as side_length FROM squares;

-- Handling edge cases
SELECT SQRT(-1);  -- Returns NaN
SELECT SQRT(0);   -- Returns 0.0
SELECT SQRT(NULL); -- Returns NULL
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.sqrt

df.select(sqrt($"number").as("square_root"))

// With column reference
df.withColumn("sqrt_value", sqrt(col("input_column")))
```

## See Also

- `Power` - For computing arbitrary powers including fractional exponents
- `Cbrt` - For computing cube roots specifically  
- Mathematical functions in `org.apache.spark.sql.functions`