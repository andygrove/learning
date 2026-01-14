# InSet

## Overview
InSet is an optimized Catalyst expression for evaluating IN clauses when all filter values are static and known at query planning time. It uses a Set data structure for O(1) lookup performance instead of sequential comparison, making it significantly more efficient than the standard In expression for large value lists.

## Syntax
```sql
column_expression IN (value1, value2, value3, ...)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The expression to test for membership in the value set |
| hset | Set[Any] | A pre-computed set of static values to check against (cannot be null) |

## Return Type
Returns `BooleanType` - true if the child expression value is found in the set, false otherwise, or null under specific null-handling conditions.

## Supported Data Types

- All atomic types (ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType, DecimalType, StringType, DateType, TimestampType, etc.)
- NullType
- Complex types (StructType, ArrayType, MapType) with interpreted ordering
- Special handling for StringType with collation awareness
- BinaryType (uses TreeSet with interpreted ordering)

## Algorithm

- Pre-computes the value set at expression creation time for optimal lookup performance
- Uses different Set implementations based on data type: CollationAwareSet for non-UTF8 strings, TreeSet for complex types, regular HashSet for atomic types
- Performs null-safe evaluation with O(1) containment checks
- Handles NaN values specially for floating-point types (Float, Double)
- Falls back to TreeSet with interpreted ordering for complex data types to support comparison between UnsafeRow and regular row formats

## Partitioning Behavior
InSet is a predicate expression that does not directly affect partitioning:

- Preserves existing partitioning when used in filter operations
- Does not require shuffle operations as it only evaluates row-level predicates
- Can be pushed down to data sources for partition pruning when the partitioning column matches the child expression

## Edge Cases

- **Null handling**: Returns null if child evaluates to null, or if child value not found but set contains null
- **Empty set behavior**: Returns false for empty sets under current behavior (legacy mode returns null if child is null)
- **NaN handling**: For Float/Double types, NaN values are handled specially - if input is NaN, returns true only if set contains NaN
- **Collation support**: String comparisons respect collation settings for non-UTF8 binary collations
- **Legacy compatibility**: Behavior changes based on `spark.sql.legacy.nullInEmptyBehavior` configuration

## Code Generation
InSet supports Tungsten code generation with two optimization strategies:

- **Switch statement generation**: For integer-like types (Byte, Short, Int, Date) when set size is below `spark.sql.optimizer.inSetSwitchThreshold`
- **Set-based code generation**: For all other cases, generates code that references the pre-built Set object
- Falls back to interpreted evaluation for very large sets or unsupported code generation scenarios

## Examples
```sql
-- Basic usage
SELECT * FROM table WHERE id IN (1, 2, 3, 4, 5);

-- With string values
SELECT * FROM table WHERE status IN ('ACTIVE', 'PENDING', 'COMPLETED');

-- With null handling
SELECT * FROM table WHERE category IN ('A', 'B', NULL);
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._
df.filter(col("id").isin(1, 2, 3, 4, 5))

// Programmatic creation (internal API)
val insetExpr = InSet(col("id").expr, Set(1, 2, 3, 4, 5))
```

## See Also

- **In**: The standard IN expression for dynamic value lists
- **EqualTo**: For single value equality comparisons  
- **Contains**: For array/string containment operations
- **Predicate**: Base trait for boolean-returning expressions