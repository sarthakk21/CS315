# You are allowed to import any modules whatsoever (not even numpy, sklearn etc)
# The use of file IO is forbidden. Your code should not read from or write onto files

# SUBMIT YOUR CODE AS TWO PYTHON (.PY) FILES INSIDE A ZIP ARCHIVE
# THE NAME OF THE PYTHON FILES MUST BE index.py and execute.py

# DO NOT CHANGE THE NAME OF THE METHODS my_execute BELOW
# THESE WILL BE INVOKED BY THE EVALUATION SCRIPT. CHANGING THESE NAMES WILL CAUSE EVALUATION FAILURE

# You may define any new functions, variables, classes here
# For example, functions to create indices or statistics
def execute_name_equals(trie, name):
    current = trie
    for char in name:
        if current.links[ord(char) - ord('a')] is None:
            return []
        current = current.links[ord(char) - ord('a')]
    return list(range(current.disklocstart, current.disklocstart + current.cnt))

def execute_name_like(trie, prefix):
    current = trie
    for char in prefix:
        if current.links[ord(char) - ord('a')] is None:
            return []
        current = current.links[ord(char) - ord('a')]
    return list(range(current.disklocstart, current.disklocend + 1))

def execute_year_query(year_map, operator, value, total_count):
    if operator == '=':
        if value in year_map:
            loc = year_map[value]
            return list(range(loc['disklocstart'], loc['disklocend'] + 1))
    elif operator == '>=':
        return [i for year, loc in year_map.items() if year >= value for i in range(loc['disklocstart'], loc['disklocend'] + 1)]
    elif operator == '<=':
        return [i for year, loc in year_map.items() if year <= value for i in range(loc['disklocstart'], loc['disklocend'] + 1)]
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
                diskloc_list.extend(execute_name_equals(idx['global_trie'], value, idx['disk']))
            elif operator == 'LIKE':
                # Trim the '%' from value since we are assuming predicates end with this for LIKE
                value = value[:-1]
                diskloc_list.extend(execute_name_like(idx['global_trie'], value, idx['disk']))
        elif field == 'year':
            diskloc_list.extend(execute_year_query(idx['year_map'], operator, int(value), len(idx['disk'])))
        else:
            continue  # Skip unrecognized predicates
	
	# THE METHOD MUST RETURN A SINGLE LIST OF INDICES INTO THE DISK MAP
	return list(set(diskloc_list))
    
