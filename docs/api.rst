API Documentation
=================

This section describes the API routes provided by the Vocabulary Builder application. It includes details on request and response formats, authentication, and error handling.

Authentication and Authorization
--------------------------------

This module handles user authentication and JWT token management.

.. automodule:: vocabulary_builder.utils.auth
   :members:
   :private-members:
   :exclude-members: OAuth2PasswordBearerWithCookie

Translation Handling
--------------------

This module provides translation functionalities across different languages.

.. automodule:: vocabulary_builder.utils.translations
   :members:
   :private-members:

Routes for Pages
----------------

These routes render HTML pages for different parts of the application.

.. automodule:: vocabulary_builder.routes.pages
   :members:
   :private-members:

API Endpoints
-------------

This section covers the API routes for interacting with words and user data.

.. automodule:: vocabulary_builder.routes.words
   :members:
   :private-members:

.. automodule:: vocabulary_builder.routes.users
   :members:
   :private-members:

.. automodule:: vocabulary_builder.routes.auth
   :members:
   :private-members:

Custom Exceptions
-----------------

The following exceptions are used in the API to handle errors gracefully.

.. automodule:: vocabulary_builder.exceptions
   :members:
   :private-members:
