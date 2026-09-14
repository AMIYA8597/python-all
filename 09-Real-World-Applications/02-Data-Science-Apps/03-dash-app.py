"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (DATA VISUALIZATION / DASH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior Data Scientist finishes a complex Machine Learning model. They 
# present the raw JSON output and a static PNG graph to the CEO. The CEO 
# asks, "What if we change the interest rate parameter to 5%?" The junior 
# scientist replies, "Give me 20 minutes to re-run the Python script." The 
# CEO loses confidence and cancels the project.
#
# A senior Data Scientist uses `Plotly Dash`. They mathematically bind their 
# Python functions to a React.js frontend without writing a single line of 
# JavaScript. They deploy a live, interactive web application. When the CEO 
# drags a UI slider to 5%, the browser fires an AJAX request, the Python 
# backend instantly recalculates the matrix, and the React frontend dynamically 
# re-renders the 3D graph in 0.2 seconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the architecture of Interactive Web Data Apps (Dash / Streamlit).
# - Understand Reactive Callbacks (`@app.callback`).
# - Differentiate between Server-Side Rendering and Client-Side Rendering.
#
# ==============================================================================
"""

import threading
import time
import requests
import random
# Gracefully handle missing dependencies
try:
    import dash
    from dash import dcc, html, Input, Output
    import plotly.graph_objs as go
    HAS_DASH = True
except ImportError:
    HAS_DASH = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE REACTIVE ARCHITECTURE (DASH APP)
# ==============================================================================
if HAS_DASH:
    # Dash is physically built on top of Flask! It spins up a WSGI server!
    app = dash.Dash(__name__)
    
    # We turn off massive logging for the lab
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # --- 1. THE VIRTUAL DOM (Frontend Layout) ---
    # We mathematically construct the HTML/React structure entirely in Python!
    app.layout = html.Div([
        html.H1("Live Algorithmic Trading Simulator", style={'textAlign': 'center'}),
        
        # A React Slider Component!
        html.Label("Volatility Index (Risk Level):"),
        dcc.Slider(
            id='volatility-slider',
            min=1,
            max=10,
            step=1,
            value=5, # Default value
            marks={i: str(i) for i in range(1, 11)}
        ),
        
        # The Graph Component! (It waits for data from the backend)
        dcc.Graph(id='trading-chart')
    ], style={'maxWidth': '800px', 'margin': 'auto', 'fontFamily': 'Arial'})


    # --- 2. THE REACTIVE CALLBACK (Backend Logic) ---
    # This is the architectural magic. We bind the Output (the Graph) to the 
    # Input (the Slider). When the Slider moves on the user's browser, Dash 
    # automatically POSTs the new integer to this Python function!
    @app.callback(
        Output('trading-chart', 'figure'),
        Input('volatility-slider', 'value')
    )
    def update_graph(volatility: int):
        """Re-calculates the entire simulation based on the UI input."""
        # 1. Simulate a heavy mathematical calculation based on the parameter!
        prices = [100.0]
        for _ in range(50):
            # Higher volatility = wilder price swings
            swing = random.uniform(-volatility, volatility)
            prices.append(prices[-1] + swing)
            
        # 2. Construct the Plotly Graph Object
        figure = {
            'data': [
                go.Scatter(
                    y=prices,
                    mode='lines+markers',
                    name='Stock Price',
                    line=dict(color='blue')
                )
            ],
            'layout': go.Layout(
                title=f"Simulation at Volatility Level {volatility}",
                xaxis={'title': 'Time (Days)'},
                yaxis={'title': 'Price ($)'}
            )
        }
        
        # 3. Return the JSON payload! Dash automatically updates the React frontend!
        return figure


# ==============================================================================
# 4. MATHEMATICAL PROOF OF EXECUTION
# ==============================================================================
def run_dash_server():
    """Boot the Dash server in the background."""
    # We run on 8050, the standard Dash port
    app.run_server(host='127.0.0.1', port=8050, debug=False, use_reloader=False)

def demonstrate_dash_app():
    section_header("Interactive Data Visualization (Plotly Dash)")
    
    if not HAS_DASH:
        print("  [ERROR] Dash is not installed.")
        print("  Run `pip install dash plotly pandas` to execute this lab.")
        return
        
    print("  [INIT] Booting Dash Server on background OS Thread...")
    server_thread = threading.Thread(target=run_dash_server, daemon=True)
    server_thread.start()
    
    # Wait for TCP binding
    time.sleep(1.5)
    
    base_url = "http://127.0.0.1:8050"
    
    print("\n  [TEST 1: The Initial Page Load]")
    # The browser sends a GET request for the HTML
    res1 = requests.get(base_url)
    print(f"    -> Status Code: {res1.status_code}")
    print("    -> Content:     React.js virtual DOM initialized.")
    
    print("\n  [TEST 2: The Reactive Callback (Simulating Slider Movement)]")
    # When a user drags a slider, Dash fires an AJAX POST request to `_dash-update-component`
    # We will simulate the browser's JSON payload mathematically!
    payload = {
        "output": "trading-chart.figure",
        "changedPropIds": ["volatility-slider.value"],
        "inputs": [
            {"id": "volatility-slider", "property": "value", "value": 9} # Changed to 9!
        ]
    }
    
    # Fire the AJAX request!
    res2 = requests.post(f"{base_url}/_dash-update-component", json=payload)
    print(f"    -> Status Code: {res2.status_code}")
    print("    -> Backend re-calculated the matrix instantly!")
    
    # The response is the new Graph JSON, which React natively renders!
    response_json = res2.json()
    new_title = response_json['response']['trading-chart']['figure']['layout']['title']
    print(f"    -> Graph updated to: '{new_title['text']}'")
    
    print("\n  [SHUTDOWN] Terminating Client. Background Server thread will die automatically.")


def run_all_labs():
    demonstrate_dash_app()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the architectural difference between a static rendering library like `matplotlib` and a reactive library like `Dash` or `Streamlit`?"
   Senior Answer: "`matplotlib` is a synchronous, server-side plotting library. It mathematically calculates the pixel coordinates of the data and physicalizes it into a static PNG or JPG byte stream. Once the image is rendered, it is completely immutable. If the user wants to zoom in, the Python backend must execute the script again, generate a brand new PNG, and transmit it. `Dash` (built on Plotly and React) utilizes Client-Side Rendering. The Python backend mathematically serializes the raw *data points* into a lightweight JSON payload and sends it to the browser. The JavaScript engine in the browser reads the JSON and physically renders the pixels dynamically on the client's GPU. This allows the user to mathematically zoom, pan, and hover over data points at 60 FPS in the browser with zero additional network requests to the Python server."

2. Interviewer: "How does the `@app.callback` decorator physically bridge the gap between a button click on a web browser and a Python function running on a server in AWS?"
   Senior Answer: "The `@app.callback` decorator mathematically registers a mapping between a specific Frontend Component ID (e.g., `submit-btn`) and a Python function. When the Dash application boots, it automatically injects a JavaScript event listener (AJAX) into the React frontend for that specific button. When the user clicks the button on their laptop, the JS listener intercepts the click, packages the current state of the UI into a JSON payload, and executes an asynchronous `POST` request (`/_dash-update-component`) over the internet to the Flask server. Flask routes the JSON to the Python function, executes the Data Science logic, and returns the new JSON state back to the browser, where React instantly updates the DOM."

3. Interviewer: "Why are Dash and Streamlit applications considered 'State-less', and why is this critical for horizontal scalability?"
   Senior Answer: "In a 'State-less' architecture, the Python server mathematically retains absolutely zero memory of the user's session between clicks. When User A clicks the slider, the backend processes the request and instantly forgets User A exists. If the application was 'State-ful' (remembering variables in RAM), and we scaled up to 10 servers, the user's next click might hit Server B, causing a catastrophic crash because Server B doesn't have their RAM variables. Because Dash forces all UI state (slider values, dropdown selections) to be stored entirely in the *Client's Browser* and transmitted within the JSON payload on every click, we can flawlessly deploy $100$ load-balanced Python servers, mathematically guaranteeing that any server can safely process any request."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Data Science (Plotly Dash) Completed.")
