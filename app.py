import http.server
import socketserver
import cgi
import mysql.connector

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'SupplyDB',
}

# Define a handler to handle form submissions
class FormHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/form':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('form.html', 'rb') as file:
                self.wfile.write(file.read())

    def do_POST(self):
        if self.path == '/query':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            user_input = form.getvalue('user_input')

            # Connect to the database
            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                # Execute your SQL query here
                query = "SELECT * FROM Suppliers"
                cursor.execute(query, (user_input,))

                # Fetch the results
                results = cursor.fetchall()

                for row in results:
                    self.wfile.write(f"{row}<br>".encode())

            except mysql.connector.Error as err:
                self.wfile.write(f"Error: {err}".encode())
            finally:
                cursor.close()
                connection.close()

# # Start the HTTP server
# with socketserver.TCPServer(('localhost', 8080), FormHandler) as httpd:
#     print('Server running at http://localhost:8080')
#     httpd.serve_forever()