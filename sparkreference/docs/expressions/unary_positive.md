# UnaryPositive

## Overview
The UnaryPositive expression represents the unary plus operator (+) applied to a numeric or interval expression. It is a runtime-replaceable expression that effectively returns the input value unchanged, serving as a no-op operation that preserves the original expression's value and data type.

## Syntax
```sql
SELECT +expression
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The numeric or interval expression to apply the unary plus operator to |

## Return Type
Returns the same data type as the input expression. The output data type is determined by `child.dataType`.

## Supported Data Types

- All numeric types (IntegerType, LongType, FloatType, DoubleType, DecimalType, etc.)
- All interval types (CalendarIntervalType, YearMonthIntervalType, DayTimeIntervalType)

## Algorithm

- The expression implements the `RuntimeReplaceable` trait, meaning it is replaced at runtime
- During optimization, the entire UnaryPositive expression is replaced with its child expression
- No actual computation is performed - it's essentially a pass-through operation
- The replacement happens through the `lazy val replacement: Expression = child` implementation
- Supports context-independent constant folding when the child expression is foldable

## Partitioning Behavior
- Preserves partitioning since it's a no-op that doesn't modify data distribution
- Does not require shuffle operations
- Maintains the same partitioning properties as the child expression

## Edge Cases

- **Null handling**: Preserves null values unchanged (returns null if input is null)
- **Empty input**: Not applicable as this operates on individual expressions, not collections
- **Overflow behavior**: No overflow concerns since no arithmetic computation is performed
- **Type preservation**: Exactly preserves the input data type and precision for decimal types

## Code Generation
This expression supports code generation through the RuntimeReplaceable mechanism. Since it gets replaced by its child expression during query planning, the code generation behavior depends entirely on the child expression's code generation capabilities.

## Examples
```sql
-- Example SQL usage
SELECT +1;
-- Returns: 1

SELECT +(-5);
-- Returns: -5

SELECT +salary FROM employees;
-- Returns the salary values unchanged
```

```scala
// Example DataFrame API usage
import org.apache.spark.sql.functions._

// Using unary plus (though rarely needed in practice)
df.select(col("amount").unary_+)

// More commonly seen in SQL expressions
spark.sql("SELECT +price FROM products")
```

## See Also

- UnaryMinus - The unary minus operator (-)
- Add - Binary addition operator
- NumericAndInterval type collection for supported input types