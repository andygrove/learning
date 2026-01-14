# Coalesce

## Overview
The Coalesce expression returns the first non-null value from a sequence of expressions, evaluating arguments from left to right. It implements short-circuit evaluation, stopping as soon as a non-null value is found. If all expressions evaluate to null, the result is null.

## Syntax
```sql
COALESCE(expr1, expr2, ..., exprN)
```

```scala
// DataFrame API
coalesce(col("expr1"), col("expr2"), ..., col("exprN"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| children | Seq[Expression] | A sequence of expressions to evaluate, requires at least one expression |

## Return Type
Returns the same data type as the input expressions. All input expressions must have the same data type.

## Supported Data Types
All Spark SQL data types are supported, including:

- Numeric types (IntegerType, LongType, DoubleType, DecimalType, etc.)
- String types (StringType)
- Date and timestamp types (DateType, TimestampType)
- Complex types (ArrayType, MapType, StructType)
- Binary types (BinaryType)

All input expressions must be of the same type.

## Algorithm

- Expressions are evaluated sequentially from left to right
- Evaluation stops immediately when the first non-null value is encountered (short-circuit evaluation)
- Only the first expression is always evaluated; subsequent expressions are conditionally evaluated
- Returns the first non-null value found, or null if all expressions are null
- Uses ComplexTypeMergingExpression to handle type resolution across all children

## Partitioning Behavior
Coalesce does not affect data partitioning:

- Preserves existing partitioning scheme
- Does not require data shuffle
- Operates as a row-level transformation within each partition

## Edge Cases

- **Null handling**: Returns null only if all input expressions evaluate to null
- **Single argument**: If only one expression is provided, returns that expression's value
- **Empty input**: Throws QueryCompilationErrors.wrongNumArgsError if no arguments provided
- **Type mismatch**: Throws type check error if input expressions have different data types
- **Nullable result**: Result is nullable only if all input expressions are nullable

## Code Generation
This expression supports Tungsten code generation with optimized implementations:

- Generates efficient Java code using do-while loops with continue statements
- Implements short-circuit evaluation in generated code
- Uses splitExpressionsWithCurrentInputs for handling large numbers of expressions
- Falls back to interpreted eval() method when code generation is not available

## Examples
```sql
-- Basic usage
SELECT COALESCE(null, 'hello', 'world') AS result;
-- Returns: 'hello'

-- With column references
SELECT COALESCE(col1, col2, 'default') FROM table;

-- Numeric example
SELECT COALESCE(null, null, 42, 100) AS result;
-- Returns: 42
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions.coalesce

df.select(coalesce($"col1", $"col2", lit("default")))

// Multiple columns with fallback
df.withColumn("result", coalesce($"primary", $"secondary", lit(0)))
```

## See Also

- **IsNull / IsNotNull**: For null checking expressions
- **If / When**: For conditional expressions with more complex logic
- **NullIf**: For converting specific values to null
- **Nvl / Nvl2**: Alternative null handling functions