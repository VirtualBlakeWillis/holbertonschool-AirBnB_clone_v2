#!/usr/bin/python3
"""
something
"""
from flask import Flask, render_template
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(content):
    """ call close """
    import models
    models.storage.close()


@app.route('/states')
@app.route('/states/<id>')
def states_list(id=""):
    """ print list of states in html page """
    import models
    states = models.storage.all(models.state.State)
    found = False
    for state in states.values():
        if state.id == id:
            found = True
    if id == "":
        found = True
    return render_template("9-states.html", states=states, id=id, found=found)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
