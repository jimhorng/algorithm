class Node:
    def __init__(self, count, keys: Set):
        self.next = None
        self.prev = None
        self.count = count
        self.keys: Set = keys

class AllOne:

    def __init__(self):
        self.first = Node(0, set()) # dummy
        self.last = Node(0, set()) # dummy
        self.first.next = self.last
        self.last.prev = self.first
        self.key_cnt = {}
        self.cnt_node = {}

    def inc(self, key: str) -> None:
        cnt_org = self.key_cnt.get(key, 0)
        cnt_new = cnt_org + 1
        self.key_cnt[key] = cnt_new
        node_org = self.cnt_node.get(cnt_org)
        node_prev = node_org
        # if new key, org node not exist
        if not node_org:
            node_prev = self.first
        else:
            if self._remove_key_from_node(key, node_org, cnt_org):
                node_prev = node_org.prev
            # print_nodes_line(self.first)
        node_new = self.cnt_node.get(cnt_new)
        # if new node's not exists, add node
        if not node_new:
            node_new = self._add_node(node_prev, cnt_new)
        node_new.keys.add(key)
        # print(key)
        # print_nodes_line(self.first)
        
    def dec(self, key: str) -> None:
        cnt_org = self.key_cnt.get(key, 0)
        cnt_new = cnt_org - 1
        self.key_cnt[key] = cnt_new
        if self.key_cnt[key] == 0:
            del self.key_cnt[key]
        node_org = self.cnt_node.get(cnt_org)
        node_next = node_org
        if self._remove_key_from_node(key, node_org, cnt_org):
            node_next = node_org.next
        # if new count is 0, skip
        if cnt_new != 0:
            node_new = self.cnt_node.get(cnt_new)
            # if new node's not exists, add node
            if not node_new:
                node_new = self._add_node(node_next.prev, cnt_new)
            node_new.keys.add(key)
        # print(key)
        # print_nodes_line(self.first)

    def getMaxKey(self) -> str:
        if self.first.next == self.last:
            return ""
        return next(iter(self.last.prev.keys))

    def getMinKey(self) -> str:
        if self.first.next == self.last:
            return ""
        return next(iter(self.first.next.keys))
    
    def _remove_key_from_node(self, key, node_org, cnt_org):
        node_org.keys.remove(key)
        # if org node's key is empty, remove node
        if len(node_org.keys) == 0:
            node_org.prev.next = node_org.next
            node_org.next.prev = node_org.prev
            del self.cnt_node[cnt_org]
            return True
        return False
    
    def _add_node(self, node_prev, cnt_new):
        node_new = Node(cnt_new, set())
        node_next = node_prev.next
        node_prev.next = node_new
        node_next.prev = node_new
        node_new.prev = node_prev
        node_new.next = node_next
        self.cnt_node[cnt_new] = node_new
        return node_new


# Your AllOne object will be instantiated and called as such:
# obj = AllOne()
# obj.inc(key)
# obj.dec(key)
# param_3 = obj.getMaxKey()
# param_4 = obj.getMinKey()
