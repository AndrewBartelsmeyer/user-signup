#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PW_RE = re.compile(r"^.{3,20}$")
def valid_password(username):
    return PW_RE.match(username)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(username):
    return EMAIL_RE.match(username)

def build_page(username, user_err, email, email_err, password_err):

    header = "<h1>User signup</h1>"
    user_label = "<label>Username:</label>"
    user_input = "<input type='text' name='username' value = '" + cgi.escape(username, quote=True) + "'/>"

    email_label = "<label>Email:</label>"
    email_input = "<input type='text' name='email' value = '" + cgi.escape(email, quote=True) + "'/>"

    password_label = "<label>Password:</label>"
    password_input = "<input type='text' name='password'/>"

    verify_label = "<label>Verify password:</label>"
    verify_input = "<input type='text' name='verify'/>"

    submit = "<input type = 'submit'/>"
    form = ("<form method = 'post'>" +
        user_label + user_input + user_err + "<br>" +
        email_label + email_input + email_err + "<br>" +
        password_label + password_input + password_err + "<br>" +
        verify_label + verify_input + "<br>" +
        submit + "</form>")

    return header + form


class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = build_page("","","","","")
        self.response.write(content)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        email = self.request.get("email")
        verify = self.request.get("verify")

        user_err = ""
        password_err = ""
        email_err = ""
        bError = False

        if not valid_username(username):
            user_err = "Username must be 3-20 characters in length, with no special characters other than '_'"
            bError = True
        if not valid_password(password):
            password_err = "Password must be 3-20 characters in length."
            bError = True
        if password != verify:
            password_err = "Passwords do not match!"
            bError = True
        if not valid_email(email) and len(email) > 0:
            email_err = "Invalid email address, please enter a valid email address."
            bError = True

        if bError:
            content = build_page(username, user_err, email, email_err, password_err)
            self.response.write(content)
        else:
            username = cgi.escape(username, quote=True)
            self.redirect('/welcome?username='+username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        content = "<p> Welcome, " + cgi.escape(username, quote=True) + "!</p>"
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
