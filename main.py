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

class MainHandler(webapp2.RequestHandler):
    def get(self):

        content="""
                    <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="">
                        <span class="error"></span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
        """
        self.response.write(content)

    def post(self):

        username=self.request.get("username")
        check_password=self.request.get("password")
        ver_password=self.request.get("verify")

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        PASS_RE = re.compile(r"^.{3,20}$")

        def valid_username(username):
            return USER_RE.match(username)

        def valid_password(check_password):
            return PASS_RE.match(check_password)

        if not PASS_RE.match(check_password):
            invalid_password="<span style = 'color:red'>Not valid password</span>"
        else:
            invalid_password=""

        if not USER_RE.match(username):
            name_error="<span style = 'color:red'>Not valid username</span>"
        else:
            name_error=""

        if check_password != ver_password:
            password_error="<span style ='color:red'>Passwords do not match</span>"
        else:
            password_error=""

        if invalid_password=="" and name_error=="" and password_error=="":
            self.redirect("/welcome?username="+username)



        error_form="""
            <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="""+cgi.escape(username)+""" required>
                        <span class="error">%s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error">%s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required>
                        <span class="error">%s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="">
                        <span class="error"></span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>"""%(name_error,invalid_password, password_error)
        self.response.write(error_form)


class WelcomeHandler(webapp2.RequestHandler):

    def get(self):
        username = self.request.get("username")
        self.response.write("<h1>Welcome "+username+"</h1>")



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
