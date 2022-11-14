#!/usr/bin/python3
"""
something
"""
from flask import Flask, render_template
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown.appcontext
def teardown():
    """ call close """
    import models
    models.storage.close()


@app.route('/states_list')
def states_list():
    """ print list of states in html page """
    import models
    states = models.storage.all(models.state.State)
    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
