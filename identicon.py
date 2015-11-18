from StringIO import StringIO
import webapp2
import png
import hashlib
import struct
import random
import base64

MAIN_PAGE = """\

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="favicon.ico">

    <title>Identicon generator</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">

    <!-- Custom styles for this template -->
    <link href="/s/identicon.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">Identicon generator</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li><a href="#about">Github</a></li>

          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">

      <div class="starter-template">
        <h1>Identicon generator</h1>
        <p class="lead">The following is a random indenticon from this service API</p>
        <img src="/%s?s=20&p=7" />
      </div>

      <p>
      <h2>API</h2>
      <i>http://identicon-1132.appspot.com/[data]?s=[s]&p=[p]&f=[f]<i>
      <ul>
          <li><strong>[data]</strong> This data will be hashed with sha256 and the result used to generate the identicon </li>
          <li>[s] (Optional) The size of the identicon smallest unit. Accepted value are from 4 to 8</li>
          <li>[p] (Optional) The pixel size of the smalles unit. Accepted value are from 1 to 20</li>
          <li>[f] (Optional) The output format wich default to png but accept also base64</li>
      </ul>
      </p>

    </div><!-- /.container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="../../dist/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>

"""

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class Home(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(MAIN_PAGE % (str(random.randint(1,2014122214) )) )

class Identicon(webapp2.RequestHandler):
    def get(self, identidata):
        #data = "Testing commit & reveal feature!"
        #data = str(random.random() )
        p = self.request.get('p')
        s = self.request.get('s')
        f = self.request.get('f')
        print "p=" + p + " s=" + s + " f=" + f
        datahash = hashlib.sha256(identidata)
        digest = datahash.digest()

        first = struct.unpack('B', digest[0])[0]
        second = struct.unpack('B', digest[1])[0]
        third = struct.unpack('B', digest[2])[0]
        palette=[(255,255,255,0), (first,second,third,255)]

        height = 5 if p=="" or not RepresentsInt(p) else max(4,min(8,int(p)))
        width = height;
        mul = 13 if s=="" or not RepresentsInt(s) else max(1,min(20,int(s))) ;
        print "height=" + str(height) + " width=" + str(width) + " mul=" + str(mul)

        s = [[0 for col in range(height*mul)] for row in range(width*mul)]

        for x in range(width) :
            if x < height/2 :
                i = x
            else:
                i = width - 1 - x;

            for y in range(height) :
                curi=struct.unpack('B', digest[i])[0]
                cur=(curi >> y & 1);
                if cur :
                    for m1 in range(mul) :
                        for m2 in range(mul) :
                            s[y*mul+m1][x*mul+m2]=1;

        w = png.Writer(len(s[0]), len(s), palette=palette, bitdepth=1)
        content = StringIO()
        w.write(content, s)

        if f=="base64" :
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write(base64.b64encode( content.getvalue() ))
        else :
            self.response.headers['Content-Type'] = 'image/png'
            self.response.write(content.getvalue())



app = webapp2.WSGIApplication([
    ('/', Home),
    (r'/(\w+)', Identicon),

], debug=True)
