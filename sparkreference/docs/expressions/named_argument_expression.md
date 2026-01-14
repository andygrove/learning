# NamedArgumentExpression

## Overview
`NamedArgumentExpression` is a Catalyst expression that represents a named argument in routine calls, allowing arguments to be passed by name rather than position. This expression is used internally to support named parameter syntax in SQL functions, where arguments can be specified with explicit parameter names for better readability and flexibility.

## Syntax
```sql
function_name(parameter_name => value, ...)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| key | String | The name of the routine argument/parameter |
| value | Expression | The value expression for the routine argument |

## Return Type
The return type matches the data type of the `value` expression. Since this is a wrapper expression, it inherits the data type from its child value expression.

## Supported Data Types
All data types are supported since `NamedArgumentExpression` acts as a wrapper around any underlying expression. The supported data types depend entirely on the wrapped `value` expression.

## Algorithm
- Acts as a unary expression wrapper around the value expression
- Preserves the data type of the underlying value expression
- Provides named parameter semantics for routine calls
- Delegates all evaluation logic to the child value expression
- Maintains the parameter name for proper argument binding during function resolution

## Partitioning Behavior
- **Preserves partitioning**: Yes, since it's a wrapper expression that doesn't modify data distribution
- **Requires shuffle**: No, this expression doesn't trigger data shuffling as it only provides naming semantics

## Edge Cases
- **Null handling**: Inherits null handling behavior from the wrapped value expression
- **Empty input**: Behavior depends on the underlying value expression
- **Unevaluable**: This expression extends `Unevaluable`, meaning it cannot be directly evaluated and must be processed/transformed during analysis phase
- **Resolution dependency**: The value expression is resolved recursively by Analyzer rules (e.g., `ResolveFunctions` for built-in functions)

## Code Generation
This expression does not support code generation as it extends `Unevaluable`. It serves as an intermediate representation during query analysis and is typically transformed or resolved before the code generation phase.

## Examples
```sql
-- Named arguments in encode function
SELECT encode(charset => "utf-8", value => "abc");

-- Named arguments with mixed positional and named parameters
SELECT some_function(arg1 => 'value1', arg2 => 42);
```

```scala
// This expression is primarily used internally during SQL parsing
// and is not typically created directly in DataFrame API
val namedArg = NamedArgumentExpression("charset", Literal("utf-8"))
```

## See Also
- `UnaryExpression` - Base class for expressions with single child
- `Unevaluable` - Trait for expressions that cannot be directly evaluated
- `ResolveFunctions` - Analyzer rule that resolves function expressions
- Expression resolution and analysis phases in Catalyst optimizer