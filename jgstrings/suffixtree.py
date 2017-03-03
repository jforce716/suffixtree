import logging
import collections
import itertools

logger = logging.getLogger(__name__)

def getpath(node):
    path = []
    while node:
        path.insert(0, node.label())
        node = node.parent

    return path


class Endtag:
    __slots__ = ["__tag"]

    def __init__(self, tag):
        self.__tag = tag

    @property
    def tag(self):
        return self.__tag

    def __eq__(self, other):
        if isinstance(other, Endtag):
            return self.tag == other.tag
        else:
            return False

    def __hash__(self):
        return hash(self.tag)
    
class InternalNode:
    __slots__ = ["basestr", "start", "end", "parent",
                 "childmap", "suffixlink"]

    def __init__(self, basestr=None, start=0, end=0, parent=None):
        if parent and not basestr:
            raise ValueError("Base string is need for non-root node")
        
        self.basestr = basestr
        self.start = start
        self.end = end
        self.childmap = {}
        self.parent = parent
        self.suffixlink = None

    def __str__(self):
        return "InternalNode@{:x}({}, {}){}".format(id(self), self.start,
                                             self.end, self.label())
                                                
    def __getitem__(self, index):
        if index < 0 or index >= len(self):
            raise IndexError("Index out of range: {}".format(index))

        return self.basestr[self.start + index]
    
    def __len__(self):
        return self.end - self.start

    def is_leaf(self):
        return False
        
    def is_root(self):
        return self.parent is None
    
    def label(self):
        return "" if self.is_root() else self.basestr[self.start:self.end]

    def child(self, key):
        return self.childmap[key] if key in self.childmap else None

class Leaf:
    __slots__ = ["basestr", "start", "parent", "suffixid"]

    def __init__(self, basestr, start, parent, suffixid):
        if not basestr:
            raise ValueError("Empty base string")
        if parent is None:
            raise ValueError("Empty parent node")
        
        self.basestr = basestr
        self.start = start
        self.parent = parent
        self.suffixid = suffixid

    @property
    def end(self):
        return len(self.basestr) + 1

    def __str__(self):
        return "LeafNode@{:x}({})".format(id(self), self.suffixid)
        
    def __getitem__(self, index):
        if len(self.basestr) == (self.start + index):
            return Endtag(id(self.basestr))
        else:
            return self.basestr[self.start + index]

    def __len__(self):
        return len(self.basestr) - self.start + 1

    def is_leaf(self):
        return True
    
    def is_root(self):
        return False

    def label(self):
        return self.basestr[self.start:]

    def suffix(self):
        return self.basestr[self.suffixid:]

    def child(self, key):
        return None


def collect_suffixes(node, suffix_list):
    if node.is_leaf():
        suffix_list.append((node.basestr, node.suffixid))
    else:
        for cnode in node.childmap.values():
            collect_suffixes(cnode, suffix_list)


LocationTag = collections.namedtuple('LocTag', 'node key index')

     
class Anchor:
    __slots__ = ["node", "key", "index"]
    
    def __init__(self, node):
        self.node = node
        self.key = None
        self.index = 0

    def __str__(self):
        return "Anchor(node = {}, key = {}, index = {}".format(self.node,
                                                               self.key,
                                                               self.index)
    
    def match(self, item):
        retval = False
        
        if self.index == 0:
            if self.node.child(item):
                self.key = item
                self.index += 1
                retval = True
        else:
            child = self.child()
            if child[self.index] == item:
                self.index += 1
                retval = True
            
        if retval and self.index >= len(self.child()):
            self.node = self.node.child(self.key)
            self.key = None
            self.index = 0

        return retval
    
    def reset(self):
        while self.node.parent is not None:
            self.node = self.node.parent
        self.index = 0
        self.key = None
        
    def get_suffixes(self, suffix_list=None):
        if suffix_list is None:
            suffix_list = []

        if self.key:
            collect_suffixes(self.child(), suffix_list)
        else:
            collect_suffixes(self.node, suffix_list)
        return suffix_list

    def child(self):
        return self.node.child(self.key) if self.key else None

    def tag(self):
        return LocationTag(node=self.node, key=self.key, index=self.index)

    def moveup(self):
        n = self.child()
        idx = 0
        if self.node.is_root():
            if self.index > 0:
                self.key = self.child()[1] if len(self.child()) > 1 else None
                self.index -= 1
                idx += 1
        else:
            self.node = self.node.suffixlink

        while self.index > 0 and self.index >= len(self.child()):
            self.node = self.child()
            self.index -= len(self.node)
            idx += len(self.node)
            if self.index == 0:
                self.key = None
            else:
                self.key = n[idx] if idx < len(n) else n.basestr[n.start + idx]

    
class TreeBuildingContext(Anchor):
    __slots__ = ["basestr", "currentlen", "nleaves"]
    
    def __init__(self, node, basestr):
        Anchor.__init__(self, node)
        self.basestr = basestr
        self.currentlen = 0
        self.nleaves = 0
    
    def __str__(self):
        fmt = "TreeBuildingContext({}, {}, index:{}, len:{}, nleaves:{}"
        return fmt.format(self.node, self.key, self.index,
                          self.currentlen, self.nleaves)
            
    
class SuffixTree:
    __slots__ = ["root"]

    def __init__(self, *strs):
        self.root = InternalNode()
        if not strs:
            return
        
        for s in strs:
            self.add_to_tree(s)
    
    def start_traverse(self):
        return Anchor(self.root)
        
    def add_to_tree(self, s):
        if not s or len(s) == 0:
            return

        ctx = TreeBuildingContext(self.root, s)        
        #build implicit suffix tree
        for item in s:
            self.extend(ctx, item)
            
        #add endtag to make it true suffix tree
        self.extend(ctx)
    
    def extend(self, ctx, item=None):
        #item is None, add end tag to finish suffix tree construction
        if not item:
            item = Endtag(id(ctx.basestr))
        
        ctx.currentlen += 1
        pnode = None
        cnode = ctx.node
        while (ctx.nleaves < ctx.currentlen and 
               ctx.nleaves < len(ctx.basestr)):
            #if matched then current phrase is done
            if ctx.match(item):
                break
            
            cnode = self.insert_node(ctx, item)
            ctx.nleaves += 1
            ctx.moveup()
            
            if pnode is not None:
                pnode.suffixlink = cnode
                
            if not cnode.is_root() and cnode.suffixlink is None:
                pnode = cnode
                cnode = ctx.node
            else:
                pnode = None
    
        if pnode is not None:
            pnode.suffixlink = cnode
            
    def insert_node(self, ctx, item):
        internalnode = ctx.node
        if ctx.index > 0:
            echild = ctx.child()
            splitpoint = echild.start + ctx.index
            internalnode = InternalNode(echild.basestr, echild.start,
                                        splitpoint, ctx.node)
            ctx.node.childmap[ctx.key] = internalnode
            echild.start = splitpoint
            echild.parent = internalnode
            internalnode.childmap[echild[0]] = echild
        leaf = Leaf(ctx.basestr, ctx.currentlen - 1,
                    internalnode, ctx.nleaves)
        internalnode.childmap[item] = leaf

        return internalnode
            

