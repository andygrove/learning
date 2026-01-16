# Comet Spark Expression Implementation Pipeline

This document tracks Spark expressions not yet implemented in Apache DataFusion Comet, categorized by implementation difficulty.

**Repository:** `datafusion-comet/`

## Implementation Guide

To add a new expression:
1. Add Scala serialization handler in `spark/src/main/scala/org/apache/comet/serde/`
2. Add protobuf definition in `native/proto/src/proto/expr.proto`
3. Add Rust implementation in `native/spark-expr/src/`
4. Register in `QueryPlanSerde.scala`

See: `docs/source/contributor-guide/adding_a_new_expression.md`

---

## Already Implemented (need doc update)

These expressions ARE implemented but not marked in `docs/spark_expressions_support.md`:

### Math (via CometScalarFunction)
- [x] `cosh` - Hyperbolic cosine
- [x] `sinh` - Hyperbolic sine
- [x] `tanh` - Hyperbolic tangent
- [x] `expm1` - exp(x) - 1
- [x] `cot` - Cotangent
- [x] `hex` - Convert to hex string

### Hash
- [x] `sha1` - SHA-1 hash
- [x] `sha2` - SHA-2 hash
- [x] `xxhash64` - xxHash64

### DateTime
- [x] `year` - Extract year
- [x] `month` - Extract month
- [x] `day`/`dayofmonth` - Extract day of month
- [x] `dayofweek` - Extract day of week
- [x] `dayofyear` - Extract day of year
- [x] `weekday` - Extract weekday (Mon=0)
- [x] `weekofyear` - Extract week of year
- [x] `quarter` - Extract quarter
- [x] `hour` - Extract hour
- [x] `minute` - Extract minute
- [x] `second` - Extract second
- [x] `date_add`/`dateadd` - Add days to date
- [x] `date_sub` - Subtract days from date
- [x] `trunc` - Truncate date
- [x] `date_trunc` - Truncate timestamp

### Array
- [x] `array_min` - Get minimum array element
- [x] `flatten` - Flatten nested arrays
- [x] `size` - Get array size (arrays only, not maps)

### Aggregate
- [x] `corr` - Correlation

### Predicate
- [x] `isnan` - Check if NaN (via CometIsNaN in mathExpressions)

### String
- [x] `concat` - Concatenate strings (CometConcat)
- [x] `substring`/`substr` - Substring extraction (CometSubstring)

---

## Small (1-2 hours)

Simple scalar functions that likely have DataFusion equivalents or trivial implementations.

### Math Functions
- [ ] `acosh` - Inverse hyperbolic cosine
- [ ] `asinh` - Inverse hyperbolic sine
- [ ] `atanh` - Inverse hyperbolic tanh
- [ ] `cbrt` - Cube root
- [ ] `degrees` - Convert radians to degrees
- [ ] `radians` - Convert degrees to radians
- [ ] `e` - Euler's number constant
- [ ] `pi` - Pi constant
- [ ] `log1p` - ln(1 + x)
- [ ] `rint` - Round to nearest integer
- [ ] `hypot` - Hypotenuse calculation
- [ ] `csc` - Cosecant
- [ ] `sec` - Secant

### String Functions
- [ ] `base64` - Encode to base64
- [ ] `unbase64` - Decode from base64
- [ ] `left` - Get leftmost n characters
- [ ] `right` - Get rightmost n characters
- [ ] `locate` - Find substring position
- [ ] `position` - Find substring position (ANSI)
- [ ] `soundex` - Phonetic encoding
- [ ] `split` - Split string by delimiter
- [ ] `split_part` - Get specific part after split

### Bitwise Functions
- [ ] `bit_count` - Count set bits
- [ ] `bit_get`/`getbit` - Get bit at position
- [ ] `shiftrightunsigned` - Unsigned right shift

### Hash Functions
- [ ] `crc32` - CRC32 checksum
- [ ] `hash` - Spark internal hash

