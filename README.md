# Welcome to Accord!

## What the heck are we doing here?
The premise of Accord is pretty straightforward:
 - We provide a simple way to expose your relational database as a RESTful API.

## Can you say some more?
Sure. Accord is based on a few key principles and assumptions.
 - People need HTTP-based APIs
 - Many of these APIs are built specifically to interact with relational databases
 - Translations are odious
 - In order to maximize the utility of our data store, we need a complete language to interact with all parts of it
 - SQL is such a language
 - An isomorphic mapping between the SQL layer and the API layer gives us maximum utility of the database
 - Because the API is isomorphic to the SQL schema, it can be defined by the schema
 - Because any client that consumes the API is isomorphic to the API, it too can be defined by the schema.

 ## OK, so what are we doing?
 In it's fullest form, Accord is a set of tools that interact with database schemas and provide ready-to-use web APIs from those schemas. The APIs themselves provide out-of-the-box functionality like filtering, pre-fetching of related fields, pagination, and API specifications in OpenAPI format. The OpenAPI specs can then be used to create client code in various languages.

 ## The first pass is being written with Django
 This is because the author has pretty good experience with Django and python in general, which makes it low-hanging fruit.

 ## Are we implementing the entire SQL api in REST?
 No. We are following the JSON:API spec, which provides a subset of SQL functionality.
