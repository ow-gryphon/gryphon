# Developer docs

This documentation aims to give insight about the development process and project structure.


## Topics
### Folder structure
### Templates metadata.json file structure
### General behavior
#### Template fetching 
#### Navigation
#### Configuration files 
##### gryphon_config.json
##### Tree files
The tree files are a specially formatted json files to describe a tree structure. 
The semantics of the fields are simple, and can be described in terms of 2 fields, "name" and "children".
Example of tree file:

```json
[
    {
        "name": "A sample node",
        "children": [
            {
                "name": "A sample leaf node (I don't have a \"children\" property)"
            },
            {
                "name": "A sample regular node (I DO have a \"children\" property)",
                "children": [
                    {
                        "name": "Leaf node",
                        "sample_property": "I can have any coustom property I need. (It just can't be named \"children\" or \"name\")"
                    }, 
                    {...}
                ]
            }
        ]
    },
	{
        "name": "I am another sample node (but I don't have children)"
    }
]

```
The `"name"` property designates the node name. It's data type is "string".

The `"children"` property designates the children nodes from a node. It's data type is "list" and It's elements canbe anoter node (with the same minimal "name" and "children" properties).

Quite simple, no?

You can even add extra properties for each node, with just one restriction: they can't be named You can even add extra properties for each node, with just one restriction: they can't be named `"name"` or `"children"`, these are reserved words.
Use it to suit your business needs.

###### category_tree.json
###### library_tree.json
##### links_about.json
