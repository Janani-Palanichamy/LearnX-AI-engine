{
  "skills": [
    {
      "id": "SKL-01",
      "name": "Node Creation & Basic Attributes",
      "description": "Defining the Node class with data and next pointer attributes.",
      "prerequisites": []
    },
    {
      "id": "SKL-02",
      "name": "Traversal & Inspection",
      "description": "Iterating through the list using a temporary pointer without losing head reference.",
      "prerequisites": ["SKL-01"]
    },
    {
      "id": "SKL-03",
      "name": "Insertion at Head",
      "description": "Creating a new node, pointing its next to current head, and updating head.",
      "prerequisites": ["SKL-01"]
    },
    {
      "id": "SKL-04",
      "name": "Insertion at Tail/Middle",
      "description": "Navigating to a specific index/end and updating pointers in correct sequence.",
      "prerequisites": ["SKL-02", "SKL-03"]
    },
    {
      "id": "SKL-05",
      "name": "Deletion of Node",
      "description": "Locating target/index node, updating preceding pointers, and handling memory references.",
      "prerequisites": ["SKL-02", "SKL-04"]
    },
    {
      "id": "SKL-06",
      "name": "Null & Edge-Case Handling",
      "description": "Handling operations on empty lists (head is None) or single-node lists safely.",
      "prerequisites": ["SKL-02"]
    },
    {
      "id": "SKL-07",
      "name": "List Reversal",
      "description": "In-place reversal of pointers using prev, curr, and next tracking pointers.",
      "prerequisites": ["SKL-02", "SKL-04", "SKL-06"]
    }
  ],
  "misconceptions": [
    {
      "id": "MIS-01",
      "name": "Losing Head Pointer",
      "root_cause": "Student mutates head directly during iteration instead of using a temporary variable.",
      "deterministic_trigger": "Head reassignment during loop / head becomes None unexpectedly",
      "hints": {
        "L1": "Take a look at how you are traversing the list. Are you keeping track of where the list starts?",
        "L2": "Modifying `head` directly moves the start pointer of your list. Use a temporary pointer like `curr = head` to iterate instead.",
        "L3": "Example:\ncurr = head\nwhile curr:\n    print(curr.val)\n    curr = curr.next  # head remains untouched!",
        "L4": "curr = head\nwhile curr:\n    # Process curr.val\n    curr = ___ # Update loop variable, NOT head"
      }
    },
    {
      "id": "MIS-02",
      "name": "Missing None Check",
      "root_cause": "Accessing attributes on a pointer variable that evaluates to None.",
      "deterministic_trigger": "AttributeError: 'NoneType' object has no attribute",
      "hints": {
        "L1": "What happens if your node pointer becomes `None` before you access `.next` or `.val`?",
        "L2": "You are attempting to access properties of a node that is `None`. Always check `if node is not None:` or include `while curr:` before accessing attributes.",
        "L3": "Example:\nif curr is not None:\n    print(curr.val)",
        "L4": "while curr and ___:\n    curr = curr.next"
      }
    },
    {
      "id": "MIS-03",
      "name": "Wrong Pointer Reassignment Order",
      "root_cause": "Reassigning a node's next pointer before saving the downstream node reference, breaking the list.",
      "deterministic_trigger": "List disconnect / unreachable nodes / unexpected node loss",
      "hints": {
        "L1": "Check the sequence in which you change pointer targets. Did you lose access to any nodes downstream?",
        "L2": "If you overwrite `prev.next` before storing `curr.next`, the rest of the list becomes unreachable.",
        "L3": "Example:\ntemp = curr.next # Preserve target\nprev.next = temp # Update link safely",
        "L4": "new_node.next = ___\nprev.next = new_node"
      }
    },
    {
      "id": "MIS-04",
      "name": "Infinite Loop",
      "root_cause": "Forgetting to advance the pointer in a loop or creating circular pointer references.",
      "deterministic_trigger": "TimeoutError / Execution Limit Exceeded",
      "hints": {
        "L1": "Your loop isn't terminating. Is your pointer moving forward with each step?",
        "L2": "A `while` loop over a linked list requires advancing the current reference at the end of each iteration.",
        "L3": "Example:\nwhile curr:\n    # do work\n    curr = curr.next # Essential increment step!",
        "L4": "while curr:\n    # do work\n    ___ = curr.next"
      }
    },
    {
      "id": "MIS-05",
      "name": "Forgetting Head Update",
      "root_cause": "Performing insertion or deletion at position 0 without returning/updating the new head reference.",
      "deterministic_trigger": "Head node remains old node / modification at index 0 ignored",
      "hints": {
        "L1": "When operating on index 0, does the caller receive the updated reference to the start of the list?",
        "L2": "Modifications at the start of a list change which node is the `head`. Be sure to explicitly update or return the new head node.",
        "L3": "Example:\nif index == 0:\n    new_node.next = head\n    return new_node # New head returned",
        "L4": "if index == 0:\n    new_node.next = head\n    return ___"
      }
    },
    {
      "id": "MIS-06",
      "name": "Off-by-One in Position Search",
      "root_cause": "Looping k+1 or k-1 times, causing insertion/deletion at the wrong position index.",
      "deterministic_trigger": "Insertion or deletion at incorrect index in output list",
      "hints": {
        "L1": "Trace your counter variable manually for index = 1. Does your loop stop at the node right before the target?",
        "L2": "To insert or delete at position `k`, you must stop traversal at position `k-1` (the node before target).",
        "L3": "Example:\nfor i in range(index - 1):\n    curr = curr.next",
        "L4": "for i in range(___):\n    curr = curr.next"
      }
    },
    {
      "id": "MIS-07",
      "name": "Value vs Node Confusion",
      "root_cause": "Passing or assigning raw data types (e.g. integers) where a Node object is expected.",
      "deterministic_trigger": "AttributeError: 'int' object has no attribute 'next'",
      "hints": {
        "L1": "Are you assigning an integer value directly to a pointer reference?",
        "L2": "`next` pointers must reference `Node` objects, not primitive values like integers. Wrap raw data in `Node(val)`.",
        "L3": "Example:\n# Incorrect: curr.next = 5\n# Correct:   curr.next = Node(5)",
        "L4": "curr.next = ___(val)"
      }
    },
    {
      "id": "MIS-08",
      "name": "Single Node Edge Case Failure",
      "root_cause": "Assuming list length >= 2, causing failure when head.next is None.",
      "deterministic_trigger": "AttributeError on 1-element list inputs",
      "hints": {
        "L1": "Does your algorithm work if the list only has a single element?",
        "L2": "Operations accessing `head.next.val` fail if `head.next` is `None`. Add guard clauses for single-element lists.",
        "L3": "Example:\nif head is None or head.next is None:\n    return head",
        "L4": "if head is None or ___:\n    return head"
      }
    }
  ],
  "questions": [
    {
      "id": "Q01",
      "title": "Create a Node Class",
      "skill_id": "SKL-01",
      "difficulty": "Easy",
      "prompt": "Define a standard Node class for a singly linked list. It should initialize with attributes 'val' (defaults to 0) and 'next' (defaults to None).",
      "starter_code": "class Node:\n    def __init__(self, val=0, next=None):\n        # Write your code here\n        pass",
      "test_cases": [
        {
          "input_script": "n = Node(10); result = (n.val == 10 and n.next is None)",
          "expected_output": true
        },
        {
          "input_script": "n1 = Node(5); n2 = Node(10, n1); result = (n2.next.val == 5)",
          "expected_output": true
        },
        {
          "input_script": "n = Node(); result = (n.val == 0 and n.next is None)",
          "expected_output": true
        }
      ],
      "transfer_variant": {
        "id": "Q01-T",
        "title": "Node Class with Custom Default",
        "prompt": "Define a Node class where default value is -1 and next is None."
      }
    },
    {
      "id": "Q02",
      "title": "Count Nodes in Linked List",
      "skill_id": "SKL-02",
      "difficulty": "Easy",
      "prompt": "Write a function `count_nodes(head: Node) -> int` that counts and returns the total number of nodes in the linked list.",
      "starter_code": "def count_nodes(head):\n    # Write your solution here\n    pass",
      "test_cases": [
        {
          "input_array": [1, 2, 3, 4],
          "expected_output": 4
        },
        {
          "input_array": [10],
          "expected_output": 1
        },
        {
          "input_array": [],
          "expected_output": 0
        }
      ],
      "transfer_variant": {
        "id": "Q02-T",
        "title": "Sum All Node Values",
        "prompt": "Write a function `sum_nodes(head: Node) -> int` to calculate the total sum of all node values."
      }
    },
    {
      "id": "Q03",
      "title": "Insert at Beginning",
      "skill_id": "SKL-03",
      "difficulty": "Easy",
      "prompt": "Write a function `insert_at_head(head: Node, val: int) -> Node` that creates a new node with `val` and inserts it at the front of the list, returning the new head.",
      "starter_code": "def insert_at_head(head, val):\n    # Write your solution here\n    pass",
      "test_cases": [
        {
          "input_array": [2, 3],
          "val": 1,
          "expected_output": [1, 2, 3]
        },
        {
          "input_array": [10],
          "val": 5,
          "expected_output": [5, 10]
        },
        {
          "input_array": [],
          "val": 1,
          "expected_output": [1]
        }
      ],
      "transfer_variant": {
        "id": "Q03-T",
        "title": "Prepend Multiple Values",
        "prompt": "Write `prepend_multiple(head: Node, vals: list[int]) -> Node` to prepend a list of values in given order."
      }
    },
    {
      "id": "Q04",
      "title": "Append Node at End",
      "skill_id": "SKL-04",
      "difficulty": "Easy",
      "prompt": "Write a function `append_node(head: Node, val: int) -> Node` that appends a node with value `val` to the end of the list and returns the head.",
      "starter_code": "def append_node(head, val):\n    # Write your solution here\n    pass",
      "test_cases": [
        {
          "input_array": [1, 2],
          "val": 3,
          "expected_output": [1, 2, 3]
        },
        {
          "input_array": [5],
          "val": 10,
          "expected_output": [5, 10]
        },
        {
          "input_array": [],
          "val": 1,
          "expected_output": [1]
        }
      ],
      "transfer_variant": {
        "id": "Q04-T",
        "title": "Append Unique Value",
        "prompt": "Write `append_if_absent(head: Node, val: int) -> Node` to append `val` only if it isn't already present."
      }
    },
    {
      "id": "Q05",
      "title": "Insert at Specific Index",
      "skill_id": "SKL-04",
      "difficulty": "Medium",
      "prompt": "Write `insert_at_index(head: Node, val: int, index: int) -> Node` to insert a new node containing `val` at 0-based position `index`.",
      "starter_code": "def insert_at_index(head, val, index):\n    # Write your solution here\n    pass",
      "test_cases": [
        {
          "input_array": [1, 3, 4],
          "val": 2,
          "index": 1,
          "expected_output": [1, 2, 3, 4]
        },
        {
          "input_array": [1, 2],
          "val": 3,
          "index": 2,
          "expected_output": [1, 2, 3]
        },
        {
          "input_array": [2],
          "val": 1,
          "index": 0,
          "expected_output": [1, 2]
        },
        {
          "input_array": [],
          "val": 5,
          "index": 0,
          "expected_output": [5]
        }
      ],
      "transfer_variant": {
        "id": "Q05-T",
        "title": "Insert After Value",
        "prompt": "Write `insert_after_value(head: Node, target: int, val: int) -> Node` to insert node `val` after node with value `target`."
      }
    },
    {
      "id": "Q06",
      "title": "Delete Head Node",
      "skill_id": "SKL-05",
      "difficulty": "Easy",
      "prompt": "Write `delete_head(head: Node) -> Node` to remove the front element and return the new head.",
      "starter_code": "def delete_head(head):\n    # Write your solution here\n    pass",
      "test_cases": [
        {
          "input_array": [1, 2, 3],
          "expected_output": [2, 3]
        },
        {
          "input_array": [10],
          "expected_output": []
        },
        {
          "input_array": [],
          "expected_output": []
        }
      ],
      "transfer_variant": {
        "id": "Q06-T",
        "title": "Delete Tail Node",
        "prompt": "Write `delete_tail(head: Node) -> Node` to remove the last node of the list."
      }
    },
    {
      "id": "Q07",
      "title": "Delete Node by Value",
      "skill_id": "SKL-05",
      "difficulty": "Medium",
      "prompt": "Write `delete_by_val(head: Node, target: int) -> Node` to remove the first node whose `val == target`.",
      "starter_code": "def delete_by_val(head, target):\n    # Write your solution here\n    pass",
      "test_cases": [
        {
          "input_array": [1, 2, 3, 4],
          "target": 3,
          "expected_output": [1, 2, 4]
        },
        {
          "input_array": [1, 2],
          "target": 1,
          "expected_output": [2]
        },
        {
          "input_array": [1, 2],
          "target": 5,
          "expected_output": [1, 2]
        },
        {
          "input_array": [],
          "target": 1,
          "expected_output": []
        }
      ],
      "transfer_variant": {
        "id": "Q07-T",
        "title": "Delete All Occurrences",
        "prompt": "Write `delete_all_occurrences(head: Node, target: int) -> Node` to remove all nodes with matching values."
      }
    },
    {
      "id": "Q08",
      "title": "Find Middle Node",
      "skill_id": "SKL-02",
      "difficulty": "Medium",
      "prompt": "Write `find_middle(head: Node) -> Node` using slow/fast pointers. If list length is even, return second middle node.",
      "starter_code": "def find_middle(head):\n    # Write your solution here\n    pass",
      "test_cases": [
        {
          "input_array": [1, 2, 3, 4, 5],
          "expected_output_val": 3
        },
        {
          "input_array": [1, 2, 3, 4, 5, 6],
          "expected_output_val": 4
        },
        {
          "input_array": [1],
          "expected_output_val": 1
        },
        {
          "input_array": [],
          "expected_output_val": null
        }
      ],
      "transfer_variant": {
        "id": "Q08-T",
        "title": "Find K-th Node From End",
        "prompt": "Write `find_kth_from_end(head: Node, k: int) -> Node` to find node k positions from tail."
      }
    },
    {
      "id": "Q09",
      "title": "Detect Cycle in List",
      "skill_id": "SKL-06",
      "difficulty": "Medium",
      "prompt": "Write `has_cycle(head: Node) -> bool` using Floyd's algorithm to determine if the list contains a loop.",
      "starter_code": "def has_cycle(head):\n    # Write your solution here\n    pass",
      "test_cases": [
        {
          "input_array": [1, 2, 3],
          "cycle_pos": 1,
          "expected_output": true
        },
        {
          "input_array": [1, 2, 3],
          "cycle_pos": -1,
          "expected_output": false
        },
        {
          "input_array": [],
          "cycle_pos": -1,
          "expected_output": false
        }
      ],
      "transfer_variant": {
        "id": "Q09-T",
        "title": "Detect Cycle Entry Node",
        "prompt": "Write `detect_cycle_start(head: Node) -> Node` to return the node reference where the cycle begins."
      }
    },
    {
      "id": "Q10",
      "title": "Reverse Linked List",
      "skill_id": "SKL-07",
      "difficulty": "Medium",
      "prompt": "Write `reverse_list(head: Node) -> Node` to reverse a singly linked list in-place and return the new head node.",
      "starter_code": "def reverse_list(head):\n    # Write your solution here\n    pass",
      "test_cases": [
        {
          "input_array": [1, 2, 3, 4],
          "expected_output": [4, 3, 2, 1]
        },
        {
          "input_array": [1, 2],
          "expected_output": [2, 1]
        },
        {
          "input_array": [1],
          "expected_output": [1]
        },
        {
          "input_array": [],
          "expected_output": []
        }
      ],
      "transfer_variant": {
        "id": "Q10-T",
        "title": "Reverse Range Sublist",
        "prompt": "Write `reverse_sublist(head: Node, left: int, right: int) -> Node` to reverse nodes between positions left and right."
      }
    },
    {
      "id": "Q11",
      "title": "Remove Duplicates from Sorted List",
      "skill_id": "SKL-05",
      "difficulty": "Medium",
      "prompt": "Write `delete_duplicates(head: Node) -> Node` to remove all duplicate values from a sorted linked list.",
      "starter_code": "def delete_duplicates(head):\n    # Write your solution here\n    pass",
      "test_cases": [
        {
          "input_array": [1, 1, 2, 3, 3],
          "expected_output": [1, 2, 3]
        },
        {
          "input_array": [1, 1, 1],
          "expected_output": [1]
        },
        {
          "input_array": [1, 2, 3],
          "expected_output": [1, 2, 3]
        },
        {
          "input_array": [],
          "expected_output": []
        }
      ],
      "transfer_variant": {
        "id": "Q11-T",
        "title": "Remove All Duplicated Elements",
        "prompt": "Write `delete_all_duplicate_nodes(head: Node) -> Node` to remove all nodes that have duplicate numbers entirely."
      }
    },
    {
      "id": "Q12",
      "title": "Merge Two Sorted Lists",
      "skill_id": "SKL-04",
      "difficulty": "Hard",
      "prompt": "Write `merge_two_lists(l1: Node, l2: Node) -> Node` to merge two sorted linked lists into one single sorted list.",
      "starter_code": "def merge_two_lists(l1, l2):\n    # Write your solution here\n    pass",
      "test_cases": [
        {
          "input_array_1": [1, 2, 4],
          "input_array_2": [1, 3, 4],
          "expected_output": [1, 1, 2, 3, 4, 4]
        },
        {
          "input_array_1": [5],
          "input_array_2": [1, 2],
          "expected_output": [1, 2, 5]
        },
        {
          "input_array_1": [],
          "input_array_2": [1, 2],
          "expected_output": [1, 2]
        },
        {
          "input_array_1": [],
          "input_array_2": [],
          "expected_output": []
        }
      ],
      "transfer_variant": {
        "id": "Q12-T",
        "title": "Merge K Sorted Lists",
        "prompt": "Write `merge_k_sorted_lists(lists: list[Node]) -> Node` to merge K sorted linked lists."
      }
    }
  ]
}