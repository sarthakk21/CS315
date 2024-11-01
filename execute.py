# You are allowed to import any modules whatsoever (not even numpy, sklearn etc)
# The use of file IO is forbidden. Your code should not read from or write onto files

# SUBMIT YOUR CODE AS TWO PYTHON (.PY) FILES INSIDE A ZIP ARCHIVE
# THE NAME OF THE PYTHON FILES MUST BE index.py and execute.py

# DO NOT CHANGE THE NAME OF THE METHODS my_execute BELOW
# THESE WILL BE INVOKED BY THE EVALUATION SCRIPT. CHANGING THESE NAMES WILL CAUSE EVALUATION FAILURE

# You may define any new functions, variables, classes here
# For example, functions to create indices or statistics

def binary_search_year(yearly_roots, target_year):
    left, right = 0, len(yearly_roots) - 1
    while left <= right:
        mid = (left + right) // 2
        year, _ = yearly_roots[mid]
        if year == target_year:
            return mid 
        elif year < target_year:
            left = mid + 1      
        else:
            right = mid - 1 
    return -1


def execute_name_equals(trie, name):
    current = trie
    for char in name:
        if current.child[ord(char) - ord('a')] is None:
            return []
        current = current.child[ord(char) - ord('a')]
    if current.wordEnd:
        return list(range(current.start,current.start + current.count))
    return []

def execute_name_like(trie, prefix):
    current = trie
    for char in prefix:
        if current.child[ord(char)-ord('a')] is None:
            return []
        current = current.child[ord(char) - ord('a')]
    return list(range(current.start,current.end + 1))

def execute_year_query(year_map, operator, value):
    if operator == '=':
        found_pos = binary_search_year(year_map,value)
        if found_pos != -1:
            current = year_map[found_pos][1]
            return list(range(current.start,current.end+1))
    elif operator == '<=':
        result = []
        for i in year_map:
            if i[0]<=value:
                current = i[1]
                result.extend(list(range(current.start,current.end+1)))
            else:
                break
        return result
    elif operator == '>=':
        result = []
        for i in reversed(year_map):
            if i[0]>=value:
                current = i[1]
                result.extend(list(range(current.start,current.end+1)))
            else:
                break
        return result
    return []

def execute_composite(op, op1, val, val1, year_map):
    result = []
    # Determine which function to use based on 'op' only once
    execute_fn = execute_name_equals if op == '=' else execute_name_like
    # Adjust the 'val' based on function to avoid slicing repeatedly
    val_processed = val[1:-1] if op == '=' else val[1:-2]
    found_pos = binary_search_year(year_map,val1)
    if op1 == '=':
        if found_pos != -1 :
            current = year_map[found_pos][1]
            return execute_fn(current, val_processed)
    elif op1 == '<=':
        result = []
        for i in year_map:
            if i[0]<=val1:
                current = i[1]
                result.extend(execute_fn(current, val_processed))
            else:
                break
    elif op1 == '>=':
        result = []
        for i in reversed(year_map):
            if i[0]>=val1:
                current = i[1]
                result.extend(execute_fn(current, val_processed))
            else:
                break
    return result



################################
# Non Editable Region Starting #
################################
def my_execute( clause, idx ):

################################
#  Non Editable Region Ending  #
################################

	# Use this method to take a WHERE clause specification
	# and return results of the resulting query
	# clause is a list containing either one or two predicates
	# Each predicate is itself a list of 3 objects, column name, comparator and value
	# idx contains the packaged variable returned by the my_index method
	# Use this method to take a WHERE clause specification
    # and return results of the resulting query
    # clause is a list containing either one or two predicates
    # Each predicate is itself a list of 3 objects, column name, comparator and value
    # idx contains the packaged variable returned by the my_index method

    # Initialize an empty list to store final disk locations
    diskloc_list = []
    op_1 = None
    val_1 = None
    # Process each predicate in the clause
    itr = 0
    for predicate in clause:
        field, operator, value = predicate
        if len(clause) == 2 and itr == 0:
            val_1 = value
            op_1 = operator
            itr+=1
            continue
        elif len(clause) == 2 and itr == 1:
            break
        if field == 'name':
            if operator == '=':
                diskloc_list.extend(execute_name_equals(idx[0][1], value[1:-1]))
            elif operator == 'LIKE':
                # Trim the '%' from value since we are assuming predicates end with this for LIKE
                value = value[1:-2]
                diskloc_list.extend(execute_name_like(idx[0][1], value))
        elif field == 'year':
            diskloc_list.extend(execute_year_query(idx[0][0], operator, int(value)))
	
    if itr == 1 and val_1 and op_1:
        diskloc_list.extend(execute_composite(op_1,operator,val_1,int(value),idx[0][0]))

	# THE METHOD MUST RETURN A SINGLE LIST OF INDICES INTO THE DISK MAP
    return sorted(diskloc_list)
    