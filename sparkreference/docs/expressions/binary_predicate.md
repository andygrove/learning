# BinaryPredicate

## Overview
BinaryPredicate is a runtime replaceable expression that provides binary predicate operations on binary data types. It serves as a wrapper for string-like operations (startswith, endswith, and other binary predicates) by delegating the actual implementation to ByteArrayMethods at runtime.

## Syntax
```sql
-- Used internally by SQL predicates like:
column1 STARTSWITH column2
column1 ENDSWITH column2
```

```scala
// DataFrame API usage (through higher-level functions)
df.filter(col("column1").startsWith("prefix"))
df.filter(col("column1").endsWith("suffix"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| prettyName | String | The display name of the predicate operation (e.g., "startswith", "endswith") |
| left | Expression | The left operand expression to be evaluated |
| right | Expression | The right operand expression to be evaluated |

## Return Type
BooleanType - Returns true or false based on the predicate evaluation.

## Supported Data Types
BinaryType - Both input expressions must evaluate to binary data types. The expression uses implicit cast input types to convert inputs to binary format when necessary.

## Algorithm

- Maps the prettyName to the actual method name in ByteArrayMethods (e.g., "startswith" → "startsWith")
- Creates a StaticInvoke expression that calls the corresponding method in ByteArrayMethods class
- Evaluates both left and right expressions to binary values
- Delegates the actual predicate logic to the ByteArrayMethods implementation
- Returns the boolean result from the method invocation

## Partitioning Behavior
This expression does not affect partitioning behavior:

- Preserves existing partitioning as it's a row-level predicate operation
- Does not require shuffle operations
- Can be pushed down as a filter predicate in query optimization

## Edge Cases

- Null handling: Follows standard SQL null semantics - any null input results in null output
- Empty binary data: Handled by the underlying ByteArrayMethods implementation
- Case sensitivity: Operates on raw binary data, so no case conversion is applied
- The prettyName mapping ensures backward compatibility with different naming conventions

## Code Generation
This expression supports code generation through the RuntimeReplaceable interface. The replacement StaticInvoke expression generates efficient Java code that directly calls ByteArrayMethods, avoiding interpreted execution overhead.

## Examples
```sql
-- Internal usage in SQL predicates
SELECT * FROM table WHERE binary_col STARTSWITH X'48656C6C6F'
SELECT * FROM table WHERE data_col ENDSWITH X'576F726C64'
```

```scala
// DataFrame API usage (via higher-level string functions)
import org.apache.spark.sql.functions._

df.filter(col("name").startsWith("John"))
df.filter(col("filename").endsWith(".txt"))
```

## See Also

- ByteArrayMethods - The underlying implementation class for binary operations
- RuntimeReplaceable - The interface for expressions that are replaced during query planning
- StaticInvoke - The expression used for invoking static methods with code generation
- ImplicitCastInputTypes - The trait for automatic type casting of inputs