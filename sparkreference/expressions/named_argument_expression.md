# NamedArgumentExpression

## Overview

`NamedArgumentExpression` represents an argument expression to a routine call accompanied with an explicit reference to the corresponding argument name. This allows function arguments to be specified by name rather than position, enabling flexible argument ordering and improved readability. This expression is unevaluable and is replaced with its value during query analysis after argument list rearrangement.

## Syntax

```sql
key => value
```

Where:
- `key` is an identifier representing the argument name
- `=>` is the fat arrow operator
- `value` is any valid expression

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| key | String | The name of the routine argument parameter |
| value | Expression | The expression providing the value for the named argument |

## Return Type

The return type matches the data type of the `value` expression, as determined by `value.dataType`. The `NamedArgumentExpression` itself acts as a transparent wrapper around the value expression's type.

## Supported Data Types

Supports all data types since it accepts any `Expression` as its value. The supported data types are determined by the underlying value expression and the requirements of the target function that will receive the named argument.

## Algorithm

- Acts as a wrapper around a value expression with an associated parameter name
- Extends `UnaryExpression` with the value expression as its single child
- Marked as `Unevaluable` - cannot be directly evaluated in the execution engine
- During analysis phase, the analyzer matches the key name to function parameter names
- The expression is replaced with its value expression after argument reordering
- Child expression resolution occurs recursively through normal analyzer rules

## Partitioning Behavior

- **Preserves partitioning**: Yes, as it's a transparent wrapper that gets replaced during analysis
- **Requires shuffle**: No, the expression itself doesn't affect data distribution
- The actual partitioning behavior depends on the target function that receives the resolved argument

## Edge Cases

- **Null handling**: Inherits null handling behavior from the wrapped value expression
- **Empty input**: No special handling - delegates to the value expression
- **Analysis phase**: Must be completely resolved and replaced before code generation
- **Duplicate names**: Analyzer handles validation of duplicate argument names in function calls
- **Unmatched names**: Analyzer validates that named arguments match expected function parameters

## Code Generation

This expression does **not** support code generation (Tungsten). It is marked as `Unevaluable` and must be completely resolved and replaced with its value expression during the analysis phase before reaching code generation. Any attempt to evaluate this expression directly will result in an error.

## Examples

```sql
-- Using named arguments with encode function
SELECT encode("abc", charset => "utf-8");

-- Arguments can appear in any order
SELECT encode(charset => "utf-8", value => "abc");

-- Named arguments with complex expressions
SELECT my_function(
  param1 => col1 + col2,
  param2 => CASE WHEN col3 > 0 THEN "positive" ELSE "negative" END
);
```

```scala
// DataFrame API usage (conceptual - actual API may vary)
import org.apache.spark.sql.catalyst.expressions._

// Creating a NamedArgumentExpression programmatically
val namedArg = NamedArgumentExpression("charset", Literal("utf-8"))

// The expression shows its structure
namedArg.toString // Returns: "charset => utf-8"
namedArg.dataType // Returns: StringType (from the Literal)
```

## See Also

- `UnaryExpression` - Base class for expressions with a single child
- `Unevaluable` - Trait for expressions that cannot be directly evaluated
- `ResolveFunctions` - Analyzer rule that resolves function calls and handles named arguments
- Function call expressions that accept named arguments