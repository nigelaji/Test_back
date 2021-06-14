from flask_restful.reqparse import Argument, RequestParser
from flask import request, current_app
from werkzeug import exceptions
from tp_app.handler.http_handler import self_abort
import six


# class SelfArgument(Argument):
#
#     def handle_validation_error(self, error, bundle_errors):
#         """Called when an error is raised while parsing. Aborts the request
#         with a 400 status and an error message
#
#         :param error: the error that was raised
#         :param bundle_errors: do not abort when first error occurs, return a
#             dict with the name of the argument and the error message to be
#             bundled
#         """
#         error_str = six.text_type(error)
#         error_msg = self.help.format(error_msg=error_str) if self.help else error_str
#         msg = f"{self.name} {error_msg}"
#
#         if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
#             return error, msg
#         self_abort(400, msg)


class SelfRequestParser(RequestParser):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(self, *args, **kwargs)
    #     self.argument_class = SelfArgument

    def parse_args(self, req=None, strict=True, http_error_code=400, errors_dict=None):
        """Parse all arguments from the provided request and return the results
        as a Namespace

        :param req: Can be used to overwrite request from Flask
        :param strict: if req includes args not in parser, throw 400 BadRequest exception
        :param http_error_code: use custom error code for `flask_restful.abort()`
        """
        if req is None:
            req = request

        namespace = self.namespace_class()

        # A record of arguments not yet parsed; as each is found
        # among self.args, it will be popped out
        req.unparsed_arguments = dict(self.argument_class('').source(req)) if strict else {}
        print(req.unparsed_arguments)
        errors = {}

        for arg in self.args:
            value, found = arg.parse(req, self.bundle_errors)

            if isinstance(value, ValueError):
                errors.update(found)
                found = None
            if isinstance(value, TypeError):
                errors.update({arg.name: value})
            if found or arg.store_missing:
                namespace[arg.dest or arg.name] = value
        if errors:
            errors_dict = errors_dict or {}
            for field, error in errors.items():
                error_code = errors_dict.get(field, {'code': 404}).get('code')
                self_abort(error_code, "{field} {error}".format(field=field, error=error))

        if strict and req.unparsed_arguments:
            raise exceptions.BadRequest('Unknown arguments: %s'
                                        % ', '.join(req.unparsed_arguments.keys()))

        return namespace
