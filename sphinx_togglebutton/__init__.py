"""A small sphinx extension to add "toggle" buttons to items."""
import os
from docutils.parsers.rst import Directive, directives
from docutils import nodes

__version__ = "0.0.3dev0"


def st_static_path(app):
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "_static"))
    app.config.html_static_path.append(static_path)


def add_to_context(app, config):
    # Update the global context
    config.html_context.update({"togglebutton_hint": config.togglebutton_hint})


# This function reads in a variable and inserts it into JavaScript
def insert_custom_selection_config(app):
    # This is a configuration that you've specified for users in `conf.py`
    selector = app.config["togglebutton_selector"]
    js_text = "var togglebuttonSelector = '%s';" % selector
    app.add_js_file(None, body=js_text)


class Toggle(Directive):
    """Hide a block of markup text by wrapping it in a container."""

    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True

    option_spec = {"id": directives.unchanged, "show": directives.flag}

    def run(self):
        self.assert_has_content()
        classes = ["toggle"]
        if "show" in self.options:
            classes.append("toggle-shown")

        if len(self.arguments) == 0:
            parent = nodes.container(classes=classes)
            self.state.nested_parse(self.content, self.content_offset, parent)
        else:
            parent = nodes.admonition(classes=["toggle-body"])
            title = nodes.title(self.arguments[0], self.arguments[0])
            body = nodes.container(classes=classes)
            self.state.nested_parse(self.content, self.content_offset, body)
            parent += title
            parent += body
        return [parent]


# We connect this function to the step after the builder is initialized
def setup(app):
    # Add our static path
    app.connect("builder-inited", st_static_path)

    # Add relevant code to headers
    app.add_css_file("togglebutton.css")

    # Add the string we'll use to select items in the JS
    # Tell Sphinx about this configuration variable
    app.add_config_value("togglebutton_selector", ".toggle", "html")
    app.add_config_value("togglebutton_hint", "Click to show", "html")
    app.add_js_file("togglebutton.js")

    # Run the function after the builder is initialized
    app.connect("builder-inited", insert_custom_selection_config)
    app.connect("config-inited", add_to_context)
    app.add_directive("toggle", Toggle)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
