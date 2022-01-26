# Developer docs

This documentation aims to give insight about the development process and project structure.

### Templates
One of Gryphon's main functionality is to handle project templates. 
In this way, we need to define a pattern according to which we will structure our templates.

#### Folder structure
First concern about the templates are the folder structure. 
This folder structure consists of a sub-folder called 
`template` and a file called `metadata.json`
that is used to specify information about the template.

```
template_name
    |―― template
    |   |―― "all the code from the template"
    |―― metadata.json
```

The template name is given by the folder name.

#### Templates metadata.json
The `metadata.json` file can/should contain the following fields:

- `display_name`: An alternative well formatted name. The way that the template will 
be shown on the gryphon interface.
- `dependencies`: Should be a list of strings containing the name of any needed 
python library. They will be installed along with the console.


Generate exclusive ones (smaller usage types)
- `arguments`: In this field the template developer can specify extra parameters to be asked 
for the user and used in the template rendering (ask a parameter and replace the value inside the files).
The data structure is a list of objects with the following properties.
    - `name`: Name of the field. 
    - `type`: Field data type. Should be one of ["string", "int"]
    - `required`: Boolean field saying whether it is a required argument or not.  
    - `help`: String containing a short description of the field. It will be displayed to the user to help in the argument filling.


- `description`: Small string description about the template. It shall be displayed after template selection.
- `methodology`: List of strings containing the methodologies applied to the template. The user may filter by methodologies in the menu navigation.
- `topic`: List of strings containing relevant topics related to the template. The user may filter by topics in the menu navigation.
- `sector`: List of strings containing relevant sectors in which the template might be applied to. The user may filter by sector in the menu navigation.
- `keywords`: List of strings containing generic keywords describing the template. The user may search by some keyword. 

#### Template registries

Template registries are a collection of templates that are stored in a particular structure so that gryphon can 
understand it properly. 

We must have two folders `init` and `generate` to distinguish between
the project templates and the snippets ones. The templates should be placed inside this two folders. Refer to the f

```
registry
    |
    |―― init
    |     |―― sample_template
    |          |―― metadata.json  
    |          |―― template
    |                 |―― template code
    |
    |―― generate
    |     |―― sample_template
    |          |―― metadata.json  
    |          |―― template
    |                 |―― template code
```


### General behavior
In this section we will give an overview of the inner workings of gryphon, from the beginning to the halt. 

#### Template fetching 
At the time gryphon is started, the first thing that happens is the template fetching. It consists of getting updated versions from 
the templates, which can come both from git remote repos or from local folders.

It copies the specified folders and git repos to the site-packages folder,
overwriting the existing folders inside the `{...}/site-packages/gryphon/data/template_registry`. 

(see `gryphon_config.json` explanation for further details).

#### Navigation
When gryphon is started and the navigation starts with the first 5 options:
- `Start a new Gryphon project`: Option to navigate in the project templates and to create a new project based on then.
- `Load template code into an existing Gryphon project`: Option to navigate in the snippet templates and to render then inside the current project.
- `Install Python libraries/packages`: Option to navigate into the available lib categories and to install them. 
- `About OW Gryphon`: Shows some information about Gryphon and the persons in charge of it.
- `Exit`: Exit the program.

#### Configuration files 
In order to coordinate gryphon's workings and parameterize some behaviors, some configuration files are necessary. In this session we give more insight about the 

##### gryphon_config.json
This file is the general gryphon configuration file. It, so far, enables the developers and/or heavy users to configure some parameters:
- `git_registry`: It specifies a set of git repositories from whose gryphon will pull It's template registries; 
- `local_registry`: It specifies a set of local folders from whose gryphon will copy template registries from; 

In the following example gryphon would get its templates from 3 different sources,
being 2 git repositories and 1 local folder.

```json
{
    "git_registry": {
        "open-source": "https://github.com/vittorfp/template_registry.git",
        "ow-private": "https://github.com/vittorfp/ow_registry.git"
    },
    "local_registry": {
        "default_registry": "/home/vittorfp/labskit_registry"
    }
}
```

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
                    {}
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

The category_tree file contains the tree structure of the 
 template rendering feature (generate). It describes a tree of navigation
that contains some predefined nodes, such as `Methodology`, `Search by topic` and `Search by sector`.
These nodes are related to specific behaviors in the navigation, therefore any changes in 
the actual structure may influence in the overall rules and might require code changes.

###### library_tree.json
This file is meant to set the hierarchical layers through the library installation menu. Here, the regular nodes are categories while leaf nodes are libraries which the user can install. 
In the following example the `"Data Visualization"` is a category and `"matplotlib"` is a library users can install.
```json
[
	{
		"name": "Data Visualization",
		"children": [
			{
				"name": "matplotlib",
				"short_description": "Fundamental library of data visualization in python.",
				"long_description": "Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python. Matplotlib makes easy things easy and hard things possible.\n\n\t- Create publication quality plots.\n\t- Make interactive figures that can zoom, pan, update.\n\t- Customize visual style and layout.\n\t- Export to many file formats.\n\t- Embed in JupyterLab and Graphical User Interfaces.\n\t- Use a rich array of third-party packages built on Matplotlib.",
				"reference_link": "https://matplotlib.org/"
			}
		]
	}
]
```
The leaf nodes, are expected to have the following fields: 
- `short_description`: This is a short description with at most 50 chars, that will be shown in the selection menu side-by-side with the name;
- `long_description`: This is a more complete description that will be shown in the time that the user clicks in a specific library;
- `reference_link`: Link to the library reference, will be shown together with the long description;

##### links_about.json
This config file specifies reference links that will be shown in the "About" section in the menu. 

The semantics of the file is very simple, it is just a list of objects containing the link and display name:
```json
[
    {
        "title": "Google",
        "value": "https://www.google.com/"
    },
    {
        "title": "Yahoo",
        "value": "https://www.yahoo.com/"
    },
    {
        "title": "YouTube",
        "value": "https://www.youtube.com/"
    }
]

```