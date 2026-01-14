# SQLKeywords

## Overview
The SQLKeywords expression is a generator function that produces a table of SQL keywords and their reservation status. It returns all SQL keywords supported by Spark SQL along with a boolean flag indicating whether each keyword is reserved or non-reserved.

## Syntax
```sql
SELECT * FROM sql_keywords()
```

```scala
// DataFrame API usage
spark.sql("SELECT * FROM sql_keywords()")
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | N/A | This expression takes no arguments |

## Return Type
Returns a table with the following schema:

- `keyword` (StringType, non-nullable): The SQL keyword string
- `reserved` (BooleanType, non-nullable): Whether the keyword is reserved (true) or non-reserved (false)

## Supported Data Types
This expression does not accept input data types as it is a parameterless generator function that produces its own data.

## Algorithm

- Retrieves the complete list of SQL keywords from Spark's internal keyword registry
- Obtains the reservation status for each keyword using `getReservedList()`
- Combines keywords with their corresponding reservation status using zip operation
- Generates InternalRow objects for each keyword-reservation pair
- Returns an iterable collection of rows representing the complete keyword catalog

## Partitioning Behavior
As a generator function:

- Does not preserve input partitioning (generates new data)
- The output is typically collected to a single partition since it's a metadata operation
- No shuffle is required as this is a local data generation operation

## Edge Cases

- Always returns a consistent set of keywords regardless of session state
- Keywords are returned as UTF8String objects to ensure proper encoding
- Both keyword and reserved columns are marked as non-nullable in the schema
- The function generates the same output deterministically across calls

## Code Generation
This expression extends `CodegenFallback`, meaning it does not support Tungsten code generation and always falls back to interpreted evaluation mode for compatibility and simplicity.

## Examples
```sql
-- Get all SQL keywords
SELECT * FROM sql_keywords();

-- Filter for reserved keywords only  
SELECT keyword FROM sql_keywords() WHERE reserved = true;

-- Count total keywords
SELECT COUNT(*) as total_keywords FROM sql_keywords();

-- Find non-reserved keywords containing 'ADD'
SELECT keyword FROM sql_keywords() 
WHERE reserved = false AND keyword LIKE '%ADD%';
```

```scala
// DataFrame API usage
import org.apache.spark.sql.SparkSession
val spark = SparkSession.builder().getOrCreate()

// Get all keywords
val keywords = spark.sql("SELECT * FROM sql_keywords()")
keywords.show()

// Filter and collect reserved keywords
val reserved = spark.sql("SELECT keyword FROM sql_keywords() WHERE reserved = true")
reserved.collect()
```

## See Also

- Table-valued functions for metadata inspection
- `SHOW` commands for schema and catalog information
- Generator expressions like `explode()` and `posexplode()`