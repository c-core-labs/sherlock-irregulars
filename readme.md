Irregulars: Sherlock Metadata Translation library

The Irregulars library is provided to allow for the translation of external metadata JSON to
the most recent STAC format. 
Irregulars uses the Pystac(https://github.com/stac-utils/pystac) Library to generate 
STAC Items that can be sent to a dynamic STAC API

How to Use

## STAC Adapters

The Irregulars contains a BaseSTACAdapter Class that is extended to create specific adapters for converting various metadata to STAC format.
In the /examples directory there are samples implementation of the Specific adapter classes.

The Stac Adapter consists of 4 primary portions:
- Fetching Metatdata
- Interpreting Metadata
- Generating a STAC Entry
- Pushing to Dynamic Catalog 


### Fetching Metadata

As each search api can have it's own fetching return behaviour it is necessary to create a fetch method in order to retrieve the original metadata
The retrieval of the metadata and batching of requests is handled by the `fetch_results` method and the `process_results` methods. 
`fetch_results` is responsible for the batching and sending of requests and conversion to json and the `process_results` method is responsible for yield each entry in the response.


### Interpret and Extract Attributes

The interpretation and extraction of attributes from the external metadata is done via the interpret methods within the adapter class, 
these methods return a dict object where possible so that it is easy to add any necessary constant attributes by extending the parent method. 

- `interpret_geometry` is responsible for converting the external spatial information into a org geometry.
 This geometry is then used to create the extent and geometry properties in the generated STAC item.

- `extract_required_attributes` is used to extract the following key properties from the properties of the source metadata.
 `timestamp, id, title, desc, collection, license`. 

- `extract_properties` is used to extract the medadata properties object and to ensure 
  any attributes are not duplicated in the final input.  

- `extract_source_link` generates a link back to the original metadata source

- `extract_keywords` The sherlock platform makes use of keywords assigned to any stac items.
 This can be especially useful in derived and value added products
 
#### Mapping Objects 
The Irregulars Mapping Object holds the various attribute mappings to the specific STAC relevant
properties and formats of data from the external metadata.
The Base Class also includes a series of properties for extracting properties directly 
when no extraction transformation is required

### Create STAC Item

The `create_stac_item` method is responsible for running the extraction and interpretation methods and generating a stac item using the pyStac library and returns the result as a dictionary.

### Publish to STAC API

The `publish_to_catalog` method handles committing the stac item to either a dynamic 
stac API or writing the result to file.  


##
