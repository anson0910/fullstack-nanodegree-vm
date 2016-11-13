from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def helloGetHandler(self):
        print self.path
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = ""
        output += "<html><body>"
        output += "<h1>Hello!</h1>"
        output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
        output += "</body></html>"
        self.wfile.write(output)

    def helloPostHandler(self):
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        ctype, pdict = cgi.parse_header(
            self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get('message')
        output = ""
        output += "<html><body>"
        output += " <h2> Okay, how about this: </h2>"
        output += "<h1> %s </h1>" % messagecontent[0]
        output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
        output += "</body></html>"
        self.wfile.write(output)

    def restaurantsHandler(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        restaurants = session.query(Restaurant.name, Restaurant.id).all()
        output = ""
        output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"
        output += "<html><body>"
        for r in restaurants:
            output += r.name + "</br>"
            output += "<a href='/restaurants/%s/edit'>Edit</a></br>" % r.id
            output += "<a href='/restaurants/%s/delete'>Delete</a></br></br>" % r.id
        output += "</body></html>"
        self.wfile.write(output)

    def restaurantsNewGetHandler(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = ""
        output += "<html><body>"
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
            <h2>Make a New Restaurant</h2>
            <input name="message" type="text" placeholder = 'New Restaurant Name'>
            <input type="submit" value="Submit"></form>'''
        output += "</body></html>"
        self.wfile.write(output)

    def restaurantsNewPostHandler(self):
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()

        ctype, pdict = cgi.parse_header(
            self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get('message')
        restaurant = Restaurant(name=messagecontent[0])
        session.add(restaurant)
        session.commit()

    def restaurantsEditGetHandler(self):
        res_id = self.path.split('/')[-2]
        restaurant = session.query(Restaurant).filter_by(id=res_id).one()

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = ""
        output += "<html><body>"
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/{res_id}/edit'>
                <h2>{name}</h2>
                <input name="message" type="text" placeholder = "{name}">
                <input type="submit" value="Submit"></form>'''.format(res_id=res_id,  name=restaurant.name)
        output += "</body></html>"
        self.wfile.write(output)

    def restaurantsEditPostHandler(self):
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()

        res_id = self.path.split('/')[-2]
        restaurant = session.query(Restaurant).filter_by(id=res_id).one()

        ctype, pdict = cgi.parse_header(
            self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get('message')
        restaurant.name = messagecontent[0]
        session.add(restaurant)
        session.commit()

    def restaurantsDeleteGetHandler(self):
        res_id = self.path.split('/')[-2]
        restaurant = session.query(Restaurant).filter_by(id=res_id).one()

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = ""
        output += "<html><body>"
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/{res_id}/delete'>
                <h2>Are you sure you want to delete {name}?</h2>
                <input type="submit" value="Delete"></form>'''.format(res_id=res_id, name=restaurant.name)
        output += "</body></html>"
        self.wfile.write(output)

    def restaurantsDeletePostHandler(self):
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()

        res_id = self.path.split('/')[-2]
        restaurant = session.query(Restaurant).filter_by(id=res_id).one()
        session.delete(restaurant)
        session.commit()

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.helloGetHandler()
                return

            if self.path == "/restaurants":
                self.restaurantsHandler()
                return

            if self.path == "/restaurants/new":
                self.restaurantsNewGetHandler()
                return

            if self.path.endswith("/edit"):
                self.restaurantsEditGetHandler()
                return

            if self.path.endswith("/delete"):
                self.restaurantsDeleteGetHandler()
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            # if self.path.endswith("/hello"):
            #     self.helloPostHandler()
            #     return

            if self.path == "/restaurants/new":
                self.restaurantsNewPostHandler()
                return

            if self.path.endswith("/edit"):
                self.restaurantsEditPostHandler()
                return

            if self.path.endswith("/delete"):
                self.restaurantsDeletePostHandler()
                return

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
