# PrimaryKeyConstraint

## Overview
`PrimaryKeyConstraint` is a Catalyst expression that represents a primary key constraint on one or more columns in a table. It extends `LeafExpression` and `TableConstraint` to define uniqueness and non-null requirements for specified columns, and can be converted to Spark's V2 constraint representation.

## Syntax
```sql
-- In CREATE TABLE or ALTER TABLE statements
CONSTRAINT constraint_name PRIMARY KEY (column1, column2, ...)
```

```scala
// Programmatic creation
PrimaryKeyConstraint(
  columns = Seq("col1", "col2"),
  userProvidedName = "pk_name",
  tableName = "table_name",
  userProvidedCharacteristic = ConstraintCharacteristic(...)
)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| columns | Seq[String] | Sequence of column names that form the primary key |
| userProvidedName | String | Optional user-provided name for the constraint (default: null) |
| tableName | String | Name of the table this constraint belongs to (default: null) |
| userProvidedCharacteristic | ConstraintCharacteristic | Constraint characteristics like enforced/rely flags (default: empty) |

## Return Type
This is a constraint expression that doesn't return data values. When converted via `toV2Constraint`, it returns a Spark V2 `Constraint` object.

## Supported Data Types
Primary key constraints can be applied to columns of any data type that supports equality comparison and hashing for uniqueness checks.

## Algorithm

- Validates that the constraint characteristic is not enforced (throws error if enforced is true)
- Generates a default constraint name using pattern `${tableName}_pk` if no user name provided
- Converts column names to `FieldReference.column` objects for V2 constraint creation
- Creates a V2 primary key constraint with rely/enforced flags and UNVALIDATED status
- Supports copying with modified names, table names, or characteristics

## Partitioning Behavior
Primary key constraints are metadata-only and do not directly affect data partitioning:

- Does not preserve or alter existing partitioning schemes
- Does not require shuffle operations
- Constraint validation may impact query planning and optimization

## Edge Cases

- Null handling: Primary key columns implicitly require non-null values
- Empty columns list: May be allowed but would create an invalid constraint
- Enforced characteristic: Explicitly fails if user tries to set enforced=true for PRIMARY KEY
- Missing table name: Generates constraint name as "null_pk" if tableName is null
- Duplicate constraint names: No validation performed at expression level

## Code Generation
This expression is a constraint definition that participates in Catalyst's rule-based optimization but does not generate runtime code for data processing. It operates at the metadata/schema level.

## Examples
```sql
-- Create table with named primary key constraint
CREATE TABLE users (
  id INT,
  email STRING,
  CONSTRAINT users_pk PRIMARY KEY (id)
);

-- Create table with composite primary key
CREATE TABLE order_items (
  order_id INT,
  item_id INT,
  quantity INT,
  PRIMARY KEY (order_id, item_id)
);
```

```scala
// Create primary key constraint programmatically
val pkConstraint = PrimaryKeyConstraint(
  columns = Seq("user_id", "account_id"),
  userProvidedName = "user_account_pk",
  tableName = "user_accounts"
)

// Convert to V2 constraint
val v2Constraint = pkConstraint.toV2Constraint

// Create with custom characteristics
val characteristic = ConstraintCharacteristic(rely = Some(true), enforced = Some(false))
val pkWithChar = pkConstraint.withUserProvidedCharacteristic(characteristic)
```

## See Also

- `TableConstraint` - Base trait for table-level constraints
- `ConstraintCharacteristic` - Configuration for constraint behavior
- `LeafExpression` - Base class for expressions with no child expressions
- Foreign key constraints and check constraints in the same constraint system