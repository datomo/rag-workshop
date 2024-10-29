"""
RAG Cost App

Author: Anastasiia Popova
Email: anastasiia.popova@stud.unibas.ch

Note:
Perplexity AI assisted in code writing, editing, and more effective information searches. The generated output underwent critical evaluation. The author is solely responsible for the content.
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout

def calculate_llm_cost(avg_input_tokens, avg_output_tokens, input_cost, output_cost, num_requests, tokens_per_cost):
    """
    Parameters:
    avg_input_tokens (float): Average number of input tokens per request
    avg_output_tokens (float): Average number of output tokens per request
    input_cost (float): Cost of an input token
    output_cost (float): Cost of an output token
    num_requests (int): Number of requests
    tokens_per_cost (int): Number of tokens in the specified cost
    
    Returns:
    float: The calculated price in dollars
    """
    # Calculate the cost per request
    cost_per_request = (avg_input_tokens * input_cost) + (avg_output_tokens * output_cost)
    
    # Calculate the total price
    price = cost_per_request * (num_requests / tokens_per_cost)
    
    return round(price, 3)

def calculate_embeddings_cost(avg_input_tokens, input_cost, num_requests, tokens_per_cost):

    """
    Parameters:
    avg_input_tokens (float): Average number of input tokens per request
    input_cost (float): Cost of an input token
    num_requests (int): Number of requests
    tokens_per_cost (int): Number of tokens in the specified cost
    
    Returns:
    float: The calculated price in dollars
    """
    # Calculate the cost per request
    cost_per_request = avg_input_tokens * input_cost
    
    # Calculate the total price
    price = cost_per_request * (num_requests / tokens_per_cost)
    
    return round(price, 3)



class RAGCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RAG Calculator")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        labels = ["Chunk Size:", "Rank Size:", "Number of Chunks:", 
                  "Avg Input Tokens:", "Avg Output Tokens:", "Number of Requests:"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            entry = QLineEdit()
            grid_layout.addWidget(label, i, 0)
            grid_layout.addWidget(entry, i, 1)
            self.entries[label_text] = entry

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

    def calculate(self):
        try:
            chunk_size_char = int(self.entries["Chunk Size:"].text())
            chunk_size = chunk_size_char / 4  # in tokens
            
            rank_size = int(self.entries["Rank Size:"].text())
            num_chunks = int(self.entries["Number of Chunks:"].text())
            avg_input_tokens = int(self.entries["Avg Input Tokens:"].text())
            avg_output_tokens = int(self.entries["Avg Output Tokens:"].text())
            num_requests = int(self.entries["Number of Requests:"].text())

            rag_input = chunk_size * rank_size + avg_input_tokens

            # COST OF MODELS
            input_cost = 0.6
            output_cost = 0.15
            emb_cost = 0.10
            tokens_per_cost = 1000000

            price_llm = calculate_llm_cost(rag_input, avg_output_tokens, input_cost, output_cost, num_requests, tokens_per_cost)

            rag_input_tokens = chunk_size * num_chunks

            price_emb = calculate_embeddings_cost(rag_input_tokens, emb_cost, 1, tokens_per_cost)

            price_total = round(price_llm + price_emb, 3)

            self.result_label.setText(f"Price LLM: ${price_llm}\nPrice Embeddings: ${price_emb}\nPrice Total: ${price_total}")
        except ValueError:
            self.result_label.setText("Please enter valid numbers")

def main():
    app = QApplication(sys.argv)
    calculator = RAGCalculator()
    calculator.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()