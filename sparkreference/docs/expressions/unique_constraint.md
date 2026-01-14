# UniqueConstraint

## Overview
UniqueConstraint represents a unique constraint on table columns that ensures no duplicate values exist across the specified column combination. It is a leaf expression that extends TableConstraint and can be converted to Spark's V2 Constraint format with configurable enforcement and reliance characteristics.

## Syntax
```sql
-- Used in CREATE TABLE statements
CREATE TABLE table_name (
    col1 data_type,
    col2 data_type,
    CONSTRAINT constraint_name UNIQUE (col1, col2)
)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| columns | Seq[String] | Sequence of column names that form the unique constraint |
| userProvidedName | String | Optional user-specified name for the constraint (defaults to null) |
| tableName | String | Name of the table this constraint applies to (defaults to null) |
| userProvidedCharacteristic | ConstraintCharacteristic | Constraint properties including enforced/rely flags (defaults to empty) |

## Return Type
UniqueConstraint itself is a constraint definition that returns a Catalyst Expression. When converted via `toV2Constraint`, it returns a `Constraint` object.

## Supported Data Types
UniqueConstraint can be applied to columns of any data type since it operates at the metadata level rather than performing data type-specific operations. The uniqueness check works with any comparable data types.

## Algorithm

- Validates that the constraint is not marked as enforced (throws error if enforced=true)
- Generates automatic constraint names using table name prefix and random suffix if no user name provided
- Converts to V2 Constraint format with FieldReference columns for integration with Spark's constraint system
- Sets validation status to UNVALIDATED by default, requiring explicit validation
- Preserves user-specified rely and enforced flags in the V2 constraint output

## Partitioning Behavior
UniqueConstraint operates at the metadata level and does not directly affect data partitioning:

- Does not preserve or break existing partitioning schemes
- Does not require shuffle operations during constraint definition
- Constraint validation (when performed) may require shuffle to check uniqueness across partitions

## Edge Cases

- Null handling depends on the underlying data source's unique constraint implementation
- Empty column list is allowed but may result in invalid constraints
- Enforced constraints are explicitly rejected with failIfEnforced validation
- Auto-generated names use randomSuffix to avoid naming conflicts
- Missing table names result in constraint names without table prefix

## Code Generation
UniqueConstraint does not support Tungsten code generation as it is a metadata construct rather than a runtime expression. It operates during query planning and catalog operations in interpreted mode.

## Examples
```sql
-- Create table with named unique constraint
CREATE TABLE users (
    id INT,
    email STRING,
    username STRING,
    CONSTRAINT users_email_unique UNIQUE (email)
);

-- Multi-column unique constraint
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    CONSTRAINT orders_customer_date_unique UNIQUE (customer_id, order_date)
);
```

```scala
// Create UniqueConstraint programmatically
val uniqueConstraint = UniqueConstraint(
  columns = Seq("email"),
  userProvidedName = "users_email_unique",
  tableName = "users"
)

// Convert to V2 constraint
val v2Constraint = uniqueConstraint.toV2Constraint

// Chain constraint modifications
val constraintWithCharacteristics = uniqueConstraint
  .withUserProvidedName("custom_unique")
  .withTableName("my_table")
```

## See Also

- PrimaryKeyConstraint - for primary key constraints
- CheckConstraint - for check constraints  
- TableConstraint - parent trait for all table constraints
- ConstraintCharacteristic - for constraint properties configuration