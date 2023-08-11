# PKLX: The Popper Knowledge Language Experiment

The Popper Knowledge Language is an experiment to formalize knowledge. It allows you to generate [knowledge graphs](https://en.wikipedia.org/wiki/Knowledge_graph) using a syntax that can be embedded in simple text. In the future it will also allow you to manipulate and maintain such knowledge graphs via simple interfaces.

At the moment it is not obvious how it relates to standard knowledge representation frameworks like [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework), [OWL](https://en.wikipedia.org/wiki/Web_Ontology_Language). The goal of this project is to explore the space of knowledge representation and to represent knowledge in a way that is easy to understand and easy to use.

## Installation

### From PyPI

    pip install pklx

### Development mode

    virtualenv ve
    source ve/bin/activate
    git clone https://github.com/PhylomatX/PKLX.git PKLX
    cd PKLX
    pip install -r requirements.txt
    pip install -e .

## Usage

The goal of the following is to create a (very) small knowledge graph for the Solar System.

At first you need to create a folder for your knowledge files (simple text or markdown files in which you will embed the PKLX syntax). This could be a folder specifically for this purpose or e.g. an [Obsidian](https://obsidian.md/) vault.

    mkdir data

Next, you need to specify the location of the data folder in the settings file. You can do this by running the following command:

    pklx-set-settings FOLDER_PATH <absolute_path_of_data_folder>

Instead of using these commands you can also import the respective functions from the pklx package, please see the `manage.py` file to understand these functions. The next step is to define your own ontology. An ontology is a set of relations that you want to use. You can do this by creating a file called `.ontology` in the data folder. 

    cd data
    touch .ontology

The file should contain one relation per line followed by an explanation separated by the delimiter (default: `-/`, you can change this via pklx-set-settings DELIMITER your_delimiter). For example:

    IS PART OF -/ A binary relation that holds between two objects if the first object is part of the second object.
    HAS PROPERTY -/ A binary relation that holds between an object and a property if the object has the property.

The next step is to use PKLX to create some knowledge triplets. The PKLX syntax can be embedded in markdown or text files within normal sentences, similar to inline LaTeX. You can create text or markdown files in the data folder and use PKLX in them. 

    touch knowledge.txt

The PKLX syntax needs to be surrounded by the delimiter (default: `-/`) and must follow the grammar shown in the grammar section. For example you could express some knowledge by writing:

    -/ Earth IS PART OF Solar System -/
    -/ Earth HAS PROPERTY Mass -/
    -/ Earth HAS PROPERTY Radius -/

Here, you would be using the relations that you defined in the .ontology file to connect two variables (i.e. `Earth` and `Solar System`). You can also embed the PKLX statements in normal text:

    The Earth is part of the Solar System. (-/ Earth IS PART OF Solar System -/) It has a mass (-/ Earth HAS PROPERTY Mass -/) of 5.972 × 10^24 kg and a radius (-/ Earth HAS PROPERTY Radius -/) of 6371 km.

You can also make use of the markdown syntax by using `[[` and `]]` which is especially useful in Obsidian for finding existing variables and relations. For example:

    -/ [[Earth]] [[IS PART OF]] [[Solar System]] -/

To view existing knowledge you can run the following command:

    pklx-view

This will open a web browser in which all knowledge triplets are visualized in a graph. You can use the search field at the top left to find knowledge triplets for a specific variable (e.g. `Earth` or `Solar System`).

You can also collect all knowledge triplets for a specific variable by running the following command:

    pklx-collect Earth

The grammar also allows more complex statements. For example, you can define conditional statements (this must be explained in your ontology) by expanding your ontology and making use of the grammar shown below:

    .ontology
        ONLY IF -/ A conditional binary relation where the left hand side is only true if the right hand side is true.

    knowledge.txt
        -/ My Triplet = Europe HAS PROPERTY Winter -/
        -/ My Triplet ONLY IF Australia HAS PROPERTY Summer -/ 

Here, you assign a knowledge triplet to the variable `My Triplet` and use it in another knowledge triplet to avoid complex structures. This is equivalent to the following syntax:

    -/ ( Europe HAS PROPERTY Winter ) ONLY IF ( Australia HAS PROPERTY Summer ) -/

When you now run

    pklx-collect Europe

you will see, that the collected statements also include the statements containing `My Triplet`.

## Grammar

    <pklx>
        <stmt>
        <knowld>

    <stmt>
        <name> = <knowld>

    <knowld>
        <expr> <binop> <expr>
        <unop> <expr>

    <expr>
        <name>
        ( <knowld> )
        
    <binop>
        ( [[ )? letter ( letter | digit | space )* ( ]] )?

    <unop>
        ( [[ )? letter ( letter | digit | space )* ( ]] )?

    <name>
        ( [[ )? letter ( letter | digit | space )* ( ]] )?

    letter
        a, ..., z, A, ..., Z

    digit
        0, ..., 9

## Vision

At the moment, PKLX is a simple experiment without much functionality. However, I have been using a more sophisticated version of PKLX (even more experimental which is why I don't want to publish it at the moment) for my personal research and note taking activities for a while now. I have found it to be very useful and satisfying for structuring my own understanding of certain topics.

I could envision PKLX to be used in a variety of ways:

-   Researchers mainly use PKLX to publish their research findings into a global knowledge graph. They would still use traditional publication formats (e.g. PDF) but maybe only in limited form as it is much easier to request knowledge from a knowledge base instead of reading through lengthy papers.

-   A teacher expresses knowledge about a topic in PKLX syntax and thus generates a knowledge graph. This graph can then be compared with students' knowledge graphs to identify gaps in their understanding or could help them understand the topic better.

At the moment, these applications are still very far away. In addition it is currently not clear to me how PKLX relates to existing knowledge graph technologies such as RDF and OWL and there might be a large overlap between a future final version of PKLX and these technologies. However, I believe that PKLX would be easier to start with and maybe there could even be some kind of merger between all of them in the future. 

## Contributing

Contributions and any kind of feedback are very welcome, please see the TODO list below. Please open an issue or pull request if you have any ideas or suggestions. You can also contact me directly via email (see my website [phylomatx.com](https://phylomatx.com) for details).

If you are trying to understand the code, I recommend starting with the lexer function in parser.py and then pairing each object in objects.py with the corresponding grammar rule in the grammar section above.

## TODO
-   Add documentation
-   Add tests and improve error handling
-   Extend the PKLX grammar to allow for more complex graph structures
-   Add functionality to analyze created knowledge graphs (e.g. via [graph networks](https://distill.pub/2021/gnn-intro/])
-   Research and understand similarities and differences between PKLX and e.g. RDF and OWL

## Development commands

### build process

    python -m build

Upload and download via testpypi:

    python -m twine upload --repository testpypi dist/*
    python -m pip install --index-url https://test.pypi.org/simple/ --no-deps pklx

Upload and download via pypi:

    python -m twine upload dist/*
    python -m pip install pklx


See https://packaging.python.org/en/latest/tutorials/packaging-projects/ for more information.
