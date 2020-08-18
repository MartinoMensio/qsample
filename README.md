# QSample

QSample is a natural language processing tool for automatically
detecting quotations in text.

**Example:** In the sentence

> Witnesses said that several passengers have broken bones.

the span

> _that several passengers have broken bones_

is a quotation.

## Requirements

Java JVM (>= 1.7) and Maven (>= 3.0.0) need to be installed. All other
dependencies will be downloaded automatically. The dependencies all
together will amount to ~250 MB. The trained model files take up another
~80 MB.

## Setup

Install the tool by running the following commands (NOTE: this will trigger a
**~250 MB** Maven dependency download and will produce a .jar file of
comparable size):

    git clone https://github.com/christianscheible/qsample.git
    cd qsample
    mvn compile
    mvn package

If the build was successful, you will find two .jar files in `target/`
(with and without dependencies, respectively).

Next, download and unpack the pre-trained models (**~80 MB**):

    wget https://github.com/christianscheible/qsample/releases/download/0.1/models.tar.gz
    tar xzfv models.tar.gz

## Test

To test on the extracts from the news, run the following command after Setup:

`python3 test.py`

Then open the output, `quotes.html`, in your browser.

## Usage

Now we are ready to detect quotations. As a first step, you can run the
tool on the example documents we provide in `example/documents`. The
expected format is a directory of plain text files, each containing a
single document. To process the documents, run the following command:

    java -jar target/qsample-0.1-jar-with-dependencies.jar --sample example/documents/ output

QSample will produce several files in the output directory:

- `.log` file storing the messages that were also output to command line
- `.conf` file documenting the configuration used by the tool for this run
- one `.quotations.gz` file for each document in the input directory
  containing the detected quotations

The `.quotations.gz` files contain the predictions made by the model. As
an example, take the following snippet:

    Witnesses       230     239     O       O
    said            240     244     O       C
    that            245     249     O       B
    several         250     257     O       I
    passengers      258     268     O       I
    have            269     273     O       I
    broken          274     280     O       I
    bones           281     286     O       E
    .               286     287     O       O

The output format consists of five columns. The first column contains
the tokens; the second and third columns contains the byte begin and end
positions of the tokens in the original input file; the fourth column
contains the gold labels (if there are any); the fifth column contains
the predicted quotes. The predictions are encoded using BIOE-style
labels. The label `C` marks the occurrence of a _cue_, and all words
between the `B` (begin) and `E` (end) tag are the _content_ of the
quotation.

### Console Mode

If you run the jar file with `--console` option, QSample will run in
interactive mode, taking input from stdin and writing output to stdout.

STARTED will mark the beginning of the line where QSample starts accepting
input.

QSample will record the input until an empty line is given, and process
the input afterwards. This allows inputting multiple lines.

OUTPUT_START marks the beginning of the output

OUTPUT_END marks the end of the output

Example:
```
> STARTED
> Boris Johnson claimed that the NHS will hire 50000 new nurses
>
> OUTPUT_START
> Boris 0	5	O	O
> Johnson	6	13	O	O
> claimed	14	21	O	C
> that	22	26	O	B
> the	27	30	O	I
> NHS	31	34	O	I
> will	35	39	O	I
> hire	40	44	O	I
> 50000	45	50	O	I
> new	51	54	O	I
> nurses	55	61	O	E
> OUTPUT_END
```

## Data

This repository includes the following data:

- `example/documents`: Three news articles from WikiNews for
  testing. QSample expects one plain text document per file. You can
  mark paragraph boundaries in the text by adding an empty line after
  each paragraph. Knowledge about paragraphs is useful for detecting
  quotations. Linguistic pre-processing is performed by Stanford
  CoreNLP.
- `resources/PARC/configs`: Configuration files for running experiments
  (see below). The `acl2016*` configurations use gold pre-processing,
  whereas the `predpipeline*` configurations use CoreNLP processing. For
  each setup, we supply one file for each of the methods used in the
  paper.
- `resources/PARC/listfeatures`: Word lists for extracting features. We
  supply lists of attribution nouns and verbs, organizations and
  persons, titles, as well as a mapping of verbs to VerbNet
  classes. These lists were generated from third-party resources, see
  `licenses/LICENSE.md`.
- `resources/news.txt`: A list of WSJ ID's that contain news documents.

## Running an experiment

To run an experiment on annotated data, you need to obtain several
resources:

- Penn Attribution Relations Corpus (PARC3, http://homepages.inf.ed.ac.uk/s1052974/resources.php)
- Penn Treebank 2 (https://catalog.ldc.upenn.edu/LDC95T7)
- BBN Pronoun Coreference and Entity Type Corpus (https://catalog.ldc.upenn.edu/LDC2005T33)

Afterwards, you can run experiments based on the configuration files in
`resources/PARC/configs/`. To test the pre-trained models, you need to
adapt the paths in the configuration files. To train a model, you can
simply switch from `TEST` to `TRAIN` mode in the configuration.

## More information

For more information, refer to our paper (available at
http://www.aclweb.org/anthology/P/P16/P16-1164.pdf):

    @InProceedings{scheibleklingerpado2016,
    	author    = {Scheible, Christian and Klinger, Roman and Pad\'{o}, Sebastian},
    	title     = {Model Architectures for Quotation Detection},
    	booktitle = {Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics},
    	pages     = {1736-1745},
    	year      = {2016}
    }

or check the tool's website at
http://www.ims.uni-stuttgart.de/data/qsample for news.

## License

Please see `licenses/LICENSE.md`.
