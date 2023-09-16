
# Data of Migros Products for Hack Zurich

This folders contains data of Migros Products in JSON format.
The files can be found in `./products` and each file represents the data for one product.
The filename is the ID of the product.

## Model Structure

The structure of the JSON in each file is defined in `openapi.yaml` as an [OpenAPI](https://www.openapis.org/) specification.
You can visualize this file on https://editor.swagger.io/ if you like.

Not every product has all the fields described in the specification.
There might also be fields in the specification which no product has set.

## Usage

You can use this data by e.g. importing it into a database or document storage.

