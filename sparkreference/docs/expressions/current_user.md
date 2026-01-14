# CurrentUser

## Overview
The CurrentUser expression returns the current authenticated user name in Apache Spark. This is a leaf expression that produces a string value representing the user context under which the Spark application is running, commonly used for auditing and security purposes.

## Syntax
```sql
current_user()
```

```scala
// DataFrame API
import org.apache.spark.sql.functions._
df.select(expr("current_user()"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | - | This expression takes no arguments |

## Return Type
String - Returns the current user name as a string value.

## Supported Data Types
This expression does not accept input data types as it takes no parameters. It always returns a string representing the current user.

## Algorithm

- Retrieves the current user context from the Spark session or execution environment

- Returns the authenticated user name as determined by the underlying security framework

- The actual user resolution is handled at execution time, not during analysis phase

- Uses the system's authentication mechanism to determine the current user identity

- Always produces a non-null string value representing the user

## Partitioning Behavior
This expression has minimal impact on partitioning behavior:

- Preserves existing partitioning as it doesn't depend on data values

- Does not require shuffle operations since it's not data-dependent

- Can be computed independently on each partition without cross-partition dependencies

## Edge Cases

- Never returns null values (nullable = false in the implementation)

- Returns consistent user identity across all partitions in the same query execution

- User identity is determined at query execution time, not at query planning time

- Behavior may vary between different Spark deployment modes (local, cluster, etc.)

- The actual user returned depends on the authentication mechanism configured

## Code Generation
This expression is marked as `Unevaluable`, meaning it does not support direct code generation through Tungsten. The actual evaluation is deferred to runtime through Spark's expression evaluation framework, likely requiring interpreted mode execution for user context resolution.

## Examples
```sql
-- Get current user in a query
SELECT current_user() as authenticated_user;

-- Use in audit logging
SELECT *, current_user() as query_user 
FROM sensitive_table 
WHERE department = 'finance';
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Add current user to results
val df = spark.table("employees")
val withUser = df.select($"*", expr("current_user()").alias("query_user"))

// Use in filtering with audit trail
val auditDF = df.filter($"salary" > 100000)
  .select($"*", expr("current_user()").alias("accessed_by"))
```

## See Also

- `current_timestamp()` - for temporal context in audit trails
- `current_database()` - for database context information
- Security and authentication configuration in Spark deployment