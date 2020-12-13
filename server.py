import SimpleHTTPServer
import SocketServer
from urlparse import urlparse, parse_qs
import psycopg2

# port of webserver
PORT = 7003

# DB connection
host = "localhost"  # local ip machine
port = "5432"
dbname = "webserver"
user = "postgres"
password = "postgres"
connection = psycopg2.connect(
    host=host, port=port, dbname=dbname, user=user, password=password)
cursorConnection = connection.cursor()

# DB create user
def createUser(name, age, sex, email, phone):
    try:
        query = "INSERT INTO users (name, age, sex, email, phone) VALUES (%s, %s, %s, %s, %s);"
        data = (name, age, sex, email, phone)
        cursorConnection.execute(query, data)
        connection.commit()
        return 200
    except Exception:
        return 500

# DB get all users
def getUsers():
    try:
        query = "SELECT * FROM users;"
        cursorConnection.execute(query)
        users = cursorConnection.fetchall()
        return users
    except Exception:
        return 500

class handleWebPage(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            # Comparing url path (route)
            if(self.path == "/user/list"):
                # Opening files
                file_upperContent = open(
                    "src/template/upperContent.html")
                file_lowerContent = open("src/template/lowerContent.html")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # Geting content from files and writing on response file
                self.wfile.write(file_upperContent.read())
                self.wfile.write(usersTable())  # Getting html table and data
                self.wfile.write(file_lowerContent.read())
                # Closing files
                file_upperContent.close()
                file_lowerContent.close()
            else:
                file_index = open("src/index.html")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file_index.read())
                file_index.close()

        except IOError:
            self.send_error(404, self.path)
        return

    def do_POST(self):
        # Opening files
        file_upperContent = open("src/template/upperContent.html")
        file_middleContent = ""
        file_lowerContent = open("src/template/lowerContent.html")
        #Reading POST file
        size = int(self.headers['Content-Length'])
        data = self.rfile.read(size)
        # Getting parameters and sending to db function 
        # parse_qs(data) generate following structure:{'key': ['value'], 'key2': ['value']}
        status = createUser(
            parse_qs(data)['name'][0],
            parse_qs(data)['age'][0],
            parse_qs(data)['sex'][0],
            parse_qs(data)['email'][0],
            parse_qs(data)['phone'][0])
        if(status == 200):
            file_middleContent += "<h2 style='margin-left: 30%;'>Registered successfully! </h2>"
        elif(status == 500):
            file_middleContent += "<h2 style='margin-left: 30%;'>An error happened! </h2>"
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Geting content from files and writing on response file
        self.wfile.write(file_upperContent.read())
        self.wfile.write(file_middleContent)
        self.wfile.write(file_lowerContent.read())
        # Closing files
        file_upperContent.close()
        file_lowerContent.close()

# Build a table html with users fetched
def usersTable():
    #Getting users
    users = getUsers()

    if users == 500:
        return "<h2 style='margin-left: 30%;'>An error happened! </h2>"

    #Building html middle content
    html = """ <table class="table">
    <thead class="thead-dark">
    <tr><th scope="col">ID</th>
    <th scope="col">Name</th>
    <th scope="col">Age</th>
    <th scope="col">Sex</th>
    <th scope="col">Email</th>
    <th scope="col">Phone</th></tr>
    </thead>
    <tbody> """

    if users:
        for row in users:
            html += "<tr>"
            html += "<th scope='row'>"+str(row[0])+"</th>"
            html += "<td>"+str(row[1])+"</td>"
            html += "<td>"+str(row[2])+"</td>"
            html += "<td>"+str(row[3])+"</td>"
            html += "<td>"+str(row[4])+"</td>"
            html += "<td>"+str(row[5])+"</td>"
            html += "</tr>"

    html += """ </tbody>
    </table> """

    return html

try:
    httpd = SocketServer.ThreadingTCPServer(('', PORT), handleWebPage)
    print("Server running... ", PORT)
    httpd.serve_forever()

except KeyboardInterrupt:
    print("You disconnected, closing connections...")
    httpd.socket.close()
    connection.close()
    httpd.shutdown()
