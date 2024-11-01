# You are allowed to import any modules whatsoever (not even numpy, sklearn etc)
# The use of file IO is forbidden. Your code should not read from or write onto files

# SUBMIT YOUR CODE AS TWO PYTHON (.PY) FILES INSIDE A ZIP ARCHIVE
# THE NAME OF THE PYTHON FILES MUST BE index.py and execute.py

# DO NOT CHANGE THE NAME OF THE METHODS my_index BELOW
# THESE WILL BE INVOKED BY THE EVALUATION SCRIPT. CHANGING THESE NAMES WILL CAUSE EVALUATION FAILURE

# You may define any new functions, variables, classes here
# For example, functions to create indices or statistics

class TrieNode:
    def __init__(self, start_pos):
        self.child = [None] * 26  # Initialize array for 26 lowercase English letters
        self.wordEnd = False       # Mark if the node corresponds to the end of a word
        self.start = start_pos     # Start index of the word in sorted list
        self.end = start_pos       # End index of the word in sorted list
        self.count = 0

def insert_key(root, key, pos):
    """Inserts a key into the Trie with its starting position."""
    curr = root
    for c in key:
        index = ord(c) - ord('a')  # Calculate the index for the character
        if curr.child[index] is None:
            curr.child[index] = TrieNode(pos)  # Create new node if needed
            curr = curr.child[index]
        else:
            curr = curr.child[index]
            curr.end = pos  # Update the end position for existing node
    curr.count += 1
    curr.wordEnd = True

def my_index(tuples):
    """Creates indices and statistics from the input list of tuples."""
    ids, names, years = zip(*tuples)

    # Sorting tuples by year (primary) and name (secondary)
    sorted_by_years = sorted(zip(years, names, ids))
    years_sorted = [year for year, _, _ in sorted_by_years]
    names_sorted_by_year = [name for _, name, _ in sorted_by_years]
    disk_by_years = [id_ for _, _, id_ in sorted_by_years]

    # Sorting tuples by name (primary) and id (secondary)
    sorted_by_names = sorted(zip(names, ids))
    names_sorted = [name for name, _ in sorted_by_names]
    disk_by_names = [id_ for _, id_ in sorted_by_names]

    # Combined disk map
    disk = disk_by_years + disk_by_names
    n = len(disk_by_years)

    # Initializing the Trie with names sorted by name and ids
    root = TrieNode(-1)
    for i in range(n):
        insert_key(root, names_sorted[i], n + i)

    # Building yearly Tries
    current_year = years_sorted[0]
    yearly_root = TrieNode(0)
    insert_key(yearly_root, names_sorted_by_year[0], 0)
    yearly_roots = []

    for i in range(1, n):
        if years_sorted[i] == current_year:
            insert_key(yearly_root, names_sorted_by_year[i], i)
        else:
            yearly_root.end = i-1
            yearly_roots.append((current_year, yearly_root))

            # Update for the next year
            current_year = years_sorted[i]
            yearly_root = TrieNode(i)
            insert_key(yearly_root, names_sorted_by_year[i], i)

    yearly_root.end = n-1
    yearly_roots.append((current_year, yearly_root))

    # Packing index and statistics
    my_index = [yearly_roots, root]
    my_stats = {
        "count": len(years),
        "min": min(years),
        "max": max(years)
    }

    # Return the combined disk map and the index-statistics package
    idx_stat = [my_index, my_stats]
    return disk, idx_stat
