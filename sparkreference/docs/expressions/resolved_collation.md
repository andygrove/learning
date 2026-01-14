# ResolvedCollation

## Overview
ResolvedCollation is a leaf expression that represents a resolved collation name in Spark SQL. It encapsulates a collation identifier that has been resolved during the analysis phase and provides a way to reference specific collation rules for string operations.

## Syntax
This expression is primarily used internally during query planning and analysis. It's not directly exposed in SQL syntax but represents resolved collation references.

```sql
-- Collations are typically specified in column definitions or COLLATE clauses
SELECT col1 COLLATE "UTF8_BINARY" FROM table1
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| collationName | String | The name of the resolved collation (e.g., "UTF8_BINARY") |

## Return Type
Returns a StringType with the collation ID corresponding to the resolved collation name. The collation ID is determined by `CollationFactory.collationNameToId(collationName)`.

## Supported Data Types
This expression works with string collation names and produces string types with specific collation metadata.

- Input: String collation name
- Output: StringType with collation metadata

## Algorithm
The expression evaluation follows these steps:

- Stores the resolved collation name as a string parameter
- Maps the collation name to a collation ID using CollationFactory
- Creates a StringType with the resolved collation ID as metadata
- Evaluates to a literal string value containing the collation name
- Delegates actual evaluation to a Literal expression for consistency

## Partitioning Behavior
ResolvedCollation has minimal impact on partitioning behavior:

- Does not affect partitioning schemes as it's a leaf expression
- Does not require shuffle operations
- Preserves existing partitioning since it produces deterministic output

## Edge Cases

- Null handling: The expression is non-nullable (`nullable = false`)
- Invalid collation names: Relies on CollationFactory validation during construction
- Code generation: Uses passthrough delegation to Literal expression for consistency
- Empty collation names: Behavior depends on CollationFactory implementation
- The `doGenCode` method throws an internal error and should never be called directly

## Code Generation
Supports Tungsten code generation through delegation. The expression implements `genCode()` by creating a Literal expression with the collation name and delegating code generation to it. The `doGenCode()` method is intentionally not implemented and throws an internal error if called directly.

## Examples
```sql
-- ResolvedCollation is used internally when collations are specified
CREATE TABLE example (
  id INT,
  name STRING COLLATE 'UTF8_BINARY'
);
```

```scala
// Internal usage during expression resolution
val resolvedCollation = ResolvedCollation("UTF8_BINARY")
val dataType = resolvedCollation.dataType  // StringType with collation ID
val result = resolvedCollation.eval(InternalRow.empty)  // Evaluates to "UTF8_BINARY"
```

## See Also

- CollationFactory - Factory class for collation management
- Literal - Base literal expression used for evaluation delegation  
- StringType - The data type returned by this expression
- LeafExpression - Parent class for expressions with no children