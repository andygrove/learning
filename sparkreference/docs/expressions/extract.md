# Extract

## Overview
The `Extract` expression extracts a specific field (such as year, month, day, hour, etc.) from a date, timestamp, or interval value. This expression is equivalent to the `date_part(field, source)` function and serves as a runtime-replaceable expression that delegates its evaluation to other underlying expressions.

## Syntax
```sql
-- Standard EXTRACT syntax
EXTRACT(field FROM source)

-- Alternative date_part syntax  
date_part(field, source)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| field | Expression | The field to extract (e.g., 'YEAR', 'MONTH', 'DAY', 'HOUR', etc.) |
| source | Expression | The date, timestamp, or interval value from which to extract the field |
| replacement | Expression | Internal expression that performs the actual computation |

## Return Type
Returns an integer value representing the extracted field component.

## Supported Data Types

- **Source types**: DATE, TIMESTAMP, TIMESTAMP_NTZ, INTERVAL
- **Field types**: String literals representing valid date/time fields
- **Output type**: INTEGER

## Algorithm

- The expression acts as a runtime-replaceable wrapper that delegates to underlying extract implementations
- Creates an internal replacement expression using `Extract.createExpr("extract", field, source)`  
- The replacement expression handles the actual field extraction logic based on the field type and source data type
- SQL string generation adapts based on function alias (uses "FROM" syntax for extract, comma syntax for date_part)
- Inherits analysis rules from its replacement expression for proper type checking and validation

## Partitioning Behavior
How this expression affects partitioning:

- Preserves partitioning when used in projections as it operates row-by-row
- Does not require shuffle operations
- Can be safely pushed down to data sources that support extract operations

## Edge Cases

- **Null handling**: Returns null if either the field or source expression is null
- **Invalid fields**: Throws analysis exception for unsupported field names during query planning
- **Type mismatches**: Fails during analysis if source type doesn't support the requested field extraction
- **Timezone handling**: Behavior depends on the underlying replacement expression's timezone logic for timestamp inputs

## Code Generation
This expression supports code generation through its replacement expression. The actual code generation capability depends on the specific underlying expression created by `Extract.createExpr()`, which typically generates efficient Java code for field extraction operations.

## Examples
```sql
-- Extract year from a date
SELECT EXTRACT(YEAR FROM DATE '2023-12-25') AS year_value;

-- Extract month from timestamp  
SELECT EXTRACT(MONTH FROM CURRENT_TIMESTAMP()) AS current_month;

-- Alternative date_part syntax
SELECT date_part('DAY', DATE '2023-12-25') AS day_value;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Extract year from date column
df.select(date_part(lit("YEAR"), col("date_column")))

// Extract hour from timestamp
df.select(date_part(lit("HOUR"), col("timestamp_column")))
```

## See Also

- `DatePart` - The underlying implementation for date part extraction
- `Year`, `Month`, `DayOfMonth` - Specialized expressions for common extractions  
- `Hour`, `Minute`, `Second` - Time-specific extraction expressions
- `DateAdd`, `DateDiff` - Related date manipulation functions