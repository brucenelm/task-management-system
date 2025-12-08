import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QTextEdit, QTableWidget, QTableWidgetItem, 
    QHeaderView, QFileDialog, QMessageBox, QLabel
)
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl, QByteArray, Qt

class ApiClientExplorer(QMainWindow):
    """
    A PyQt6 desktop client for fetching data from an API, parsing JSON, 
    and displaying/exporting the results.
    """
    API_ENDPOINT = "https://jsonplaceholder.typicode.com/users"
    TABLE_HEADERS = ["ID", "Name", "Username", "Email", "City"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client API Data Explorer (PyQt6)")
        self.setGeometry(100, 100, 900, 700)
        
        # Data storage for export
        self.fetched_data = None 

        # 1. Setup Network Manager (Key for asynchronous requests)
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self.handle_api_response)
        
        self._setup_ui()

    def _setup_ui(self):
        # --- Central Widget and Layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # --- 2. Action Buttons ---
        self.fetch_button = QPushButton("1. Fetch User Data from API")
        self.fetch_button.clicked.connect(self.fetch_data)
        layout.addWidget(self.fetch_button)

        self.save_button = QPushButton("4. Save Fetched Data to Local JSON File")
        self.save_button.clicked.connect(self.save_data_to_json)
        self.save_button.setEnabled(False) # Disabled until data is fetched
        layout.addWidget(self.save_button)
        
        # --- 3. Data Display Sections ---
        
        # A. Raw JSON Output
        layout.addWidget(QLabel("Raw JSON Response:"))
        self.json_display = QTextEdit()
        self.json_display.setFixedHeight(150)
        self.json_display.setReadOnly(True)
        self.json_display.setPlaceholderText("2. Raw JSON data will appear here...")
        layout.addWidget(self.json_display)

        # B. Structured Table Output
        layout.addWidget(QLabel("Structured Data (Parsed):"))
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.TABLE_HEADERS))
        self.table_widget.setHorizontalHeaderLabels(self.TABLE_HEADERS)
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_widget)
        
        # C. Status Label
        self.status_label = QLabel("Ready.")
        layout.addWidget(self.status_label)

    # --- API Request and Handling ---

    def fetch_data(self):
        """Initiates the asynchronous GET request."""
        self.status_label.setText("Fetching data... Sending request to API.")
        self.fetch_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.json_display.clear()
        self.table_widget.setRowCount(0)

        request = QNetworkRequest(QUrl(self.API_ENDPOINT))
        self.network_manager.get(request)

    def handle_api_response(self, reply: QNetworkReply):
        """Processes the QNetworkReply when the asynchronous request finishes."""
        self.fetch_button.setEnabled(True)
        
        if reply.error() != QNetworkReply.NetworkError.NoError:
            error_msg = f"API Error: {reply.errorString()}"
            self.status_label.setText(error_msg)
            QMessageBox.critical(self, "Network Error", error_msg)
            reply.deleteLater()
            return

        # 1. Read Raw Data
        data_bytes: QByteArray = reply.readAll()
        json_string = str(data_bytes, 'utf-8')
        
        # 2. Display Raw JSON (Pretty Printed)
        try:
            # Parse the string into a Python object (list of dicts)
            parsed_data = json.loads(json_string)
            self.fetched_data = parsed_data # Store for export
            
            # Display pretty-printed JSON
            formatted_json = json.dumps(parsed_data, indent=2)
            self.json_display.setText(formatted_json)
            self.status_label.setText("3. Data fetched successfully and parsed.")
            
            self._display_data_in_table(parsed_data)
            self.save_button.setEnabled(True)
            
        except json.JSONDecodeError:
            error_msg = "Error: Received data is not valid JSON."
            self.json_display.setText(error_msg)
            self.status_label.setText(error_msg)
            self.fetched_data = None
            QMessageBox.warning(self, "JSON Error", error_msg)
            
        reply.deleteLater()

    # --- Display Logic ---

    def _display_data_in_table(self, data_list):
        """Populates the QTableWidget with structured data."""
        self.table_widget.setRowCount(len(data_list))
        
        for row_index, user in enumerate(data_list):
            # Extract data, handling nested fields (like 'address')
            user_id = str(user.get("id", ""))
            name = user.get("name", "")
            username = user.get("username", "")
            email = user.get("email", "")
            city = user.get("address", {}).get("city", "")

            # Set items in the table
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(user_id))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(name))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(username))
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(email))
            self.table_widget.setItem(row_index, 4, QTableWidgetItem(city))

    # --- Export Logic ---

    def save_data_to_json(self):
        """Opens a file dialog to save the stored fetched_data as a JSON file."""
        if not self.fetched_data:
            QMessageBox.warning(self, "Save Error", "No data has been fetched yet to save.")
            return

        # Open native "Save As" file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save JSON Data", 
            "api_users_data.json", # Default filename
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                # Save the Python object directly to the file as JSON
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.fetched_data, f, indent=4)
                
                self.status_label.setText(f"Data successfully saved to: {file_path}")
                QMessageBox.information(self, "Save Success", f"Data saved to:\n{file_path}")
                
            except Exception as e:
                error_msg = f"Failed to save file: {e}"
                self.status_label.setText(error_msg)
                QMessageBox.critical(self, "File Save Error", error_msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApiClientExplorer()
    window.show()
    sys.exit(app.exec())