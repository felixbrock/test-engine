def getDistributionQuery(dbName: str, schemaName: str, materializationName: str, columnName: str):
    return f"""select median("{columnName}") as median from "{dbName}"."{schemaName}"."{materializationName}";"""


def getCardinalityQuery(dbName: str, schemaName: str, materializationName: str, columnName: str):
    return f"""
    select count(distinct("{columnName}")) as distinct_value_count 
    from "{dbName}"."{schemaName}"."{materializationName}";
  """


def getUniquenessQuery(dbName: str, schemaName: str, materializationName: str, columnName: str):
    return f"""
    select count(distinct("{columnName}")) as distinct_value_count,
    count("{columnName}") as non_null_value_count,
    iff(non_null_value_count = 0, 0, distinct_value_count/non_null_value_count) as uniqueness_rate
    from "{dbName}"."{schemaName}"."{materializationName}";
  """


def getNullnessQuery(dbName: str, schemaName: str, materializationName: str, columnName: str):
    return f"""
    select sum(case when "{columnName}" is null then 1 else 0 end) as null_value_count,
    count("{columnName}") as non_null_value_count,
    iff((null_value_count + non_null_value_count) = 0, 0, null_value_count/(null_value_count + non_null_value_count)) as nullness_rate 
    from "{dbName}"."{schemaName}"."{materializationName}";
  """


def getFreshnessQuery(dbName: str, schemaName: str, materializationName: str, columnName: str):
    return f"""  select
  sysdate() as now, 
  datediff(minute, "{columnName}", now) as time_diff
  from "{dbName}"."{schemaName}"."{materializationName}"
  order by "{columnName}" desc nulls last
  limit 1;
  """