### Conditional Functions
- [ ] `nanvl` - Return alt value if NaN
- [ ] `when` - SQL CASE WHEN (CaseWhen exists but not standalone `when`)

### Misc Functions
- [ ] `typeof` - Get data type name
- [ ] `version` - Spark version string
- [ ] `uuid` - Generate UUID

---

## Medium (2-8 hours)

Functions requiring custom logic, multiple data type handling, or moderate complexity.

### Math Functions
- [ ] `bin` - Convert to binary string
- [ ] `conv` - Convert between number bases
- [ ] `bround` - Banker's rounding
- [ ] `pmod` - Positive modulo
- [ ] `div` - Integer division
- [ ] `factorial` - Factorial calculation
- [ ] `greatest` - Return greatest value
- [ ] `least` - Return least value
- [ ] `width_bucket` - Histogram bucket assignment

### String Functions
- [ ] `decode` - Decode bytes to string
- [ ] `encode` - Encode string to bytes
- [ ] `elt` - Return nth element
- [ ] `find_in_set` - Find position in comma-separated list
- [ ] `format_number` - Format number with locale
- [ ] `format_string`/`printf` - Format string with arguments
- [ ] `levenshtein` - Edit distance
- [ ] `mask` - Mask sensitive data
- [ ] `overlay` - Overlay substring
- [ ] `sentences` - Split text into sentences
- [ ] `substring_index` - Get substring before/after delimiter
- [ ] `to_char` - Format number to string
- [ ] `to_number`/`try_to_number` - Parse string to number
- [ ] `to_binary`/`try_to_binary` - Parse string to binary

### Regex Functions
- [ ] `regexp_count` - Count regex matches
- [ ] `regexp_extract` - Extract regex group
- [ ] `regexp_extract_all` - Extract all regex matches
- [ ] `regexp_instr` - Find regex match position
- [ ] `regexp_substr` - Extract regex substring
- [ ] `regexp`/`regexp_like`/`rlike` - Regex matching (RLike partially exists)

### Array Functions
- [ ] `array_position` - Find element position
- [ ] `arrays_zip` - Zip multiple arrays
- [ ] `sequence` - Generate sequence array
- [ ] `shuffle` - Shuffle array elements
- [ ] `slice` - Extract array slice
- [ ] `sort_array` - Sort array elements

### Collection Functions
- [ ] `array_size` - Get array size (separate from `size`)
- [ ] `cardinality` - Get collection size

### Date/Time Functions
- [ ] `add_months` - Add months to date
- [ ] `date_diff`/`datediff` - Days between dates
- [ ] `date_format` - Format date to string
- [ ] `date_from_unix_date` - Convert Unix date to date
- [ ] `last_day` - Last day of month
- [ ] `next_day` - Next day of week
- [ ] `months_between` - Months between dates
- [ ] `to_date` - Parse string to date
- [ ] `to_timestamp`/`to_timestamp_ltz`/`to_timestamp_ntz` - Parse string to timestamp
- [ ] `try_to_timestamp` - Try to parse timestamp
- [ ] `unix_timestamp`/`to_unix_timestamp` - Convert to Unix timestamp
- [ ] `unix_date` - Convert date to Unix days
- [ ] `unix_seconds`/`unix_millis`/`unix_micros` - Extract Unix time
- [ ] `timestamp_seconds`/`timestamp_millis`/`timestamp_micros` - Create timestamp
- [ ] `current_timestamp`/`now`/`localtimestamp` - Current timestamp

### Map Functions
- [ ] `map` - Create map
- [ ] `map_concat` - Concatenate maps
- [ ] `map_contains_key` - Check key exists
- [ ] `map_from_entries` - Create map from entries
- [ ] `str_to_map` - Parse string to map
- [ ] `try_element_at` - Try to get element

