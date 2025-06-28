"""
modify problem to
```
getMaxKey() Returns latest updated keys with the maximal count. If no element exists, return an empty string "".
getMinKey() Returns latest updated keys with the minimum count. If no element exists, return an empty string "".
```
"""
class Node:
    def __init__(self, count, keys: list):
        self.next = None
        self.prev = None
        self.count = count
        self.keys: list = keys

class AllOne:

    def __init__(self):
        self.first = Node(0, []) # dummy
        self.last = Node(0, []) # dummy
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
        node_new = self.cnt_node.get(cnt_new)
        # if new node's not exists, add node
        if not node_new:
            node_new = self._add_node(node_prev, cnt_new)
        node_new.keys.append(key)
        
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
            node_new.keys.append(key)

    def getMaxKey(self) -> str:
        if self.first.next == self.last:
            return ""
        return self.last.prev.keys[-1]

    def getMinKey(self) -> str:
        if self.first.next == self.last:
            return ""
        return self.first.next.keys[-1]
    
    def _remove_key_from_node(self, key, node_org, cnt_org):
        # if not key count not latest status, remove
        while node_org.keys and self.key_cnt.get(node_org.keys[-1], -1) != cnt_org:
            node_org.keys.pop()
        # if org node's key is empty, remove node
        if len(node_org.keys) == 0:
            node_org.prev.next = node_org.next
            node_org.next.prev = node_org.prev
            del self.cnt_node[cnt_org]
            return True
        return False
    
    def _add_node(self, node_prev, cnt_new):
        node_new = Node(cnt_new, [])
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

# Case 1: inc 兩個 key, 後加者為最新
obj = AllOne()
obj.inc("a")      # a:1 (latest)
obj.inc("b")      # b:1 (latest)
assert obj.getMaxKey() == "b"
assert obj.getMinKey() == "b"

# Case 2: 先加再升級某一 key，最新升級者為 max
obj = AllOne()
obj.inc("x")      # x:1 (latest)
obj.inc("y")      # y:1 (latest)
obj.inc("x")      # x:2 (latest)
assert obj.getMaxKey() == "x"  # x:2 > y:1, x為最新
assert obj.getMinKey() == "y"  # y:1, y為最新操作到min count

# Case 3: dec 讓某 key 變 min，測試最新更新
obj = AllOne()
obj.inc("a")
obj.inc("b")
obj.inc("a")
obj.dec("a")      # a:1, b:1 (a 為最新)
assert obj.getMaxKey() == "a"  # a,b:1, 但a為最新
assert obj.getMinKey() == "a"

# Case 4: 只剩一個 key，刪除後查詢
obj = AllOne()
obj.inc("foo")
obj.dec("foo")
assert obj.getMaxKey() == ""
assert obj.getMinKey() == ""

# Case 5: 反覆操作，最新操作 key 應回傳
obj = AllOne()
obj.inc("x")
obj.inc("y")
obj.inc("z")
obj.inc("x")      # x:2, y:1, z:1 (x latest)
obj.dec("z")      # x:2, y:1, z removed (z latest op)
obj.dec("x")      # x:1, y:1 (x latest)
assert obj.getMaxKey() == "x"
assert obj.getMinKey() == "x"
