from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, lit

def clean_dataframe(
    df: DataFrame,
    string_null_value: str = "DESCONHECIDO",
    numeric_null_value: float = 0
) -> DataFrame:
    """
    Cleans null values and fields containing only special characters in string columns.
    Also fills null values in numeric columns.
    
    Args:
        df (DataFrame): Input DataFrame.
        string_null_value (str): Value to replace NULLs and special characters in string columns.
        numeric_null_value (float/int): Value to replace NULLs in numeric columns.
    
    Returns:
        DataFrame: Cleaned DataFrame.
    """

    string_cols = [c for c, t in df.dtypes if t == "string"]
    double_cols = [c for c, t in df.dtypes if t in ("double", "float", "int", "bigint")]

    special_chars_regex = r'^[^a-zA-Z0-9]+$'

    for c in string_cols:
        df = df.withColumn(
            c,
            when(col(c).isNull(), lit(string_null_value))
            .when(col(c).rlike(special_chars_regex), lit(string_null_value))
            .otherwise(col(c))
        )

    for c in double_cols:
        df = df.withColumn(
            c,
            when(col(c).isNull(), lit(numeric_null_value)).otherwise(col(c))
        )

    return df