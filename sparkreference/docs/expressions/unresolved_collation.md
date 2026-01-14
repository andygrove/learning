# UnresolvedCollation

## Overview

UnresolvedCollation is a temporary leaf expression used during Spark SQL's analysis phase to represent a collation name that has not yet been resolved from a fully qualified collation name. This expression serves as a placeholder until the collation specification can be validated and resolved into a concrete collation implementation.

## Syntax

```sql
-- Used internally during SQL parsing, not directly invokable by users
COLLATE collation_name
```

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| collationName | Seq[String] | A sequence of strings representing the hierarchical collation name parts (e.g., database, schema, collation) |

## Return Type

This expression throws an `UnresolvedException` when `dataType` is accessed, as it is not meant to be evaluated directly. The return type is determined after resolution.

## Supported Data Types

This expression does not directly support data types as it is an intermediate representation. After resolution, collations typically apply to string-based data types.

## Algorithm

- Stores the unresolved collation name as a sequence of string identifiers

- Implements the `Unevaluable` trait, preventing direct evaluation

- Maintains `resolved = false` to indicate it requires further analysis

- Throws `UnresolvedException` when data type information is requested

- Uses the `UNRESOLVED_COLLATION` tree pattern for identification during analysis

## Partitioning Behavior

This expression does not affect partitioning behavior as it is resolved away during the analysis phase before physical planning:

- Does not preserve or affect partitioning (resolved before physical planning)

- No shuffle requirements (not present during execution)

## Edge Cases

- Throws `UnresolvedException` when `dataType` is accessed before resolution

- Returns `false` for `nullable` property by default

- Cannot be evaluated directly due to `Unevaluable` trait implementation

- Must be resolved during analysis phase or query compilation will fail

## Code Generation

This expression does not support code generation as it implements the `Unevaluable` trait and is designed to be resolved away during the analysis phase before code generation occurs.

## Examples

```sql
-- Internal representation during parsing of:
SELECT col COLLATE utf8_general_ci FROM table
-- Creates UnresolvedCollation(Seq("utf8_general_ci"))
```

```scala
// This is an internal expression, not directly created in DataFrame API
// It would be created during SQL parsing of collation specifications
val unresolvedCollation = UnresolvedCollation(Seq("utf8", "general", "ci"))
```

## See Also

- ResolvedCollation expressions (after analysis phase)
- Collation-related catalog functions
- String expressions that support collation