### Aggregate Functions
- [ ] `approx_count_distinct` - Approximate distinct count
- [ ] `collect_list` - Collect values to list
- [ ] `collect_set` - Collect unique values to set
- [ ] `histogram_numeric` - Numeric histogram
- [ ] `kurtosis` - Kurtosis statistic
- [ ] `skewness` - Skewness statistic
- [ ] `max_by` - Max value by ordering column
- [ ] `min_by` - Min value by ordering column
- [ ] `mode` - Most frequent value
- [ ] `median` - Median value
- [ ] `percentile`/`percentile_approx`/`approx_percentile` - Percentile calculations
- [ ] `try_avg` - Try average (null on overflow)
- [ ] `try_sum` - Try sum (null on overflow)
- [ ] `array_agg` - Aggregate to array

### Struct Functions
- [ ] `named_struct` - Create named struct (CreateNamedStruct exists but `named_struct` SQL not exposed?)
- [ ] `struct` - Create struct

### Conversion Functions
- [ ] `bigint`/`int`/`smallint`/`tinyint` - Integer casts
- [ ] `binary` - Binary cast
- [ ] `boolean` - Boolean cast
- [ ] `cast` - General cast (exists but needs completion)
- [ ] `date` - Date cast
- [ ] `decimal` - Decimal cast
- [ ] `double`/`float` - Float casts
- [ ] `string` - String cast
- [ ] `timestamp` - Timestamp cast

### Misc Functions
- [ ] `input_file_name` - Get input file name
- [ ] `input_file_block_start` - Get file block start
- [ ] `input_file_block_length` - Get file block length
- [ ] `assert_true` - Assert condition
- [ ] `raise_error` - Raise error

---

## Large (8+ hours)

Complex features requiring significant infrastructure or architectural changes.

### Window Functions
- [ ] `row_number` - Row number
- [ ] `rank` - Rank with gaps
- [ ] `dense_rank` - Rank without gaps
- [ ] `percent_rank` - Percentile rank
- [ ] `cume_dist` - Cumulative distribution
- [ ] `ntile` - N-tile bucket
- [ ] `lag` - Previous row value
- [ ] `lead` - Next row value
- [ ] `nth_value` - Nth row value

### Generator Functions (UDTF)
- [ ] `explode` - Explode array to rows
- [ ] `explode_outer` - Explode with nulls
- [ ] `posexplode` - Explode with position
- [ ] `posexplode_outer` - Posexplode with nulls
- [ ] `inline` - Explode struct array
- [ ] `inline_outer` - Inline with nulls
- [ ] `stack` - Stack columns to rows

### Lambda/Higher-Order Functions
- [ ] `aggregate`/`reduce` - Aggregate array with function
- [ ] `array_sort` - Sort with comparator
- [ ] `exists` - Check if any element matches
- [ ] `filter` - Filter array elements (ArrayFilter exists but limited to null filtering)
- [ ] `forall` - Check if all elements match
- [ ] `transform` - Transform array elements
- [ ] `transform_keys` - Transform map keys
- [ ] `transform_values` - Transform map values
- [ ] `map_filter` - Filter map entries
- [ ] `map_zip_with` - Zip maps with function
- [ ] `zip_with` - Zip arrays with function

### JSON Functions
- [ ] `from_json` - Parse JSON to struct (JsonToStructs exists but limited)
- [ ] `to_json` - Convert to JSON (StructsToJson exists but limited)
- [ ] `get_json_object` - Extract JSON path
- [ ] `json_array_length` - Get JSON array length
- [ ] `json_object_keys` - Get JSON object keys
- [ ] `json_tuple` - Extract multiple JSON fields
- [ ] `schema_of_json` - Infer JSON schema

### CSV Functions
- [ ] `from_csv` - Parse CSV to struct
- [ ] `to_csv` - Convert to CSV
- [ ] `schema_of_csv` - Infer CSV schema

