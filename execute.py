# You are allowed to import any modules whatsoever (not even numpy, sklearn etc)
# The use of file IO is forbidden. Your code should not read from or write onto files

# SUBMIT YOUR CODE AS TWO PYTHON (.PY) FILES INSIDE A ZIP ARCHIVE
# THE NAME OF THE PYTHON FILES MUST BE index.py and execute.py

# DO NOT CHANGE THE NAME OF THE METHODS my_execute BELOW
# THESE WILL BE INVOKED BY THE EVALUATION SCRIPT. CHANGING THESE NAMES WILL CAUSE EVALUATION FAILURE

# You may define any new functions, variables, classes here
# For example, functions to create indices or statistics

def find_year_index_left(yearly_roots, target_year):
    left, right = 0, len(yearly_roots) - 1
    result_index = -1  # Initialize to -1 to handle cases where no smaller year exists
    
    while left <= right:
        mid = (left + right) // 2
        year, _ = yearly_roots[mid]
        
        if year == target_year:
            return mid 
        elif year < target_year:
            result_index = mid  
            left = mid + 1      
        else:
            right = mid - 1 
        
    return result_index

def find_year_index_right(yearly_roots, target_year):
    left, right = 0, len(yearly_roots) - 1
    result_index = -1  # Initialize to -1 to handle cases where no smaller year exists
    
    while left <= right:
        mid = (left + right) // 2
        year, _ = yearly_roots[mid]
        
        if year == target_year:
            return mid 
        elif year < target_year:
            left = mid + 1      
        else:
            result_index = mid
            right = mid - 1 
        
    return result_index


def execute_name_equals(trie, name):
    current = trie
    for char in name:
        if current.child[ord(char) - ord('a')] is None:
            return []
        current = current.child[ord(char) - ord('a')]
    return list(range(current.start,current.end+1))

def execute_name_like(trie, prefix):
    current = trie
    for char in prefix:
        if current.child[ord(char)-ord('a')] is None:
            return []
        current = current.child[ord(char) - ord('a')]
    return list(range(current.start,current.end+1))

def execute_year_query(year_map, operator, value):
    if operator == '=':
        found_pos = find_year_index_left(year_map,value)
        if year_map[found_pos][0] == value:
            current = year_map[found_pos][1]
            return list(range(current.start,current.end+1))
    elif operator == '>=':
        found_pos = find_year_index_left(year_map,value)
        result = []
        for i in range(found_pos+1):
            current = year_map[i][1]
            result.extend(list(range(current.start,current.end+1)))
        return result
    elif operator == '<=':
        found_pos = find_year_index_right(year_map,value)
        result = []
        for i in range(found_pos,len(year_map)):
            current = year_map[i][1]
            result.extend(list(range(current.start,current.end+1)))
        return result
    return []


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

    # Process each predicate in the clause
    for predicate in clause:
        field, operator, value = predicate
        if field == 'name':
            if operator == '=':
                diskloc_list.extend(execute_name_equals(idx[0][1], value[1:-1]))
            elif operator == 'LIKE':
                # Trim the '%' from value since we are assuming predicates end with this for LIKE
                value = value[1:-2]
                diskloc_list.extend(execute_name_like(idx[0][1], value))
        elif field == 'year':
            diskloc_list.extend(execute_year_query(idx[0][0], operator, int(value)))
        else:
            continue  # Skip unrecognized predicates
	
	# THE METHOD MUST RETURN A SINGLE LIST OF INDICES INTO THE DISK MAP
    return list(set(diskloc_list))
    