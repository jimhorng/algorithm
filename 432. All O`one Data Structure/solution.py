from typing import Set


class Node:
    def __init__(self, count, keys: Set):
        self.next = None
        self.prev = None
        self.count = count
        self.keys: Set = keys


class AllOne:

    def __init__(self):
        self.first = Node(0, set())  # dummy
        self.last = Node(0, set())  # dummy
        self.first.next = self.last
        self.last.prev = self.first
        self.key_cnt = {}
        self.cnt_node = {}

    def inc(self, key: str) -> None:
        old_count = self.key_cnt.get(key, 0)
        new_count = old_count + 1
        self.key_cnt[key] = new_count

        old_node = self.cnt_node.get(old_count)
        insert_after = old_node if old_node else self.first

        self._move_key_to_count(key, new_count, insert_after)

        if old_node:
            self.remove_key_from_node(key, old_node, old_count)

    def dec(self, key: str) -> None:
        old_count = self.key_cnt[key]
        new_count = old_count - 1
        old_node = self.cnt_node[old_count]

        self._update_key_count(key, new_count)

        if new_count > 0:
            self._move_key_to_count(key, new_count, old_node.prev)

        self.remove_key_from_node(key, old_node, old_count)

    def getMaxKey(self) -> str:
        return self._get_key_from_node(self.last.prev)

    def getMinKey(self) -> str:
        return self._get_key_from_node(self.first.next)

    def _move_key_to_count(self, key: str, count: int, insert_after: Node) -> None:
        """Add key to node with given count, creating node if necessary."""
        node = self.cnt_node.get(count)
        if not node:
            node = Node(count, set())
            # Insert new_node after insert_after in the linked list
            next_node = insert_after.next
            insert_after.next = node
            next_node.prev = node
            node.prev = insert_after
            node.next = next_node
            self.cnt_node[count] = node
        node.keys.add(key)

    def _update_key_count(self, key: str, new_count: int) -> None:
        """Update or remove key count in tracking dictionary."""
        if new_count == 0:
            del self.key_cnt[key]
        else:
            self.key_cnt[key] = new_count

    def _get_key_from_node(self, node: Node) -> str:
        """Get any key from node, or empty string if node is dummy."""
        if node == self.first or node == self.last:
            return ""
        return next(iter(node.keys))

    def remove_key_from_node(self, key, node, cnt):
        node.keys.remove(key)
        if not node.keys:
            # Remove node from linked list and tracking dictionary
            node.prev.next = node.next
            node.next.prev = node.prev
            del self.cnt_node[cnt]
            return True
        return False


# Your AllOne object will be instantiated and called as such:
# obj = AllOne()
# obj.inc(key)
# obj.dec(key)
# param_3 = obj.getMaxKey()
# param_4 = obj.getMinKey()
