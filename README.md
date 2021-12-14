# OW Gryphon
OW Gryphon is a toolbox for analytics development.

### Installing

To install OW Gryphon run the following command on the root folder of this repo. 
```bash
pip install .
```

### How to use

Once installed, you can use OW Gryphon through the command line.

#### CLI Wizard

Just type `gryphon` on the terminal and go through the steps .

```bash
gryphon
```

#### Raw CLI Samples

##### init
Initiates a new project inside the folder "sample project".
```bash
gryph init analytics sample_project
```

##### generate

Once inside a gryphon project folder generates files of a template about unsupervised learning (mlclustering).
```bash
gryph generate mlclustering sample_clustering
```

##### add
Adds and installs a required library in a project.

```bash
gryph add pandas
```

### Customizing templates

The first step towards creating or customizing templates is to set up a local template registry. 
This can be achieved by editing the OW Gryphon config file `./gryphon_commands/data/gryphon_config.json`

```json
{
    "git_registry": {
        "open-source": "https://github.com/vittorfp/template_registry.git",
        "ow-private": ""
    },
    "local_registry": {
        "default_registry": "/home/vittorfp/gryphon_registry"
    }
}
```

You can insert an entry insert the `local_registry` property, pointing to a folder in your disk. In this way:
```json
{
    "local_registry": {
        "default_registry": "/home/vittorfp/gryphon_registry",
        "new_registry": "/path/to/registry"
    }
}
```

Inside this folder you can create as many templates you want to, and the OW Gryphon will be able to find them if they have
the right folder structure and metadata files.

```

registry
    |
    |―― init
    |     |―― templates
    |     |       |―― template code
    |     |       
    |     |―― metadata.json
    |
    |―― generate
    |     |―― templates
    |     |       |―― template code
    |     |       
    |     |―― metadata.json  
```

This `metadata.json` files are required, and you can specify template pipy requirements and also replacement patterns.
Using the metadata file from the following example, OW Gryphon would install the dependencies `["scikit-learn"]` 
and ask the user for a parameter named `fileName` that will be replaced both in the contents and in the names of the 
files and folders inside the `template` folder is a sample of metadata file:

```json
{
    "arguments": [
        {
            "name": "fileName",
            "type": "str",
            "required": true,
            "help": "Name of the file that will be created."
        }
    ],
    "dependencies": ["scikit-learn"]
}
```

If you don't need any of this features, just create a `metadata.json` file with an empty json: `{}`