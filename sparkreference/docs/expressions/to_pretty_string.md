# ToPrettyString

## Overview
ToPrettyString is an internal Spark Catalyst expression that generates human-readable string representations of values across all data types. It differs from standard string casting by printing null values as "NULL" and formatting binary data in hexadecimal format.

## Syntax
This is an internal expression not directly accessible through SQL syntax. It's used internally by Spark for pretty-printing values.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The input expression whose value will be converted to a pretty string |
| timeZoneId | Option[String] | Optional timezone identifier for timestamp formatting (defaults to None) |

## Return Type
UTF8String - Always returns a non-null UTF8String representation of the input value.

## Supported Data Types
All Spark SQL data types are supported, including:

- Numeric types (integers, decimals, floating-point)
- String types
- Binary types (formatted as hex)
- Timestamp and date types (timezone-aware)
- Complex types (arrays, structs, maps)
- Boolean types
- Null values

## Algorithm
The expression evaluation follows these steps:

- Evaluates the child expression to get the input value
- If the input value is null, returns the string "NULL"
- Otherwise, applies a data type-specific casting function to convert the value to UTF8String
- For decimal types, uses plain string representation without scientific notation
- For binary data, applies hexadecimal formatting
- For complex types, uses curly braces "{}" as delimiters instead of square brackets

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Does not require shuffle operations
- Maintains the same partitioning as the input data
- Can be evaluated independently on each partition

## Edge Cases

- Null input values are converted to the literal string "NULL" instead of remaining null
- Binary values are formatted using hexadecimal representation via the configured BinaryFormatter
- Decimal values use plain string format rather than scientific notation
- Complex types (structs, arrays, maps) use curly braces "{}" as delimiters
- The expression itself is never nullable (always returns a string, even for null inputs)

## Code Generation
This expression supports Tungsten code generation for optimal performance. The generated code includes:

- Inline null checking with direct string literal assignment
- Data type-specific casting code generation via `castToStringCode`
- Compile-time constant folding for the null string value

## Examples
```sql
-- This is an internal expression, not directly accessible via SQL
-- Used internally by Spark for SHOW commands and debugging output
```

```scala
// Internal usage example (not for end-user code)
import org.apache.spark.sql.catalyst.expressions.ToPrettyString
import org.apache.spark.sql.catalyst.expressions.Literal

val expr = ToPrettyString(Literal(42))
val prettyExpr = ToPrettyString(Literal(null), Some("UTC"))
```

## See Also

- Cast - Standard type casting expression
- ToString - Basic string conversion expression  
- ToStringBase - Base trait for string conversion expressions
- UnaryExpression - Base class for single-argument expressions