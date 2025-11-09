"""
HW02 — Airport Luggage Tags (Open Addressing with Delete)

Implement linear probing with EMPTY and DELETED markers.
"""

# Step 4: create unique marker objects
EMPTY = object()
DELETED = object()


def hash_basic(s):
    """Return a simple integer hash for string s."""
    return sum(ord(ch) for ch in s)


def make_table_open(m):
    """Return a table of length m filled with EMPTY markers."""
    return [EMPTY] * m


def _find_slot_for_insert(t, key):
    """Return index to insert or overwrite. May return DELETED slot. Return None if full."""
    m = len(t)
    start = hash_basic(key) % m
    first_deleted = None

    for i in range(m):
        idx = (start + i) % m
        slot = t[idx]

        if slot is EMPTY:
            # found an empty: insert here or reuse deleted
            return first_deleted if first_deleted is not None else idx

        elif slot is DELETED:
            # remember first deleted slot (but keep probing)
            if first_deleted is None:
                first_deleted = idx

        elif slot[0] == key:
            # found existing key → overwrite here
            return idx

    # table full → maybe reuse deleted slot, else fail
    return first_deleted


def _find_slot_for_search(t, key):
    """Return index where key is found, else None. DELETED does not stop search."""
    m = len(t)
    start = hash_basic(key) % m

    for i in range(m):
        idx = (start + i) % m
        slot = t[idx]

        if slot is EMPTY:
            # stop searching — key not present
            return None
        elif slot is DELETED:
            # skip over deleted slots
            continue
        elif slot[0] == key:
            return idx
    return None


def put_open(t, key, value):
    """Insert or overwrite (key, value). Return True on success, False if table is full."""
    idx = _find_slot_for_insert(t, key)
    if idx is None:
        return False
    slot = t[idx]

    if slot is EMPTY or slot is DELETED:
        t[idx] = (key, value)
    else:
        t[idx] = (key, value)  # overwrite same key
    return True


def get_open(t, key):
    """Return value for key or None if not present."""
    idx = _find_slot_for_search(t, key)
    if idx is None:
        return None
    return t[idx][1]


def delete_open(t, key):
    """Delete key if present. Return True if removed, else False."""
    idx = _find_slot_for_search(t, key)
    if idx is None:
        return False
    t[idx] = DELETED
    return True


if __name__ == "__main__":
    # Optional manual checks (not graded)
    t = make_table_open(7)
    print(put_open(t, "AX1", "Checked In"))   # True
    print(put_open(t, "BX2", "Loaded"))       # True
    print(get_open(t, "AX1"))                 # Checked In
    print(delete_open(t, "AX1"))              # True
    print(get_open(t, "AX1"))                 # None
    print(put_open(t, "CX3", "Delayed"))      # True (can reuse deleted)
    print(t)
