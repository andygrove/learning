# PrettyPythonUDF

## Overview
`PrettyPythonUDF` is a placeholder expression used for displaying Python UDF expressions in a human-readable format without debugging information such as result IDs. It serves as a presentation layer for Python aggregate functions during query plan visualization and logging, extending `UnevaluableAggregateFunc` to indicate it cannot be directly evaluated.

## Syntax
This expression is not directly invokable by users but represents Python UDFs in query plans:
```sql
-- Represents Python aggregate UDFs in plan output
python_udf_name([DISTINCT] arg1, arg2, ...)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| `name` | `String` | The name of the Python UDF function |
| `dataType` | `DataType` | The return data type of the Python UDF |
| `children` | `Seq[Expression]` | The input expressions/arguments to the Python UDF |

## Return Type
The return type is determined by the `dataType` parameter, which can be any Spark SQL data type that the underlying Python UDF is configured to return.

## Supported Data Types
As a placeholder expression, it supports all data types that Python UDFs can return:
- Primitive types (IntegerType, StringType, DoubleType, etc.)
- Complex types (ArrayType, MapType, StructType)
- The actual type validation occurs in the underlying Python UDF implementation

## Algorithm
- Acts as a non-executable placeholder for display purposes only
- Formats the UDF name and arguments for string representation
- Delegates actual evaluation to the underlying Python UDF implementation
- Cannot be directly evaluated (throws exception if evaluation is attempted)
- Provides specialized formatting for SQL output and aggregate string representations

## Partitioning Behavior
Since this is a placeholder expression:
- Does not directly affect partitioning (inherits from underlying UDF)
- Does not require shuffle by itself
- Partitioning behavior depends on the actual Python UDF implementation it represents

## Edge Cases
- **Null handling**: Always returns `nullable = true`, indicating the expression can produce null values
- **Evaluation attempts**: Throws `UnsupportedOperationException` if direct evaluation is attempted since it extends `UnevaluableAggregateFunc`
- **Empty children**: Handles empty argument lists gracefully in string formatting
- **Display formatting**: Provides consistent formatting across different string representation methods

## Code Generation
This expression does not support code generation:
- Extends `UnevaluableAggregateFunc`, making it non-evaluable
- Falls back to the underlying Python UDF's execution model
- Code generation is handled by the actual Python UDF implementation, not this placeholder

## Examples
```sql
-- This expression appears in query plans when using Python UDFs:
-- EXPLAIN output might show:
python_sum(col1, col2)
python_avg(DISTINCT col3)
```

```scala
// Internal usage in Catalyst (not user-facing):
val prettyUDF = PrettyPythonUDF(
  name = "my_python_agg",
  dataType = DoubleType,
  children = Seq(col("value").expr)
)

// String representation:
prettyUDF.toString  // "my_python_agg(value)"
prettyUDF.sql(true) // "my_python_agg(DISTINCT value)"
```

## See Also
- `UnevaluableAggregateFunc` - Parent class for non-evaluable aggregate expressions
- `NonSQLExpression` - Trait for expressions not directly expressible in SQL
- `PythonUDF` - Actual executable Python UDF expression
- `UserDefinedAggregateFunction` - Interface for user-defined aggregate functions