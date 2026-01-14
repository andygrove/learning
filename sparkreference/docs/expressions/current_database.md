# CurrentDatabase

## Overview
The `CurrentDatabase` expression returns the name of the current database/schema in the Spark session. This is a leaf expression that produces a string value representing the active database context without requiring any input parameters.

## Syntax
```sql
SELECT current_schema();
-- or
SELECT current_database();
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("current_schema()"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | N/A | This expression takes no arguments |

## Return Type
Returns a `StringType` value representing the current database/schema name.

## Supported Data Types
This expression does not accept input data types as it takes no parameters. It always produces a string output.

## Algorithm

- Retrieves the current database name from the Spark session's catalog context
- Returns the active database/schema identifier as a string literal
- Operates as a constant expression that doesn't depend on row data
- Implements lazy evaluation through the Catalyst expression framework
- Marked as `Unevaluable`, meaning it requires special handling during execution planning

## Partitioning Behavior
This expression has no impact on partitioning behavior:

- Preserves existing partitioning schemes since it's a constant value
- Does not require data shuffle or repartitioning
- Can be computed independently of data distribution

## Edge Cases

- Never returns null values (nullable = false)
- Returns "default" when no specific database is selected
- Behavior is consistent across all executors in distributed execution
- Thread-safe for concurrent access within the same Spark session

## Code Generation
This expression is marked as `Unevaluable`, which means it cannot be directly code-generated using Tungsten. Instead, it requires special handling during query planning where the actual database name is resolved and substituted as a literal value before code generation occurs.

## Examples
```sql
-- Get current database name
SELECT current_schema();
-- Result: default

-- Use in conditional logic
SELECT CASE 
  WHEN current_schema() = 'production' THEN 'prod_mode'
  ELSE 'dev_mode'
END as environment;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Add current database as a column
val df = spark.table("my_table")
  .withColumn("database_name", expr("current_schema()"))

// Filter based on current database
val result = df.filter(expr("current_schema() != 'test_db'"))
```

## See Also

- `current_catalog()` - Returns the current catalog name
- `version()` - Returns Spark version information
- Other misc functions in the `misc_funcs` group