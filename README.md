# gff3_parser

[github](https://github.com/McClain-Thiel/gff3_parser)

This is a simple python package to parse [gff3](http://gmod.org/wiki/GFF3) ( Generic Feature Format) 
files into pandas dataframes. This file format is used for genetic annotation files and I couldn't find a parser
that worked with python so I wrote this. This is still a work in progress and I'll hopefully be adding 
features soon. 

## Background

### What if gff3 file format?

I store this from nice explanation from [NGS Analysis](https://learn.gencore.bio.nyu.edu/ngs-file-formats/gff3-format/):

>General Feature Format (GFF) is a tab-delimited text file that holds information any and every feature that can be applied to a nucleic acid or protein sequence. Everything from CDS, microRNAs, binding domains, ORFs, and more can be handled by this format. Unfortunately there have been many variations of the original GFF format and many have since become incompatible with each other. The latest accepted format (GFF3) has attempted to address many of the issues that were missing from previous versions.  
> GFF3 has 9 required fields, though not all are utilized (either blank or a default value of ‘.’).
> 1. Sequence ID
>  2. Source  - Describes the algorithm or the procedure that generated this feature. Typically Genescane or Genebank, respectively.
>  3. Feature Type  - Describes what the feature is (mRNA, domain, exon, etc.). These terms are constrained to the [Sequence Ontology terms](http://www.sequenceontology.org/).
>  4. Feature Start
>  5. Feature End
>  6. Score  - Typically E-values for sequence similarity and P-values for predictions.
>  7. Strand (+ or -)
>  8. Phase  - Indicates where the feature begins with reference to the reading frame. The phase is one of the integers 0, 1, or 2, indicating the number of bases that should be removed from the beginning of this feature to reach the first base of the next codon.
>  9. Atributes  A semicolon-separated list of tag-value pairs, providing additional information about each feature. Some of these tags are predefined, e.g. ID, Name, Alias, Parent . You can see the full list [here](https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md).

#### Example File 

```html
##gff-version 3
#description: evidence-based annotation of the human genome (GRCh38), version 38 (Ensembl 104)
#provider: GENCODE
#contact: gencode-help@ebi.ac.uk
#format: gff3
#date: 2021-03-12
##sequence-region chr1 1 248956422
chr1	HAVANA	gene	11869	14409	.	+	.	ID=ENSG00000223972.5;gene_id=ENSG00000223972.5;gene_type=transcribed_unprocessed_pseudogene;gene_name=DDX11L1;level=2;hgnc_id=HGNC:37102;havana_gene=OTTHUMG00000000961.2
chr1	HAVANA	transcript	11869	14409	.	+	.	ID=ENST00000456328.2;Parent=ENSG00000223972.5;gene_id=ENSG00000223972.5;transcript_id=ENST00000456328.2;gene_type=transcribed_unprocessed_pseudogene;gene_name=DDX11L1;transcript_type=processed_transcript;transcript_name=DDX11L1-202;level=2;transcript_support_level=1;hgnc_id=HGNC:37102;tag=basic;havana_gene=OTTHUMG00000000961.2;havana_transcript=OTTHUMT00000362751.1
chr1	HAVANA	exon	11869	12227	.	+	.	ID=exon:ENST00000456328.2:1;Parent=ENST00000456328.2;gene_id=ENSG00000223972.5;transcript_id=ENST00000456328.2;gene_type=transcribed_unprocessed_pseudogene;gene_name=DDX11L1;transcript_type=processed_transcript;transcript_name=DDX11L1-202;exon_number=1;exon_id=ENSE00002234944.1;level=2;transcript_support_level=1;hgnc_id=HGNC:37102;tag=basic;havana_gene=OTTHUMG00000000961.2;havana_transcript=OTTHUMT00000362751.1
chr1	HAVANA	exon	12613	12721	.	+	.	ID=exon:ENST00000456328.2:2;Parent=ENST00000456328.2;gene_id=ENSG00000223972.5;transcript_id=ENST00000456328.2;gene_type=transcribed_unprocessed_pseudogene;gene_name=DDX11L1;transcript_type=processed_transcript;transcript_name=DDX11L1-202;exon_number=2;exon_id=ENSE00003582793.1;level=2;transcript_support_level=1;hgnc_id=HGNC:37102;tag=basic;havana_gene=OTTHUMG00000000961.2;havana_transcript=OTTHUMT00000362751.1
```

### Why this is super annoying to parse

Basically the first 8 columns are nicely structured tapular data but that last column has an arbitrary 
number of new values. This is kind of similar to a SQL table and a paired noSQL db but the way these
files are distributed you can't use those tools. 

### How to parse

I just found every unique key in the last column and made it it's own column and then reorganized 
data accordingly. It can be reasonably sparse and it does take a good amount of time and space 
(the files are often pretty large) but the end result is a normal structured pandas dataframe. 


## Installation

```
pip install gff3-parser
```

I'd recommend updating this often as I find and fix issues

## Example Usage

```python
>>> import gff3_parser
>>> filepath = "gencode.v38.annotation.gff3"
>>>  just_tabular = gff3_parser.parse_gff3(filepath, verbose = True, parse_attributes = False)
description: evidence-based annotation of the human genome (GRCh38), version 38 (Ensembl 104)

provider: GENCODE

contact: gencode-help@ebi.ac.uk

format: gff3

date: 2021-03-12

100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 3148167/3148167 [00:07<00:00, 421099.43it/s]

>>> just_tabular.head()
  Seqid  Source        Type  Start    End  Score Strand Phase
0  chr1  HAVANA        gene  11869  14409    NaN      +   NaN
1  chr1  HAVANA  transcript  11869  14409    NaN      +   NaN
2  chr1  HAVANA        exon  11869  12227    NaN      +   NaN
3  chr1  HAVANA        exon  12613  12721    NaN      +   NaN
4  chr1  HAVANA        exon  13221  14409    NaN      +   NaN

>>> full_data = gff3_parser.parse_gff3('gencode.v38.annotation.gff3',verbose = False,  parse_attributes=True)

>>> full_data.head()
  Seqid  Source        Type  Start    End  Score Strand Phase  seqid  ...                        ID transcript_support_level             Parent  ont       transcript_type    tag       havana_transcript transcript_name ccdsid
0  chr1  HAVANA        gene  11869  14409    NaN      +   NaN    NaN  ...         ENSG00000223972.5                      NaN                NaN  NaN                   NaN    NaN                     NaN             NaN    NaN
1  chr1  HAVANA  transcript  11869  14409    NaN      +   NaN    NaN  ...         ENST00000456328.2                        1  ENSG00000223972.5  NaN  processed_transcript  basic  OTTHUMT00000362751.1\n     DDX11L1-202    NaN
2  chr1  HAVANA        exon  11869  12227    NaN      +   NaN    NaN  ...  exon:ENST00000456328.2:1                        1  ENST00000456328.2  NaN  processed_transcript  basic  OTTHUMT00000362751.1\n     DDX11L1-202    NaN
3  chr1  HAVANA        exon  12613  12721    NaN      +   NaN    NaN  ...  exon:ENST00000456328.2:2                        1  ENST00000456328.2  NaN  processed_transcript  basic  OTTHUMT00000362751.1\n     DDX11L1-202    NaN
4  chr1  HAVANA        exon  13221  14409    NaN      +   NaN    NaN  ...  exon:ENST00000456328.2:3                        1  ENST00000456328.2  NaN  processed_transcript  basic  OTTHUMT00000362751.1\n     DDX11L1-202    NaN

>>> full_data.columns
Index(['Seqid', 'Source', 'Type', 'Start', 'End', 'Score', 'Strand', 'Phase',
       'seqid', 'transcript_id', 'havana_gene', 'gene_type', 'gene_name',
       'gene_id', 'exon_id', 'level', 'protein_id', 'hgnc_id', 'exon_number',
       'ID', 'transcript_support_level', 'Parent', 'ont', 'transcript_type',
       'tag', 'havana_transcript', 'transcript_name', 'ccdsid'],
      dtype='object')


```

## Full Documentation 

This whole project has literally one public function so far so I'm just going to document it here until
I feel like it needs more.

Ill get around to it eventually. Theres only two uses and both are in the example. 



