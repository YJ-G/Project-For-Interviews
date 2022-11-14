# CSV Combiner

## Highlights

1. Set up a workflow that automatically triggers unit testing everytime changes are pushed to repo
2. allow users to set up logging level using command line
3. Can handle large files: read .csv files in chunks and output to .csv file/stdout in chunks to avoid OOM. 
4. Can handle more than two files, no inputs, empty files and files with different columns.

## Prerequisites

python(3.7.6)

pandas

## Get Started

```
$ python Combiner.py -f <intput files> 
```
add "-v" to see the full log
```
$ python Combiner.py -f <intput files> -v
```

An example:

```
$ python Combiner.py -f ./fixtures/accessories.csv ./fixtures/clothing.csv ./fixtures/household_cleaners.csv
```

## Testing

A python workflow is ready for automatically testing everytime changes are pushed. See Actions tab for details.

To do unit testing manually, use:

```
$ nosetests
```

Or

```
$ python -m unittest discover 
```

## Output

combined_file.csv and stdout
