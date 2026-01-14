# CurrentCatalog

## Overview
The `CurrentCatalog` expression returns the name of the current catalog in the Spark session. This is a leaf expression that produces a string value representing the active catalog context without requiring any input parameters.

## Syntax
```sql
SELECT current_catalog();
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.select(expr("current_catalog()"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | N/A | This expression takes no arguments |

## Return Type
`StringType` - Returns a non-nullable string representing the current catalog name.

## Supported Data Types
This expression does not accept input data types as it is a parameterless leaf expression that generates its own output.

## Algorithm

- Accesses the current Spark session's catalog context
- Retrieves the active catalog name from the session state
- Returns the catalog name as a string value
- Operates as a constant expression during query execution
- Does not perform any computation on input data

## Partitioning Behavior
This expression has neutral partitioning behavior:

- Preserves existing partitioning schemes as it doesn't affect data distribution
- Does not require shuffle operations since it produces the same constant value across all partitions
- Can be computed independently on each partition without coordination

## Edge Cases

- Never returns null values (nullable = false)
- Always returns a valid catalog name string
- Behavior is consistent across all nodes in a distributed environment
- Result remains constant throughout the execution of a single query
- No special handling required for empty datasets

## Code Generation
This expression is marked as `Unevaluable`, meaning it does not support Tungsten code generation and cannot be directly evaluated. The actual catalog name resolution is handled during query planning and analysis phases, with the result being substituted as a literal value in the optimized plan.

## Examples
```sql
-- Get the current catalog name
SELECT current_catalog();
-- Output: spark_catalog

-- Use in a WHERE clause
SELECT table_name FROM information_schema.tables 
WHERE table_catalog = current_catalog();

-- Use in a complex query
SELECT current_catalog() as catalog_name, count(*) as table_count
FROM information_schema.tables
GROUP BY current_catalog();
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Select current catalog
val catalogDF = spark.sql("SELECT current_catalog()")
catalogDF.show()

// Use with other expressions
val df = spark.range(1)
val result = df.select(expr("current_catalog()").alias("catalog"))
result.show()

// Combine with metadata queries
val tablesDF = spark.sql("""
  SELECT current_catalog() as catalog, 
         count(*) as table_count
  FROM information_schema.tables
""")
```

## See Also

- `current_database()` - Returns the current database name
- `current_schema()` - Returns the current schema name  
- `version()` - Returns Spark version information
- Catalog management functions in Spark SQL