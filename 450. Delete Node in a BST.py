# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        
        def update_node_parent(node_parent, node, node_new):
            if node_parent and node_parent.left and node_parent.left.val == node.val:
                node_parent.left = node_new
            if node_parent and node_parent.right and node_parent.right.val == node.val:
                node_parent.right = node_new
        
        def find_right_most(node):
            if node.right:
                return find_right_most(node.right)
            return node

        def del_node(node, node_parent, key):
            node_new = node
            if node.val == key:
                # left+right, left-only
                if node.left:
                    # left subtree node replace node
                    node_new = node.left
                    update_node_parent(node_parent, node, node_new)
                    # find right-most for append node.right
                    node_rightmost = find_right_most(node.left)
                    node_rightmost.right = node.right
                    
                # right-only
                elif node.right:
                    node_new = node.right
                    update_node_parent(node_parent, node, node_new)
                # no left right
                else:
                    node_new = None
                    update_node_parent(node_parent, node, node_new)
            # node != del
            else: 
                if node.left: del_node(node.left, node, key)
                if node.right: del_node(node.right, node, key)
                
            return node_new

        if not root: return None
        return del_node(root, None, key)
        
