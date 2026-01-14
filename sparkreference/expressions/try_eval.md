# TryEval

## Overview
`TryEval` is a Spark Catalyst unary expression that wraps another expression and catches any exceptions during evaluation, returning `null` instead of propagating the exception. It provides a safe evaluation mechanism for expressions that might throw runtime exceptions, making them null-tolerant.

## Syntax
This is an internal Catalyst expression not directly exposed in SQL. It's used internally by other "try_" functions like `try_add`, `try_divide`, etc.

```scala
TryEval(child: Expression)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The expression to evaluate safely, catching any exceptions |

## Return Type
Returns the same data type as the child expression, but the result is always nullable.

## Supported Data Types
Supports any data type that the child expression supports, as it acts as a transparent wrapper around the child expression.

## Algorithm
- Attempts to evaluate the child expression normally
- If evaluation succeeds, returns the child's result (including null values)
- If any exception is thrown during evaluation, catches it and returns null
- Forces the result to be nullable regardless of the child expression's nullability
- In code generation, wraps the child's generated code in a try-catch block

## Partitioning Behavior
- Preserves partitioning as it doesn't change the logical evaluation of data distribution
- Does not require shuffle operations
- Acts as a pass-through wrapper that doesn't affect data locality

## Edge Cases
- **Null handling**: If child expression returns null normally, passes through the null value
- **Exception handling**: Any exception (runtime exceptions, arithmetic errors, etc.) results in null
- **Nullability**: Always returns nullable results, even if child expression is non-nullable
- **Null intolerant**: Marked as `nullIntolerant = true`, meaning it doesn't produce null for null inputs in the traditional sense

## Code Generation
Supports full code generation (Tungsten). Generates Java code that wraps the child expression's generated code in a try-catch block, with proper initialization of result variables to default values before attempting evaluation.

## Examples
```scala
// Internal usage - not directly callable in SQL
// Used by try_add internally:
val safeAdd = TryEval(Add(col1, col2, EvalMode.ANSI))
```

```sql
-- TryEval is used internally by functions like:
SELECT try_add(2147483647, 1);  -- Returns NULL instead of overflow error
SELECT try_divide(10, 0);       -- Returns NULL instead of division by zero error
```

## See Also
- `try_add` - Safe addition using TryEval internally
- `try_divide` - Safe division using TryEval internally  
- `try_subtract` - Safe subtraction using TryEval internally
- `try_multiply` - Safe multiplication using TryEval internally
- `try_to_binary` - Safe binary conversion using TryEval internally
- `RuntimeReplaceable` - Pattern used by the try_* functions that utilize TryEval