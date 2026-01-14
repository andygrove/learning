# ForeignKeyConstraint

## Overview
`ForeignKeyConstraint` is a Catalyst expression that represents a foreign key constraint definition in Spark SQL. It establishes a referential integrity relationship between child columns in the current table and parent columns in a referenced table, ensuring that values in the child columns must exist in the parent table's referenced columns.

## Syntax
```sql
-- Foreign key constraints are typically defined in table creation or alteration statements
ALTER TABLE child_table ADD CONSTRAINT fk_name 
FOREIGN KEY (child_col1, child_col2) 
REFERENCES parent_table (parent_col1, parent_col2)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| childColumns | Seq[String] | Sequence of column names in the child table that reference the parent table |
| parentTableId | Seq[String] | Identifier sequence representing the parent table (catalog, schema, table) |
| parentColumns | Seq[String] | Sequence of column names in the parent table being referenced |
| userProvidedName | String | Optional user-specified name for the constraint (defaults to null) |
| tableName | String | Name of the table this constraint belongs to (defaults to null) |
| userProvidedCharacteristic | ConstraintCharacteristic | Constraint properties like enforced/rely flags (defaults to empty) |

## Return Type
This expression extends `LeafExpression` and represents a constraint definition rather than returning a computed value. When converted via `toV2Constraint`, it returns a `Constraint` object for the Catalog V2 API.

## Supported Data Types
Foreign key constraints can be applied to columns of any data type, as long as the child and parent column types are compatible for equality comparison. The constraint operates at the metadata level rather than on specific data values.

## Algorithm

- Validates that enforcement is not enabled (calls `failIfEnforced` for foreign key constraints)
- Converts column names to `FieldReference.column` objects for the Catalog V2 API
- Builds a foreign key constraint with the specified rely/enforced characteristics
- Generates automatic constraint names using the pattern `{tableName}_{parentTable}_fk_{randomSuffix}`
- Sets validation status to `UNVALIDATED` by default

## Partitioning Behavior
Foreign key constraints do not directly affect data partitioning behavior since they are metadata-level constructs:

- They do not preserve or break partitioning schemes
- They do not require data shuffling during constraint definition
- Constraint validation (if implemented) may require cross-partition operations

## Edge Cases

- Null handling depends on the constraint characteristics and enforcement policy
- Empty column sequences are allowed but may result in invalid constraint definitions
- Parent table identifiers are converted using `asIdentifier` which handles multi-part names
- Constraint names are auto-generated if not provided by the user
- Enforced foreign key constraints are explicitly rejected via `failIfEnforced`

## Code Generation
As a `LeafExpression` representing metadata, `ForeignKeyConstraint` does not participate in Tungsten code generation. It is used during query planning and constraint management rather than runtime expression evaluation.

## Examples
```sql
-- Create table with foreign key constraint
CREATE TABLE orders (
  order_id INT,
  customer_id INT,
  CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers (id)
);

-- Add foreign key constraint to existing table
ALTER TABLE order_items 
ADD CONSTRAINT fk_order_items_order 
FOREIGN KEY (order_id) REFERENCES orders (order_id);
```

```scala
// Create foreign key constraint programmatically
val foreignKey = ForeignKeyConstraint(
  childColumns = Seq("customer_id"),
  parentTableId = Seq("catalog", "schema", "customers"),
  parentColumns = Seq("id"),
  userProvidedName = "fk_customer",
  userProvidedCharacteristic = ConstraintCharacteristic(rely = Some(true))
)

// Convert to V2 constraint for catalog operations
val v2Constraint = foreignKey.toV2Constraint
```

## See Also
- `PrimaryKeyConstraint` - Primary key constraint definition
- `CheckConstraint` - Check constraint for data validation
- `TableConstraint` - Base trait for table-level constraints
- `ConstraintCharacteristic` - Constraint properties and characteristics