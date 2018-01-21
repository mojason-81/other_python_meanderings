from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, Restaurant, MenuItem
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
import cgi
import re

class webserverHandler(BaseHTTPRequestHandler):
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    session = DBSession()

    def do_GET(self):
        edit_re = re.compile('/restaurants/\d*/edit')
        delete_re = re.compile('/restaurants/\d*/delete')
        try:
            output = ""
            if self.path.endswith("/restaurants"):
                restaurants = self.session.query(Restaurant).all()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output += "<html><body>"
                output += "<h1>Restaurants</h1><br>"
                output += "<a href='/restaurants/new'>New Restaurant</a>"
                for restaurant in restaurants:
                    output += "<ul><li>"
                    output += restaurant.name
                    output += "<ul><li>"
                    output += "<a href='/restaurants/" + str(restaurant.id) + "/edit'>Edit</a>"
                    output += "</ul></li>"
                    output += "<ul><li>"
                    output += "<a href='/restaurants/" + str(restaurant.id) + "/delete'>Delete</a>"
                    output += "</ul></li>"
                    output += "</ul></li>"
                output += "</body></html>"

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output += "<html><body><h2>New Restaurant</h2>"
                output += "<form method='POST' enctype='multipart/form-data'>"
                output += "<input name='new_name' type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"

            if edit_re.match(self.path) != None:
                url = urlparse(self.path)
                dest = url[2]
                finds = re.findall('\d+', dest)
                restaurant_id = ""
                for find in finds:
                    restaurant_id += str(find)

                try:
                    restaurant = self.session.query(Restaurant).filter_by(id = int(restaurant_id)).one()
                except NoResultFound:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<h2>404: No Record Found</h2>"
                    output += "<a href='/restaurants'>Back to listing</a>"
                    self.wfile.write(output)
                    return

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output += "<html><body><h2>Edit " + restaurant.name + "</h2>"
                output += "<form method='POST' enctype='multipart/form-data'>"
                output += "<input name='new_name' type='text'>"
                output += "<input name='restaurant_id' type='hidden' value='%s'>" % restaurant_id
                output += "<input type='submit' value='Submit'>"
                output += "</form>"
                output += "</body></html>"

            if delete_re.match(self.path) != None:
                url = urlparse(self.path)
                dest = url[2]
                finds = re.findall('\d+', dest)
                restaurant_id = ""
                for find in finds:
                    restaurant_id += str(find)

                try:
                    restaurant = self.session.query(Restaurant).filter_by(id = int(restaurant_id)).one()
                except NoResultFound:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<h2>404: No Record Found</h2>"
                    output += "<a href='/restaurants'>Back to listing</a>"
                    self.wfile.write(output)
                    return

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output += "<html><body><h2>Delete " + restaurant.name + "</h2>"
                output += "<form method='POST' enctype='multipart/form-data'>"
                output += "<input name='restaurant_id' type='hidden' value='%s'>" % restaurant_id
                output += "<input type='submit' value='Delete'>"
                output += "</form>"
                output += "</body></html>"

            self.wfile.write(output)
            return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(201)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)

                restaurant_name = fields.get('new_name')
                restaurant_id = fields.get('restaurant_id')

                deleting = False

                if restaurant_id == None:
                    try:
                        print('Creating')
                        restaurant = self.session.query(Restaurant).filter_by(name = restaurant_name).one()
                        restaurant.name = restaurant_name[0]
                    except:
                        restaurant = Restaurant(name = restaurant_name[0])
                elif restaurant_name == None:
                    print('Deleting')
                    restaurant = self.session.query(Restaurant).filter_by(id = restaurant_id[0]).one()
                    deleting = True
                else:
                    print('Editing')
                    print(restaurant_name)
                    restaurant = self.session.query(Restaurant).filter_by(id = restaurant_id[0]).one()
                    restaurant.name = restaurant_name[0]

                if deleting:
                    print('Still deleting')
                    self.session.delete(restaurant)
                else:
                    print('Creating or Editing')
                    self.session.add(restaurant)

                self.session.commit()

            output = ""
            output += "<html><body>"
            output += " <h2>Done with %s</h2><br>" % restaurant.name
            output += "<a href='/restaurants'>Back to listing</a>"
            output += "</body></html>"
            self.wfile.write(output)
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "KBI"
        server.socket.close()

if __name__ == '__main__':
    main()
