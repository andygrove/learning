# SemiStructuredExtract

## Overview
`SemiStructuredExtract` is a Catalyst expression that represents the extraction of data from fields containing semi-structured data. It serves as an intermediate expression during query analysis that gets resolved into more specific extraction operations for variant data types.

## Syntax
This is an internal Catalyst expression that doesn't have direct SQL syntax. It's created during query analysis and immediately resolved by the `ExtractSemiStructuredFields` rule.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The semi-structured column expression to extract from |
| field | String | The field name to extract from the semi-structured data |

## Return Type
Returns `StringType` as the default data type before resolution. After resolution by `ExtractSemiStructuredFields`, the actual return type depends on the resolved expression (`VariantGet` returns `VariantType`).

## Supported Data Types
- **Input**: Currently only supports `VariantType` columns
- **Output**: `VariantType` (after resolution to `VariantGet`)

## Algorithm
- Expression is created during query parsing/analysis as an intermediate representation
- The `resolved` property is always `false`, indicating it requires further resolution
- `ExtractSemiStructuredFields` rule transforms it into appropriate extraction expressions
- For `VariantType` inputs, resolves to `VariantGet` with `failOnError = true`
- Throws `AnalysisException` for unsupported column types

## Partitioning Behavior
- **Preserves partitioning**: Yes, as this is a column-level transformation
- **Requires shuffle**: No, operates on individual rows independently

## Edge Cases
- **Null handling**: Behavior depends on the resolved expression (`VariantGet`)
- **Unresolved input**: Waits for child expression resolution before applying transformation
- **Unsupported types**: Throws `AnalysisException` with error class "COLUMN_IS_NOT_VARIANT_TYPE"
- **Field extraction failures**: Configured with `failOnError = true`, so will throw exceptions on invalid field access

## Code Generation
This expression is marked as `Unevaluable`, meaning it cannot be directly code-generated or interpreted. It must be resolved to another expression (`VariantGet`) during analysis phase, which then handles code generation.

## Examples
```sql
-- This expression is internal and doesn't have direct SQL syntax
-- It's created during analysis of variant field access operations
```

```scala
// Internal usage during Catalyst analysis
val extract = SemiStructuredExtract(
  child = someVariantColumn, 
  field = "fieldName"
)
// This gets resolved to VariantGet by ExtractSemiStructuredFields rule
```

## See Also
- `VariantGet` - The expression this resolves to for variant types
- `ExtractSemiStructuredFields` - The rule that resolves this expression
- `UnaryExpression` - Parent class providing structure
- `Unevaluable` - Trait indicating this requires resolution before evaluation