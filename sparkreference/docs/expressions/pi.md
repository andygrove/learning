# Pi

## Overview
The `Pi` expression returns the mathematical constant π (pi) as a double-precision floating-point value. This is a leaf expression that produces the constant value 3.141592653589793 without requiring any input arguments.

## Syntax
```sql
PI()
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.lit
lit(math.Pi)
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| None | - | This expression takes no arguments |

## Return Type
`DoubleType` - Returns a double-precision floating-point number representing the mathematical constant π.

## Supported Data Types
This expression does not accept input data types as it is a parameterless constant function.

## Algorithm

- Inherits from `LeafMathExpression` with the constant value `math.Pi`
- Directly returns the pre-computed Java `Math.PI` constant (3.141592653589793)
- No computation is performed at runtime - the value is embedded as a literal
- Implements the standard Catalyst expression evaluation framework
- Expression name is registered as "PI" in the function registry

## Partitioning Behavior
Since this is a constant expression that produces the same value regardless of input:

- Preserves all partitioning schemes as it doesn't depend on data values
- Does not require shuffle operations
- Can be safely pushed down in query optimization
- Deterministic and produces identical results across all partitions

## Edge Cases

- Always returns the same non-null constant value
- Cannot produce null values under any circumstances
- No overflow or underflow concerns as it returns a fixed constant
- Thread-safe as it contains no mutable state
- No special input validation required since no inputs are accepted

## Code Generation
This expression supports Spark's Tungsten code generation framework as it extends `LeafMathExpression`, which implements the necessary code generation methods for efficient runtime execution.

## Examples
```sql
-- Basic usage
SELECT PI();
-- Result: 3.141592653589793

-- Using in calculations
SELECT PI() * 2 AS two_pi;
-- Result: 6.283185307179586

-- Circle area calculation
SELECT PI() * POWER(radius, 2) AS area FROM circles;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Direct constant
df.select(lit(math.Pi).alias("pi_value"))

// In calculations  
df.select((lit(math.Pi) * col("radius") * col("radius")).alias("area"))
```

## See Also

- `E()` - Euler's number constant
- Trigonometric functions: `SIN`, `COS`, `TAN`
- `ACOS`, `ASIN`, `ATAN` - Inverse trigonometric functions

---

# Acos

## Overview
The `Acos` expression computes the inverse cosine (arc cosine) of a numeric input value. It returns the angle in radians whose cosine is the input value, with results in the range [0, π].

## Syntax
```sql
ACOS(expr)
```

```scala
// DataFrame API
import org.apache.spark.sql.functions.acos
acos(col("column_name"))
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| expr | Numeric | A numeric expression with value in the range [-1, 1] |

## Return Type
`DoubleType` - Returns a double-precision floating-point number representing the arc cosine in radians.

## Supported Data Types
Accepts all numeric data types as input:

- `ByteType`, `ShortType`, `IntegerType`, `LongType`
- `FloatType`, `DoubleType`  
- `DecimalType`

All inputs are cast to `DoubleType` for computation.

## Algorithm

- Inherits from `UnaryMathExpression` using Java's `Math.acos` function
- Input values are cast to double-precision floating-point format
- Delegates computation to `java.lang.Math.acos(double)` method
- Returns NaN for input values outside the valid domain [-1, 1]
- Expression is registered with function name "ACOS"

## Partitioning Behavior
This expression preserves partitioning characteristics:

- Maintains existing partition boundaries as it's a row-wise transformation
- Does not require data shuffling or repartitioning
- Can be safely pushed down to individual partitions for parallel execution
- Deterministic function that produces consistent results for same inputs

## Edge Cases

- Returns `NaN` for input values outside the range [-1, 1] (e.g., ACOS(2) = NaN)
- Returns `null` when input is `null` (standard null propagation)
- ACOS(-1) returns π (3.141592653589793)
- ACOS(0) returns π/2 (1.5707963267948966)
- ACOS(1) returns 0.0
- Handles positive and negative zero consistently

## Code Generation
Supports Spark's Tungsten code generation through the `UnaryMathExpression` base class, enabling optimized runtime code generation for better performance in tight loops.

## Examples
```sql
-- Basic usage
SELECT ACOS(1);
-- Result: 0.0

SELECT ACOS(0);  
-- Result: 1.5707963267948966

SELECT ACOS(-1);
-- Result: 3.141592653589793

-- Invalid input
SELECT ACOS(2);
-- Result: NaN

-- With table data
SELECT value, ACOS(value) AS arc_cosine 
FROM trigonometry_data 
WHERE value BETWEEN -1 AND 1;
```

```scala
// DataFrame API usage
import org.apache.spark.sql.functions._

// Basic usage
df.select(acos(col("cosine_value")))

// With filtering for valid domain
df.filter(col("value") >= -1 && col("value") <= 1)
  .select(col("value"), acos(col("value")).alias("arc_cosine"))

// Converting result to degrees
df.select((acos(col("cosine_value")) * 180 / math.Pi).alias("degrees"))
```

## See Also

- `ASIN` - Inverse sine function
- `ATAN` - Inverse tangent function  
- `COS` - Cosine function
- `SIN`, `TAN` - Other trigonometric functions
- `PI()` - Mathematical constant π