import os

base_dir = r"d:\work\python-all\Python-DSA-AI-Master\10-Project-Based-Learning"

projects = {
    "01-Basic-Projects": [
        "01-calculator-advanced",
        "02-file-manager",
        "03-sorting-visualizer",
        "04-ds-library",
        "05-basic-game"
    ],
    "02-Intermediate-Projects": [
        "01-compression-algo",
        "02-simple-db",
        "03-web-server",
        "04-compiler-lexer",
        "05-data-viz-tool"
    ],
    "03-Advanced-Projects": [
        "01-rag-system",
        "02-ml-framework",
        "03-genai-chatbot",
        "04-high-perf-ds",
        "05-trading-bot"
    ]
}

content_templates = {
    "01-Basic-Projects/01-calculator-advanced": {
        "readme": "# Advanced Calculator\n\n## Project Specification\nBuild a CLI-based calculator capable of handling advanced mathematical operations (trigonometry, logarithms, exponentiation) and parsing complex expressions with parentheses.\n\n## Implementation Steps\n1. Define supported operations.\n2. Implement a tokenizer to parse expressions.\n3. Implement the Shunting Yard algorithm to convert infix to postfix notation.\n4. Evaluate the postfix expression.\n\n## Structure\n- `main.py`: Entry point and expression evaluation logic.\n",
        "code": "import math\n\ndef evaluate_expression(expr):\n    # Basic evaluation using eval for demonstration purposes\n    try:\n        return eval(expr, {\"math\": math})\n    except Exception as e:\n        return str(e)\n\nif __name__ == '__main__':\n    print(\"Advanced Calculator (type 'exit' to quit)\")\n    while True:\n        user_input = input(\"Enter expression: \")\n        if user_input.lower() == 'exit':\n            break\n        print(\"Result:\", evaluate_expression(user_input))\n"
    },
    "01-Basic-Projects/02-file-manager": {
        "readme": "# CLI File Manager\n\n## Project Specification\nA command-line utility to perform basic file operations: list, copy, move, delete, and search files within directories.\n\n## Implementation Steps\n1. Use `argparse` to handle CLI arguments.\n2. Implement `list_files(directory)` using `os.listdir`.\n3. Implement `copy_file(src, dst)` using `shutil.copy`.\n4. Implement directory traversal for search functionality.\n\n## Structure\n- `main.py`: Main script to handle arguments and file operations.\n",
        "code": "import os\nimport shutil\nimport argparse\n\ndef list_directory(path):\n    for item in os.listdir(path):\n        print(item)\n\nif __name__ == '__main__':\n    parser = argparse.ArgumentParser(description='Simple File Manager')\n    parser.add_argument('path', type=str, help='Path to list directory contents')\n    args = parser.parse_args()\n    list_directory(args.path)\n"
    },
    "01-Basic-Projects/03-sorting-visualizer": {
        "readme": "# Sorting Visualizer\n\n## Project Specification\nA terminal-based or simple GUI tool to visualize sorting algorithms like Bubble Sort, Merge Sort, and Quick Sort step-by-step.\n\n## Implementation Steps\n1. Setup an array of random numbers.\n2. Implement sorting algorithms using generators to yield states.\n3. Use `matplotlib` or a terminal library to redraw the array state on each yield.\n\n## Structure\n- `main.py`: Entry point for visualization.\n",
        "code": "import random\nimport time\n\ndef bubble_sort_visualizer(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n            print(f\"\\r{arr}\", end='')\n            time.sleep(0.1)\n\nif __name__ == '__main__':\n    arr = [random.randint(1, 100) for _ in range(10)]\n    print(\"Starting Sort:\", arr)\n    bubble_sort_visualizer(arr)\n    print(\"\\nSorted:\", arr)\n"
    },
    "01-Basic-Projects/04-ds-library": {
        "readme": "# Custom Data Structures Library\n\n## Project Specification\nImplement standard data structures from scratch in Python: Linked Lists, Stacks, Queues, Binary Trees, and Graphs.\n\n## Implementation Steps\n1. Create a `LinkedList` class with insert/delete/traverse.\n2. Create `Stack` and `Queue` using arrays or Linked Lists.\n3. Implement a `BinarySearchTree`.\n4. Write tests for each structure.\n\n## Structure\n- `main.py`: Demonstrations of data structures.\n",
        "code": "class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n    \n    def append(self, data):\n        if not self.head:\n            self.head = Node(data)\n            return\n        curr = self.head\n        while curr.next:\n            curr = curr.next\n        curr.next = Node(data)\n    \n    def display(self):\n        curr = self.head\n        while curr:\n            print(curr.data, end=' -> ')\n            curr = curr.next\n        print('None')\n\nif __name__ == '__main__':\n    ll = LinkedList()\n    ll.append(1)\n    ll.append(2)\n    ll.append(3)\n    ll.display()\n"
    },
    "01-Basic-Projects/05-basic-game": {
        "readme": "# Text-based Adventure Game\n\n## Project Specification\nA simple text-based RPG where the player navigates rooms, collects items, and fights basic enemies.\n\n## Implementation Steps\n1. Define a `Room` class with descriptions and exits.\n2. Define a `Player` class to track inventory and health.\n3. Implement the game loop: prompt input -> parse action -> update state -> render.\n\n## Structure\n- `main.py`: Game loop and logic.\n",
        "code": "def game_loop():\n    print(\"Welcome to the Dungeon!\")\n    inventory = []\n    while True:\n        action = input(\"What do you do? (look/take/quit): \").lower()\n        if action == 'quit':\n            break\n        elif action == 'look':\n            print(\"You are in a dark room. There is a sword here.\")\n        elif action == 'take':\n            print(\"You take the sword.\")\n            inventory.append('sword')\n        else:\n            print(\"Unknown action.\")\n\nif __name__ == '__main__':\n    game_loop()\n"
    },
    "02-Intermediate-Projects/01-compression-algo": {
        "readme": "# Huffman Coding Compression\n\n## Project Specification\nImplement a text file compressor and decompressor using Huffman Coding trees.\n\n## Implementation Steps\n1. Read file and calculate character frequencies.\n2. Build a Min-Heap based on frequencies.\n3. Construct the Huffman Tree.\n4. Generate codes for each character.\n5. Encode the file and save the encoded string with the tree metadata.\n\n## Structure\n- `main.py`: Core compression/decompression logic.\n",
        "code": "import heapq\nfrom collections import Counter\n\nclass Node:\n    def __init__(self, char, freq):\n        self.char = char\n        self.freq = freq\n        self.left = None\n        self.right = None\n    \n    def __lt__(self, other):\n        return self.freq < other.freq\n\ndef build_huffman_tree(text):\n    freq = Counter(text)\n    heap = [Node(char, count) for char, count in freq.items()]\n    heapq.heapify(heap)\n    \n    while len(heap) > 1:\n        left = heapq.heappop(heap)\n        right = heapq.heappop(heap)\n        merged = Node(None, left.freq + right.freq)\n        merged.left = left\n        merged.right = right\n        heapq.heappush(heap, merged)\n        \n    return heap[0] if heap else None\n\nif __name__ == '__main__':\n    text = \"hello huffman\"\n    tree = build_huffman_tree(text)\n    print(\"Huffman tree root frequency:\", tree.freq)\n"
    },
    "02-Intermediate-Projects/02-simple-db": {
        "readme": "# Simple Key-Value Database\n\n## Project Specification\nA simple, persistent key-value store using a log-structured storage engine (like an LSM-tree basic concept) and an in-memory index.\n\n## Implementation Steps\n1. Create a `put(key, value)` method that appends to an append-only file.\n2. Maintain a hash map in memory mapping keys to file offsets.\n3. Create a `get(key)` method that seeks to the file offset and reads the value.\n4. Implement log compaction.\n\n## Structure\n- `main.py`: Database engine implementation.\n",
        "code": "import os\nimport json\n\nclass SimpleKVStore:\n    def __init__(self, filepath):\n        self.filepath = filepath\n        self.index = {}\n        self._load_index()\n    \n    def _load_index(self):\n        if not os.path.exists(self.filepath):\n            return\n        with open(self.filepath, 'r') as f:\n            while True:\n                offset = f.tell()\n                line = f.readline()\n                if not line: break\n                data = json.loads(line)\n                self.index[data['key']] = offset\n                \n    def put(self, key, value):\n        with open(self.filepath, 'a') as f:\n            offset = f.tell()\n            f.write(json.dumps({'key': key, 'value': value}) + '\\n')\n            self.index[key] = offset\n\n    def get(self, key):\n        if key not in self.index:\n            return None\n        with open(self.filepath, 'r') as f:\n            f.seek(self.index[key])\n            return json.loads(f.readline())['value']\n\nif __name__ == '__main__':\n    db = SimpleKVStore('db.log')\n    db.put('user1', 'alice')\n    print(db.get('user1'))\n"
    },
    "02-Intermediate-Projects/03-web-server": {
        "readme": "# Minimal HTTP Web Server\n\n## Project Specification\nA custom multi-threaded HTTP server implemented using Python's raw `socket` module. It serves static HTML/CSS files.\n\n## Implementation Steps\n1. Create a socket and bind it to a port.\n2. Listen for incoming TCP connections.\n3. Parse raw HTTP requests (method, path, headers).\n4. Read requested files from disk and construct HTTP response headers and body.\n5. Handle threading for concurrent connections.\n\n## Structure\n- `main.py`: Socket and HTTP processing logic.\n",
        "code": "import socket\n\ndef start_server(host='127.0.0.1', port=8080):\n    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    server.bind((host, port))\n    server.listen(5)\n    print(f\"Listening on {host}:{port}\")\n    \n    while True:\n        client_socket, addr = server.accept()\n        request = client_socket.recv(1024).decode('utf-8')\n        if request:\n            print(\"Received request:\\n\", request.split('\\n')[0])\n            response = \"HTTP/1.1 200 OK\\n\\nHello from Custom Server!\"\n            client_socket.sendall(response.encode('utf-8'))\n        client_socket.close()\n\nif __name__ == '__main__':\n    print(\"Run server? (uncomment to run)\")\n    # start_server()\n"
    },
    "02-Intermediate-Projects/04-compiler-lexer": {
        "readme": "# Compiler Lexer & Parser\n\n## Project Specification\nA lexical analyzer (tokenizer) and recursive descent parser for a simple custom programming language (e.g., basic arithmetic and variable assignment).\n\n## Implementation Steps\n1. Define language tokens using regular expressions.\n2. Build a lexer function that yields a stream of tokens.\n3. Build an Abstract Syntax Tree (AST) node hierarchy.\n4. Write a parser to convert tokens into an AST based on grammar rules.\n\n## Structure\n- `main.py`: Lexer and parser implementation.\n",
        "code": "import re\n\nTOKEN_TYPES = [\n    ('NUMBER',   r'\\d+'),\n    ('ASSIGN',   r'='),\n    ('IDENT',    r'[a-zA-Z_]\\w*'),\n    ('OP',       r'[+\\-*/]'),\n    ('SKIP',     r'[ \\t]+'),\n    ('MISMATCH', r'.'),\n]\n\ndef lex(code):\n    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_TYPES)\n    for mo in re.finditer(tok_regex, code):\n        kind = mo.lastgroup\n        value = mo.group()\n        if kind == 'SKIP': continue\n        elif kind == 'MISMATCH': raise RuntimeError(f'{value!r} unexpected')\n        yield kind, value\n\nif __name__ == '__main__':\n    code = \"x = 10 + 20\"\n    print(f\"Lexing: {code}\")\n    for token in lex(code):\n        print(token)\n"
    },
    "02-Intermediate-Projects/05-data-viz-tool": {
        "readme": "# Data Visualization Dashboard\n\n## Project Specification\nA simple interactive data visualization dashboard using pandas and a framework like Streamlit or Dash to visualize CSV datasets.\n\n## Implementation Steps\n1. Load dataset using pandas.\n2. Create interactive filters (e.g., dropdowns, sliders).\n3. Use Plotly or Matplotlib to generate charts (bar, line, scatter) based on filtered data.\n4. Expose the dashboard using Streamlit.\n\n## Structure\n- `main.py`: Data loading and dashboard UI.\n",
        "code": "import pandas as pd\n# import streamlit as st\n\ndef mock_dashboard():\n    df = pd.DataFrame({'Category': ['A', 'B', 'C'], 'Values': [10, 20, 15]})\n    print(\"Data loaded:\")\n    print(df)\n    print(\"\\nUse Streamlit (st.bar_chart) to visualize this data in a real environment.\")\n\nif __name__ == '__main__':\n    mock_dashboard()\n"
    },
    "03-Advanced-Projects/01-rag-system": {
        "readme": "# Retrieval-Augmented Generation (RAG) System\n\n## Project Specification\nA system that indexes documents, converts them to vector embeddings, and answers queries using an LLM combined with the retrieved documents for context.\n\n## Implementation Steps\n1. Load documents and chunk them into manageable sizes.\n2. Use an embedding model (e.g., OpenAI or HuggingFace) to embed chunks.\n3. Store embeddings in a Vector Database (like ChromaDB or FAISS).\n4. Given a query, retrieve top K relevant chunks.\n5. Pass retrieved context and query to a generative LLM to answer.\n\n## Structure\n- `main.py`: Embedding, retrieval, and generation logic.\n",
        "code": "import numpy as np\n\ndef simple_rag_mock(query, documents):\n    # Mocking vector search and retrieval\n    print(f\"Querying: {query}\")\n    # Imagine retrieving related doc\n    context = documents[0]\n    print(f\"Retrieved Context: {context}\")\n    response = f\"Generated answer based on '{context}'\"\n    return response\n\nif __name__ == '__main__':\n    docs = [\"Paris is the capital of France.\", \"Python is a programming language.\"]\n    print(simple_rag_mock(\"What is Paris?\", docs))\n"
    },
    "03-Advanced-Projects/02-ml-framework": {
        "readme": "# Custom Machine Learning Framework\n\n## Project Specification\nA miniature deep learning framework built from scratch with NumPy, featuring automatic differentiation (autograd) and basic neural network layers.\n\n## Implementation Steps\n1. Implement a `Tensor` class that tracks computation history (computational graph).\n2. Implement forward and backward passes for basic operations (+, -, *, /).\n3. Implement `Linear` and `ReLU` layers.\n4. Create a basic optimizer (e.g., SGD) and train a simple model on synthetic data.\n\n## Structure\n- `main.py`: Autograd engine and training loop.\n",
        "code": "class Value:\n    def __init__(self, data, _children=(), _op=''):\n        self.data = data\n        self.grad = 0\n        self._backward = lambda: None\n        self._prev = set(_children)\n        self._op = _op\n\n    def __add__(self, other):\n        other = other if isinstance(other, Value) else Value(other)\n        out = Value(self.data + other.data, (self, other), '+')\n        \n        def _backward():\n            self.grad += out.grad\n            other.grad += out.grad\n        out._backward = _backward\n        return out\n\nif __name__ == '__main__':\n    a = Value(2.0)\n    b = Value(3.0)\n    c = a + b\n    c.grad = 1.0\n    c._backward()\n    print(f\"c = {c.data}, a.grad = {a.grad}, b.grad = {b.grad}\")\n"
    },
    "03-Advanced-Projects/03-genai-chatbot": {
        "readme": "# GenAI Chatbot with Memory\n\n## Project Specification\nA complex chatbot that maintains conversational state (memory), handles multi-turn dialogues, and utilizes function calling / tools to fetch real-time information.\n\n## Implementation Steps\n1. Setup an LLM connection via API.\n2. Implement a rolling memory buffer to keep the context window in check.\n3. Define external tools (e.g., weather fetcher, web searcher) and parse LLM outputs to invoke them.\n4. Expose the bot via a chat interface.\n\n## Structure\n- `main.py`: Chat loop, memory management, and tool execution.\n",
        "code": "class ChatbotMemory:\n    def __init__(self):\n        self.history = []\n        \n    def add_message(self, role, content):\n        self.history.append({'role': role, 'content': content})\n        \n    def get_context(self):\n        return self.history[-5:] # Return last 5 messages\n\nif __name__ == '__main__':\n    bot = ChatbotMemory()\n    bot.add_message('user', 'Hello!')\n    bot.add_message('assistant', 'Hi, how can I help?')\n    print(\"Chat context:\", bot.get_context())\n"
    },
    "03-Advanced-Projects/04-high-perf-ds": {
        "readme": "# High-Performance Data Structures (C Extensions)\n\n## Project Specification\nImplement performance-critical data structures (e.g., a concurrent hash map or a B-Tree) in C/C++ and expose them to Python using `ctypes` or `pybind11`.\n\n## Implementation Steps\n1. Write the core data structure logic in C.\n2. Create a C wrapper with an API suitable for FFI.\n3. Compile to a shared library (.so / .dll).\n4. Write a Python module using `ctypes` to interface with the library, adding Pythonic magic methods.\n\n## Structure\n- `main.py`: Python wrapper and usage examples.\n- `structure.c` (mocked): Underlying C code.\n",
        "code": "# This is a conceptual mockup of how one would interface with a C library\nimport ctypes\n\ndef mock_c_extension_usage():\n    print(\"In a real scenario, you would load a .so or .dll file here.\")\n    print(\"libc = ctypes.CDLL('libcustom.so')\")\n    print(\"libc.insert(key, value)\")\n\nif __name__ == '__main__':\n    mock_c_extension_usage()\n"
    },
    "03-Advanced-Projects/05-trading-bot": {
        "readme": "# Algorithmic Trading Bot\n\n## Project Specification\nA bot that pulls real-time financial market data, evaluates a quantitative trading strategy (e.g., moving average crossover, mean reversion), and simulates or executes trades via a broker API.\n\n## Implementation Steps\n1. Connect to a market data websocket or REST API (e.g., Binance, Alpaca).\n2. Store incoming ticks/candles in an efficient time-series buffer.\n3. Implement backtesting and live trading modes for the strategy.\n4. Handle order execution, risk management, and portfolio tracking.\n\n## Structure\n- `main.py`: Main engine coordinating data ingestion and strategy execution.\n",
        "code": "import random\nimport time\n\ndef strategy_evaluate(price):\n    if price < 100:\n        return 'BUY'\n    elif price > 150:\n        return 'SELL'\n    return 'HOLD'\n\nif __name__ == '__main__':\n    print(\"Starting Mock Trading Bot\")\n    for _ in range(5):\n        price = random.uniform(90, 160)\n        action = strategy_evaluate(price)\n        print(f\"Price: ${price:.2f} -> Action: {action}\")\n        time.sleep(0.5)\n"
    }
}

for cat, projs in projects.items():
    for proj in projs:
        proj_dir = os.path.join(base_dir, cat, proj)
        os.makedirs(proj_dir, exist_ok=True)
        
        # Write README
        key = f"{cat}/{proj}"
        if key in content_templates:
            with open(os.path.join(proj_dir, 'README.md'), 'w') as f:
                f.write(content_templates[key]['readme'])
            with open(os.path.join(proj_dir, 'main.py'), 'w') as f:
                f.write(content_templates[key]['code'])

print("All project files generated successfully.")
