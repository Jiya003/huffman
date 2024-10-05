from flask import Flask, render_template, request, jsonify
from collections import Counter
import heapq

app = Flask(__name__)

class Node:
    def __init__(self, freq, symbol=None):
        self.freq = freq
        self.symbol = symbol
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def huffman_coding(text):
    if not text:
        return {}

    # Count frequency of each character
    frequency = Counter(text)
    
    # Create a priority queue (min-heap)
    heap = [Node(freq, char) for char, freq in frequency.items()]
    heapq.heapify(heap)

    # Build the Huffman tree
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    root = heap[0]
    codes = {}
    _generate_codes(root, "", codes)
    return codes, frequency, root

def _generate_codes(node, current_code, codes):
    if node:
        if node.symbol is not None:
            codes[node.symbol] = current_code
        _generate_codes(node.left, current_code + "0", codes)
        _generate_codes(node.right, current_code + "1", codes)

def build_tree_structure(node, prefix="", is_left=True):
    if node is None:
        return ""
    
    tree_str = prefix + ("|-- " if is_left else "|-- ") + f"{node.freq}\n"
    
    # If the node has a symbol, show it as well
    if node.symbol is not None:
        tree_str += prefix + ("|   " if is_left else "    ") + f"{node.symbol}({node.freq})\n"
    
    # Prepare the new prefix for the next level
    new_prefix = prefix + ("|   " if is_left else "    ")
    
    # Recursively build the left and right subtrees
    tree_str += build_tree_structure(node.left, new_prefix, True)
    tree_str += build_tree_structure(node.right, new_prefix, False)

    return tree_str


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/build_tree', methods=['POST'])
def build_huffman_tree():
    data = request.json
    text = data['text']
    codes, frequency, root = huffman_coding(text)

    # Get the visual representation of the tree
    tree_structure = build_tree_structure(root)

    # Prepare the response
    huffman_codes = [{"symbol": char, "code": code, "freq": frequency[char]} for char, code in codes.items()]
    return jsonify(huffman_codes=huffman_codes, tree_structure=tree_structure)

if __name__ == '__main__':
    app.run(debug=True)
