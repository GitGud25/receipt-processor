# Receipt Processor

A Python web service built with Flask to process receipts and calculate points based on rules defined in the assignment. The API, specified in `api.yml`, includes two endpoints:
- `POST /receipts/process`: Validates a JSON receipt and returns a unique ID.
- `GET /receipts/{id}/points`: Returns the points for a receipt by ID.

Data is stored in memory, as persistence is not required.

## Prerequisites

- **Python 3.11**: For local execution.
- **Docker**: For containerized execution.

## Project Structure

- `main.py`: Flask application with API endpoints and deduplication logic.
- `points.py`: Implements points calculation rules.
- `requirements.txt`: Lists Flask==3.0.3.
- `api.yml`: OpenAPI 3.0.3 specification.
- `examples/`: Contains `simple-receipt.json` (Target, single item) and `morning-receipt.json` (Walgreens, two items).
- `Dockerfile`: Configures the Docker container.

## Running Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/GitGud25/receipt-processor
   cd receipt-processor
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python main.py
   ```
   The server starts at `http://localhost:5000`.

## Running with Docker

1. **Install Docker**:
   - On macOS, download [Docker Desktop](https://www.docker.com/products/docker-desktop/).
   - Verify:
     ```bash
     docker --version
     ```

2. **Build the Docker Image**:
   ```bash
   docker build -t receipt-processor .
   ```

3. **Run the Container**:
   ```bash
   docker run -p 8000:5000 receipt-processor
   ```
   The server starts at `http://localhost:8000`.

## Troubleshooting

- **Port 8000 in Use**:
  - Check:
    ```bash
    lsof -i :8000
    ```
  - Terminate:
    ```bash
    kill -9 <pid>
    ```
  - Or use another port (e.g., 8001):
    ```bash
    docker run -p 8001:5000 receipt-processor
    ```
- **Port 5000 Conflicts (macOS)**:
  - If port 5000 was previously used, ensure it’s free or disable AirPlay Receiver:
    - System Settings > General > AirDrop & Handoff > Turn off AirPlay Receiver
    - Or: `defaults write com.apple.controlcenter AirplayRecieverEnabled -bool false`
  - Check:
    ```bash
    lsof -i :5000
    ```
- **Docker Command Not Found**:
  - Install Docker Desktop.
  - Add to `~/.zshrc`:
    ```bash
    export PATH=$PATH:/Applications/Docker.app/Contents/Resources/bin
    ```
    ```bash
    source ~/.zshrc
    ```
- **Docker Build Errors**:
  - Verify files (`main.py`, `points.py`, etc.) are present:
    ```bash
    ls -la
    ```

## Notes

- **Data Storage**: In-memory, no persistence, as specified.
- **Language**: Python with Flask, Dockerized for non-Go solution.
- **Server**: Flask’s built-in server, debug mode disabled.
- **Deduplication**: If a receipt with identical data is submitted, the existing `receipt_id` is returned instead of generating a new one, implemented using receipt hashing in `main.py`.
- **Points**: Calculated per assignment rules in `points.py` (excludes Rule 6, LLM-specific).

## Contact

For questions, refer to the assignment instructions or contact the repository owner.