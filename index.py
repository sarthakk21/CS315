# You are allowed to import any modules whatsoever (not even numpy, sklearn etc)
# The use of file IO is forbidden. Your code should not read from or write onto files

# SUBMIT YOUR CODE AS TWO PYTHON (.PY) FILES INSIDE A ZIP ARCHIVE
# THE NAME OF THE PYTHON FILES MUST BE index.py and execute.py

# DO NOT CHANGE THE NAME OF THE METHODS my_index BELOW
# THESE WILL BE INVOKED BY THE EVALUATION SCRIPT. CHANGING THESE NAMES WILL CAUSE EVALUATION FAILURE

# You may define any new functions, variables, classes here
# For example, functions to create indices or statistics
class TrieNode:
    def __init__(self):
        self.links = [None] * 26
        self.disklocstart = -1
        self.disklocend = -1
        self.cnt = 0

def insert_data_in_trie(root, data, offset):
    for index, item in enumerate(data):
        current = root
        for char in item[1]:
            if current.links[ord(char) - ord('a')] is None:
                current.links[ord(char) - ord('a')] = TrieNode()
            current = current.links[ord(char) - ord('a')]
        if current.disklocstart == -1:
            current.disklocstart = offset + index
        current.disklocend = offset + index
        current.cnt += 1




################################
# Non Editable Region Starting #
################################
def my_index( tuples ):
################################
#  Non Editable Region Ending  #
################################

	# Use this method to create indices and statistics
	# Each tuple has 3 values -- the id, name and year
    # Sorting alumni data for disk storage as required
    sorted_by_year_name = sorted(tuples, key=lambda x: (x[2], x[1]))
    sorted_by_name = sorted(tuples, key=lambda x: x[1])

    # Disk layout
    disk = [item[0] for item in sorted_by_year_name] + [item[0] for item in sorted_by_name]
    
    # Building global trie for name queries
    global_trie = TrieNode()
    insert_data_in_trie(global_trie, sorted_by_name, len(sorted_by_year_name))
    
    # Year to disk location mapping and year-specific tries
    year_map = {}
    year_tries = {}
    for idx, item in enumerate(sorted_by_year_name):
        year = item[2]
        if year not in year_map:
            year_map[year] = {'disklocstart': idx, 'disklocend': idx}
            year_tries[year] = TrieNode()
        else:
            year_map[year]['disklocend'] = idx
        
        # Insert into year-specific trie
        insert_data_in_trie(year_tries[year], [item], 0)
    
    # idx_stat setup
    idx_stat = {
        'global_trie': global_trie,
        'year_map': year_map,
        'year_tries': year_tries,
        'min_year': min(year_map.keys(), default=None),
        'max_year': max(year_map.keys(), default=None)
    }
	
	# THE METHOD SHOULD RETURN A DISK MAP AND A VARIABLE PACKAGING INDICES AND STATS
    
	return disk, idx_stat