# AssertTrue

## Overview
The `AssertTrue` expression validates that a boolean condition is true and throws an error with a custom message if it is false. This is a runtime-replaceable expression that internally uses an `If` statement combined with `RaiseError` to perform the validation. It returns `NULL` when the assertion passes and raises an error when it fails.

## Syntax
```sql
assert_true(condition)
assert_true(condition, error_message)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("assert_true(column > 0)"))
df.select(expr("assert_true(column > 0, 'Column must be positive')"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| condition | Boolean | The boolean expression to evaluate and assert as true |
| error_message | String (optional) | Custom error message to display when assertion fails. Defaults to "'<condition>' is not true!" |

## Return Type
Always returns `NULL` when the assertion passes. Throws a runtime error when the assertion fails.

## Supported Data Types

- **condition**: Boolean expressions or any expression that can be evaluated to boolean
- **error_message**: String literals or string expressions

## Algorithm

- Evaluates the boolean condition expression
- If condition is `true`, returns `NULL`
- If condition is `false` or `NULL`, raises an error with the specified message
- Uses internal `If(condition, Literal(null), RaiseError(message))` structure
- Default error message format: `"'<pretty_sql_of_condition>' is not true!"`

## Partitioning Behavior
This expression preserves partitioning behavior:

- Does not require shuffle operations
- Preserves existing data partitioning
- Evaluation occurs within each partition independently

## Edge Cases

- **Null condition**: Treats `NULL` condition as false and raises an error
- **Empty error message**: Accepts empty strings as valid error messages
- **Complex conditions**: Pretty-prints the SQL representation of complex conditions in default error messages
- **Runtime evaluation**: Errors are thrown at runtime during query execution, not at planning time

## Code Generation
This expression supports Tungsten code generation as it is implemented as a `RuntimeReplaceable` expression that gets replaced with optimized `If` and `RaiseError` expressions during catalyst optimization.

## Examples
```sql
-- Basic assertion
SELECT assert_true(1 > 0);
-- Returns: NULL

-- Assertion with custom message  
SELECT assert_true(1 < 0, 'Number must be positive');
-- Throws: java.lang.RuntimeException: Number must be positive

-- Assertion in WHERE clause
SELECT * FROM table WHERE assert_true(column IS NOT NULL, 'Column cannot be null') IS NULL;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic assertion
df.select(expr("assert_true(age >= 0)"))

// With custom error message
df.select(expr("assert_true(salary > 0, 'Salary must be positive')"))

// In filter operations
df.filter(expr("assert_true(status = 'ACTIVE') IS NULL"))
```

## See Also

- `If` - Conditional expression used internally
- `RaiseError` - Error throwing expression used internally  
- `when().otherwise()` - Alternative conditional logic
- Data validation functions like `isnotnull()`, `isnull()`