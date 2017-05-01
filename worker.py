import webapp2

class WorkerTest(webapp2.RequestHandler):
    def get(self):
        self.response.write("""
            <form method="post" action="/tests">
                <label>Check your sites</label>
                <button>Check!</button>
            </form>
        """)


app = webapp2.WSGIApplication([
    ('/worker_test', WorkerTest)
], debug=True)