# CheckConstraint

## Overview
CheckConstraint is a Catalyst expression that represents a constraint validation mechanism in Spark SQL. It enforces data quality rules and business logic constraints on table data. This expression is typically used in table definitions to ensure data integrity by validating that rows satisfy specified conditions.

## Syntax
```sql
-- SQL constraint definition
ALTER TABLE table_name ADD CONSTRAINT constraint_name CHECK (condition)

-- In CREATE TABLE statements
CREATE TABLE table_name (
  column1 datatype,
  column2 datatype,
  CONSTRAINT constraint_name CHECK (condition)
)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| name | String | The name identifier for the constraint |
| condition | Expression | The boolean expression that defines the constraint logic |
| enforcementType | EnforcementType | Specifies how the constraint is enforced (e.g., strict, warning) |

## Return Type
Returns Boolean - true if the constraint is satisfied, false if violated.

## Supported Data Types
Supports all Spark SQL data types as input since the constraint condition can operate on:

- Numeric types (IntegerType, LongType, DoubleType, DecimalType, etc.)
- String types (StringType)
- Date and timestamp types (DateType, TimestampType)
- Boolean types (BooleanType)
- Complex types (ArrayType, MapType, StructType)
- Any combination of the above in complex expressions

## Algorithm
The CheckConstraint evaluation follows these steps:

- Parse and compile the constraint condition expression into Catalyst expression tree
- Evaluate the condition expression against input row data
- Return boolean result indicating constraint satisfaction
- Handle null values according to three-valued logic (null conditions typically pass)
- Cache compiled expressions for performance optimization

## Partitioning Behavior
CheckConstraint has the following partitioning characteristics:

- Preserves existing partitioning as it operates row-by-row
- Does not require shuffle operations since validation is local to each row
- Can be applied per-partition independently
- Does not affect partition pruning or partition-wise operations

## Edge Cases

- Null handling: Null constraint conditions are typically treated as satisfied (follows SQL standard)
- Empty input: Returns true for empty datasets (vacuous truth)
- Complex expressions: Supports nested expressions and function calls within constraint conditions
- Runtime failures: Expression evaluation errors may cause constraint violation
- Type coercion: Automatic type casting follows standard Spark SQL coercion rules

## Code Generation
CheckConstraint supports Tungsten code generation for optimal performance. The constraint condition expressions are compiled to Java bytecode when possible, falling back to interpreted mode for complex expressions that cannot be code-generated.

## Examples
```sql
-- Example SQL usage
CREATE TABLE employees (
  id INT,
  age INT,
  salary DECIMAL(10,2),
  CONSTRAINT age_check CHECK (age >= 18 AND age <= 65),
  CONSTRAINT salary_check CHECK (salary > 0)
);

-- Adding constraint to existing table
ALTER TABLE products 
ADD CONSTRAINT price_positive CHECK (price > 0);
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.catalyst.expressions._

val ageConstraint = CheckConstraint(
  name = "age_validation",
  condition = And(
    GreaterThanOrEqual(col("age"), Literal(18)),
    LessThanOrEqual(col("age"), Literal(65))
  ),
  enforcementType = EnforcementType.STRICT
)

// Apply constraint validation in DataFrame operations
df.filter(ageConstraint.condition)
```

## See Also

- ConstraintCharacteristic - Defines constraint metadata and properties
- Expression - Base trait for all Catalyst expressions
- BoundReference - References to bound columns in constraint expressions
- And, Or - Logical expressions commonly used in constraint conditions