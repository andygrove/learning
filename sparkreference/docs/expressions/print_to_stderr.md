# PrintToStderr

## Overview
PrintToStderr is a debugging expression that prints the result of a child expression to stderr and then passes the value through unchanged. It's primarily used for debugging code generation in Spark Catalyst by allowing developers to inspect intermediate values during expression evaluation.

## Syntax
This expression is not directly accessible through SQL syntax. It's an internal debugging utility used within Spark's expression framework.

```scala
// Internal usage in Spark codebase
PrintToStderr(childExpression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The child expression whose result will be printed to stderr and passed through |

## Return Type
Returns the same data type as the child expression (`child.dataType`). This expression acts as a pass-through wrapper.

## Supported Data Types
Supports all data types that the child expression supports, as it simply passes through the child's result after printing it.

## Algorithm

- Evaluates the child expression to get its result value
- Constructs an output message with prefix "Result of {child expression} is " followed by the actual value
- Prints the complete message to System.err
- Returns the original child expression result unchanged
- Maintains null-safety by using the `nullSafeEval` pattern

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not affect data partitioning as it's a pass-through operation
- Does not require shuffle operations
- Maintains the same partitioning scheme as the input data

## Edge Cases

- **Null handling**: Uses null-safe evaluation pattern - if child expression returns null, nothing is printed and null is returned
- **Empty input**: Behavior depends entirely on the child expression's handling of empty input
- **Side effects**: Always produces stderr output as a side effect during evaluation, which may impact performance in production
- **Thread safety**: Uses System.err which is thread-safe for concurrent access

## Code Generation
This expression fully supports Spark's Tungsten code generation:

- Implements `doGenCode` method for optimized code generation
- Uses `nullSafeCodeGen` to generate null-safe evaluation code
- Adds the output prefix as a reference object in the generated code context
- Generated code directly calls `System.err.println` for optimal performance

## Examples
```sql
-- Not directly available in SQL
-- This is an internal debugging expression
```

```scala
// Internal usage example (not public API)
import org.apache.spark.sql.catalyst.expressions._

// Wrap any expression for debugging
val debugExpr = PrintToStderr(Literal(42))
// When evaluated, prints: "Result of 42 is 42" to stderr and returns 42
```

## See Also

- UnaryExpression - Base class for expressions with single child
- Expression.nullSafeEval - Null-safe evaluation pattern
- CodegenContext - Code generation utilities
- Literal - Simple constant expressions that might be wrapped for debugging