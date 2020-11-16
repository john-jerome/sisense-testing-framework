import re

def filter_ref_replace(data):
    """Convert Periscope-specific syntax into raw SQL code for further execution.

    Args:
        data (array of dict): original data

    Returns:
        data (array of dict): data after removing all Periscope-specific SQL syntax
    """
    
    # for date aggregations
    exp1 = r"\[([^][:]*)\:(sec|min|hour|day|date|week|month|year|month_of_year|aggregation)\]" 
    # for [channel_grouping] reference in Periscope
    exp2 = r"\[channel_grouping\]"
    # for elements like where ... [] group by (order by):
    exp3 = r"(where((?!where).)*\[[^0-9].*?\].*?(?=(group\s*by|order\s*by|union|qualify|\)\s*\,|\)\s*order|\)\s*select)))|(where((?!where).)*\[[^0-9].*?\].*$)" 
    # for elements like [X|Y]
    exp4 = r"\[([^][|]*)\|([^][|]*)\]" 

    for row in data:
        row['SQL_CODE_RAW'] = re.sub(exp4, r"\2", row['SQL_CODE_RAW'], flags = re.S|re.I)
        row['SQL_CODE_RAW'] = re.sub(exp1, r"\1", row['SQL_CODE_RAW'], flags = re.S|re.I)
        row['SQL_CODE_RAW'] = re.sub(exp2, r"null", row['SQL_CODE_RAW'], flags = re.S|re.I)
        row['SQL_CODE_RAW'] = re.sub(exp3, r"", row['SQL_CODE_RAW'], flags = re.S|re.I)
    
    return data

def view_ref_replace(data, reference_data):
    """Replace the [view_reference] with the corresponding view SQL code.

    Args:
        data (array of dict): original data
        reference_data (array of dict): view data

    Returns:
        data (array of dict): data after replacing all view references
    """
    
    
    for row1 in data:

        row1['SQL_CODE_RAW'] = row1['SQL_CODE']

        for row2 in reference_data:
            view_ref = '[' + row2['NAME'] + ']'
            if view_ref in row1['SQL_CODE']:
                view_code = '(' + row2['SQL_CODE'] + ') ' + row2['NAME']
                row1['SQL_CODE_RAW'] = row1['SQL_CODE_RAW'].replace(view_ref, view_code)

    return data