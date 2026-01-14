# UnresolvedNamedLambdaVariable

## Overview
`UnresolvedNamedLambdaVariable` is a placeholder expression used during the analysis phase to represent lambda variables in higher-order functions before they are resolved. It prevents unexpected resolution of lambda functions during the initial parsing and analysis stages of query planning.

## Syntax
This is an internal Catalyst expression that is not directly accessible through SQL or DataFrame API. It is created automatically during the parsing of lambda expressions in higher-order functions like `transform`, `filter`, `exists`, etc.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| nameParts | Seq[String] | Sequence of string parts that make up the lambda variable name |

## Return Type
This expression is `Unevaluable` and throws `UnresolvedException` for all type-related methods. It does not have a concrete return type as it must be resolved before evaluation.

## Supported Data Types
Not applicable - this expression is a placeholder that must be resolved before type checking occurs.

## Algorithm

- Stores the lambda variable name as a sequence of string parts
- Marks itself as unresolved (`resolved = false`)
- Throws `UnresolvedException` for any attempt to access type information or evaluation methods
- Provides string representation for debugging and SQL generation
- Uses `LAMBDA_VARIABLE` tree pattern for pattern matching during analysis

## Partitioning Behavior
Not applicable - this expression is resolved before physical planning and does not affect partitioning behavior.

## Edge Cases

- All type-related methods (`dataType`, `nullable`, `qualifier`) throw `UnresolvedException`
- All evaluation-related methods throw `UnresolvedException` since it extends `Unevaluable`
- Expression ID and attribute conversion methods throw `UnresolvedException`
- Name parts containing dots are wrapped in backticks for proper SQL representation

## Code Generation
This expression does not support code generation as it is `Unevaluable` and must be resolved to concrete expressions before the code generation phase.

## Examples
```sql
-- Lambda variables are created implicitly in higher-order functions
-- The 'x' below would initially be represented as UnresolvedNamedLambdaVariable
SELECT transform(array(1, 2, 3), x -> x * 2);
```

```scala
// DataFrame API usage where lambda variables are created
// The lambda parameter would be UnresolvedNamedLambdaVariable initially
import org.apache.spark.sql.functions._
df.select(transform(col("numbers"), x => x * 2))
```

## See Also

- `LambdaFunction` - The resolved form of lambda expressions
- `NamedLambdaVariable` - The resolved form of lambda variables
- Higher-order functions like `ArrayTransform`, `ArrayFilter`, `ArrayExists`