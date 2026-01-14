# With

## Overview

The `With` expression is an expression-level common table expression (CTE) that holds a list of common sub-expressions and allows the main expression to reference them. It guarantees that common expressions are evaluated only once even if referenced multiple times, providing optimization for complex expressions with repeated computations.

## Syntax

```scala
With(child: Expression, defs: Seq[CommonExpressionDef])
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The main expression that may contain references to common expressions |
| defs | Seq[CommonExpressionDef] | List of common expression definitions that can be referenced by the child |

## Return Type

The `With` expression returns the same data type as its child expression. The data type is dynamically determined by the `child.dataType` property.

## Supported Data Types

The `With` expression supports all data types since it acts as a container and defers to its child expression for type determination. There are no restrictions on input data types at the `With` expression level.

## Algorithm

- Validates that no aggregate expressions contain unsupported common expression references in the same scope

- Maintains a list of common expression definitions (`defs`) that can be referenced by the child expression

- During canonicalization, reassigns all CommonExpressionRef and CommonExpressionDef IDs starting from 0 to ensure consistent comparison

- Updates CommonExpressionRef instances when their corresponding CommonExpressionDef data types or nullability change

- Preserves evaluation semantics by ensuring common expressions are computed once and reused

## Partitioning Behavior

The `With` expression preserves partitioning behavior since it acts as a container:

- Does not affect partitioning directly as it defers to its child expression

- No shuffle operations are introduced by the `With` expression itself

## Edge Cases

- Null handling behavior is inherited from the child expression

- The expression validates against creating dangling CommonExpressionRef after rewriting aggregate expressions

- Nested `With` expressions are supported with proper ID scoping to avoid conflicts

- Empty `defs` list is allowed, though the expression provides no optimization benefit in that case

## Code Generation

The `With` expression extends `Unevaluable`, meaning it cannot be directly evaluated and does not support code generation. It must be rewritten by the `RewriteWithExpression` rule before code generation, which replaces common expression references with their actual definitions while ensuring single evaluation.

## Examples

```scala
// Example: Creating a With expression programmatically
val commonDef = CommonExpressionDef(
  Add(col("a"), col("b")), 
  CommonExpressionId(1)
)
val withExpr = With(
  child = Multiply(
    CommonExpressionRef(commonDef), 
    CommonExpressionRef(commonDef)
  ),
  defs = Seq(commonDef)
)
```

```scala
// Example: Nested With expressions
val innerWith = With(child = col("x"), defs = Seq(innerDef))
val outerWith = With(child = innerWith, defs = Seq(outerDef))
```

## See Also

- `CommonExpressionDef` - Defines a common expression with an ID
- `CommonExpressionRef` - References a common expression by ID  
- `RewriteWithExpression` - Rule that rewrites With expressions for execution
- `Unevaluable` - Base trait for expressions that require rewriting before evaluation