### XML Functions
- [ ] `xpath` - XPath string extraction
- [ ] `xpath_boolean` - XPath boolean
- [ ] `xpath_double`/`xpath_float`/`xpath_number` - XPath numeric
- [ ] `xpath_int`/`xpath_long`/`xpath_short` - XPath integer
- [ ] `xpath_string` - XPath string

### URL Functions
- [ ] `parse_url` - Parse URL components
- [ ] `url_encode` - URL encode
- [ ] `url_decode` - URL decode

### Timezone Functions
- [ ] `convert_timezone` - Convert between timezones
- [ ] `from_utc_timestamp` - Convert from UTC
- [ ] `to_utc_timestamp` - Convert to UTC
- [ ] `make_dt_interval` - Create day-time interval
- [ ] `make_ym_interval` - Create year-month interval
- [ ] `make_interval` - Create interval
- [ ] `make_date` - Create date from parts
- [ ] `make_timestamp`/`make_timestamp_ltz`/`make_timestamp_ntz` - Create timestamp from parts

### Aggregate Functions (Complex)
- [ ] `grouping` - Grouping set indicator
- [ ] `grouping_id` - Grouping set bitmap
- [ ] `count_min_sketch` - Count-min sketch
- [ ] `regr_intercept` - Regression intercept
- [ ] `regr_r2` - Regression R-squared
- [ ] `regr_slope` - Regression slope
- [ ] `regr_sxx`/`regr_sxy`/`regr_syy` - Regression sums

### Encryption Functions
- [ ] `aes_encrypt` - AES encryption
- [ ] `aes_decrypt` - AES decryption

---

## Implementation Status Summary

### Expressions by Category

| Category | Implemented | Total | Missing |
|----------|-------------|-------|---------|
| Math | ~35 | ~53 | ~18 |
| String | ~32 | ~65 | ~33 |
| Array | ~18 | ~22 | ~4 |
| DateTime | ~16 | ~58 | ~42 |
| Aggregate | ~18 | ~52 | ~34 |
| Hash | ~5 | ~7 | ~2 |
| Bitwise | ~8 | ~9 | ~1 |
| Predicate | ~16 | ~18 | ~2 |
| Conditional | ~6 | ~8 | ~2 |
| Map | ~5 | ~11 | ~6 |
| Struct | ~3 | ~5 | ~2 |
| Conversion | ~1 | ~13 | ~12 |
| Window | 0 | 9 | 9 |
| Generator | 0 | 7 | 7 |
| Lambda | 0 | 12 | 12 |
| JSON | ~2 | 7 | ~5 |
| CSV | 0 | 3 | 3 |
| XML | 0 | 9 | 9 |
| URL | 0 | 3 | 3 |
| Misc | ~10 | ~17 | ~7 |
| **TOTAL** | **~175** | **~380** | **~205** |

### High Priority Recommendations

1. **Window Functions** - Major Spark feature, enables significant query coverage
2. **Generator Functions (explode)** - Very common in data processing
3. **DateTime completion** - Many already partially exist
4. **collect_list/collect_set** - Very common aggregations

### Quick Wins (Already in DataFusion)
These likely just need the Scala serde mapping since DataFusion already supports them:
- `acosh`, `asinh`, `atanh` - Inverse hyperbolic functions
- `cbrt` - Cube root
- `degrees`, `radians` - Angle conversions
- `pi`, `e` - Constants
- `base64`, `unbase64` - Base64 encoding

### Files to Reference

**Scala Serde:**
- `spark/src/main/scala/org/apache/comet/serde/QueryPlanSerde.scala` - Main expression registry
- `spark/src/main/scala/org/apache/comet/serde/CometScalarFunction.scala` - Simple scalar function wrapper

**Existing Implementations:**
- `math.scala`, `strings.scala`, `arrays.scala`, `datetime.scala`, `hash.scala`, `aggregates.scala`

**Rust Native:**
- `native/spark-expr/src/` - All Rust implementations
