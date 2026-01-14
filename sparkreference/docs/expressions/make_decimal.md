# MakeDecimal

## Overview
MakeDecimal is an internal Spark Catalyst expression that creates a Decimal value from an unscaled Long integer. This expression is generated exclusively by the optimizer during query planning and is not directly accessible to users. It handles the conversion of Long values to Decimal types with specified precision and scale parameters.

## Syntax
This expression is internal only and not directly accessible via SQL or DataFrame API. It is created automatically by the Catalyst optimizer during decimal operations.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression that evaluates to a Long value |
| precision | Int | The total number of digits in the decimal number |
| scale | Int | The number of digits after the decimal point |
| nullOnOverflow | Boolean | Whether to return null on overflow (true) or throw exception (false) |

## Return Type
Returns `DecimalType(precision, scale)` where precision and scale are the specified parameters.

## Supported Data Types
This expression specifically requires:

- Input: Long integers (unscaled decimal values)
- Output: Decimal type with specified precision and scale

## Algorithm
The expression evaluation follows these steps:

- Casts the input value to Long type
- Creates a new Decimal instance
- Uses either `setOrNull` or `set` method based on overflow handling preference
- Returns the constructed Decimal value with the specified precision and scale
- Handles overflow according to the `nullOnOverflow` flag

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require data shuffle as it operates on individual values
- Maintains the same partitioning scheme as the input expression
- Can be evaluated locally on each partition

## Edge Cases

- **Null handling**: Expression is null-intolerant, meaning null inputs produce null outputs
- **Overflow behavior**: Controlled by `nullOnOverflow` parameter - either returns null or throws exception
- **ANSI mode**: When ANSI SQL compliance is enabled, overflow throws exceptions instead of returning null
- **Precision limits**: Subject to Spark's decimal precision and scale constraints
- **Default constructor**: Uses `!SQLConf.get.ansiEnabled` as default for `nullOnOverflow` parameter

## Code Generation
This expression supports Tungsten code generation through the `doGenCode` method. It generates optimized bytecode that:

- Uses `nullSafeCodeGen` for efficient null handling
- Dynamically selects between `setOrNull` and `set` methods
- Includes conditional null checking only when the result is nullable

## Examples
```sql
-- This expression is internal only and not directly accessible in SQL
-- It may be generated during decimal arithmetic operations
SELECT CAST(123 AS DECIMAL(10,2)) + CAST(456 AS DECIMAL(10,2));
```

```scala
// This expression is internal only and not directly accessible in DataFrame API
// It may be generated during decimal operations
import org.apache.spark.sql.functions._
df.select(col("long_column").cast(DecimalType(10, 2)))
```

## See Also

- DecimalType - The target data type for this expression
- Cast expressions - Related type conversion operations
- UnaryExpression - The base class this expression extends