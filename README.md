#PlasmidTron
You have a set of samples where you have a known phenotype, and a set of controls. PlasmidTron lets you assemble the differences between the two so that you can gain a better understanding of the phenotype and the other sequences around it (the rest of the plasmid).  For example, often researchers will just look for an anti-microbial resistance gene, and look no further, because its still a difficult problem. PlasmidTron can let you see the sequence around your gene, giving you greater biological insights into the mechanisms of the resistance. Whilst its primary purpose is to pull out plasmids, phage can also be recovered.

[![Build Status](https://travis-ci.org/sanger-pathogens/plasmidtron.svg?branch=master)](https://travis-ci.org/sanger-pathogens/plasmidtron)

#Usage
```
usage: plasmidtron [options] output_directory file_of_trait_fastqs file_of_nontrait_fastqs

A tool to assemble parts of a genome responsible for a trait

positional arguments:
  output_directory      Output directory
  file_of_trait_fastqs  File of filenames of trait (case) FASTQs
  file_of_nontrait_fastqs
                        File of filenames of nontrait (control) FASTQs

optional arguments:
  -h, --help            show this help message and exit
  --action {intersection,union}, -a {intersection,union}
                        Control how the traits kmers are filtered for assembly
                        [union]
  --kmer KMER, -k KMER  Kmer to use, depends on read length [51]
  --min_contig_len MIN_CONTIG_LEN, -l MIN_CONTIG_LEN
                        Minimum contig length in final assembly [1000]
  --min_kmers_threshold MIN_KMERS_THRESHOLD, -m MIN_KMERS_THRESHOLD
                        Exclude k-mers occurring less than this [25]
  --max_kmers_threshold MAX_KMERS_THRESHOLD, -x MAX_KMERS_THRESHOLD
                        Exclude k-mers occurring more than this [254]
  --threads THREADS, -t THREADS
                        Number of threads [1]
  --spades_exec SPADES_EXEC, -s SPADES_EXEC
                        Set the SPAdes executable [spades.py]
  --verbose, -v         Turn on debugging [0]
  --version             show program's version number and exit
```

##Input parameters
The following parameters change the results:

__action__: There are two fundamental methods of operation. The default is 'union', where kmers which occur in ANY trait sample, but are absent from the nontrait samples, get used to filter the reads. So in effect you are assembling the whole accessory genome of the trait samples. This leads to larger end assemblies and more false positives, but will capture greater regions of the accessory genome. It is tolerant to situations where you have a plasmid which can vary substantially with different backbones or payloads.  The next is 'intersection', where kmers must occur in ALL trait samples and not in the nontrait samples. This leads to smaller end assemblies and more fragmentation, with less false positives.  It is less tolerant to variation. 

__kmer__: Choosing a kmer is not an exact science, and have greatly influence the final results. This kmer size is used by KMC for counting and filtering, and by SPAdes for assembly.  Ideally it should be between about 50-90% of the read length, should be an odd number and between 21 and 127 (SPAdes restriction).  If choose a kmer which is too small, you will get a lot more false positives. If you choose a kmer too big, you will use a lot more RAM and potentially get too little data returned. Quite often with Illumina data the beginning and end of the reads have higher sequencing error rates. Ideally you want a kmer size which sits nicely inside the good cycles of the read. Trimming with Trimmomatic can help if the quality collapses quite badly at the end of the read.

__min_contig_len__: This needs to be a minimum of twice the mean fragment size (insert size) of your library to reduce the impact of false positives. For example if you have a single kmer which randomly occurs in the genome, using it will then allow for reads upstream and downstream, plus their mates, to be assembled. This variable can control this noise, and inpractice you will want to set this a fair bit higher, perhaps 6 times the fragment size. Setting this too high will lead to valuable information being lost (e.g. small plasmids).

__min_kmers_threshold__: This value lets you set a minimum threshold for the occurance of a kmer. Ideally you need about 30X depth of coverage to perform de novo assembly. This value default to 25, so excluding kmers below this level eliminates kmers where you wont get a good assembly, thus reducing false positives. The maximum value is 254, but the results poor.

__max_kmers_threshold__: This value lets you set a maximum threshold for the occurance of a kmer. The occurance of kmers forms a Poisson distribution, with a very long tail. With KMC, there is a catchall bin for occurances of 255 and greater (so 255 is the maximum value). By default it is set to 254 which excludes this catchall bin for kmers, and thus the long tail of very common kmers. This reduces the false positives. You need to be careful when setting this lower because you could exclude all of the interesting kmers.

__min_spades_contig_coverage__: Filter out contigs with less than this coverage in the SPAdes assemblies. This gets applied at the end of each SPAdes assembly, and filters out some of the noise. If your input data is lower coverage you may need to reduce this value but the defaults are sensible.

The following parameters have no impact on the results:

__threads__: This sets the number of threads available to KMC and SPAdes. It should never be more than the number of CPUs available on the server. If you use a compute cluster, make sure to request the same number of threads on a single server. It defaults to 1 and you will get a reasonable speed increase by adding a few CPUs, but the benefit tails off quite rapidly since the I/O becomes the limiting factor (speed of reading files from a disk or network).

__spades_exec__: By default SPAdes is assumed to be in your PATH and called spades.py. You can set this to point to a different executable, which might be required if you have multiple versions of SPAdes installed.

__verbose__: By default the output is limited and all intermediate files are deleted. Setting this flag allows you output more details of the software as it runs and it keeps the intermediate files.

##Required resources
###RAM (memory)
The largest consumer of RAM (memory) is SPAdes. Assembling a whole bacteria takes approximately 4GB of RAM. If the filtering allows everything through then this worst case will occur, but generally less than 1GB of RAM is required. Poor quality sequencing data will increase the amount of RAM required. In this instance running Trimmomatic first will help greatly.

###Disk space
By default all of the intermediate files are cleaned up at the end, so the overall disk space usage is quite low. As an example, an input of 800 Mbytes of compressed reads created 40 Mbytes of output data at the end. While the algorithm is running the disk usage will never exceed the size of the input reads. The intermediate files can be kept if you use the 'verbose' option. 

#Outputs 
For every trait sample you will get an assembly of nucleotide sequences in FASTA format. These are scaffolded by SPAdes and have small sequences filtered out. You will also get a text file describing the process, with versions of software, parameters used and references.

#Installation
There are a number of installation methods. Choosing the right one for the system you use will simpliy the process.

* Linux 
  * Debian Testing/Ubuntu 16.04 (Xenial)
  * Ubuntu 14.04 (Trusty)
  * Ubuntu 12.04 (Precise)
  * LinuxBrew
* OSX
  * HomeBrew
* Linux/OSX/Windows/Cloud
  * Docker

##Linux
The instructions for Linux assume you have root (sudo) on your machine.

###Debian Testing/Ubuntu 16.04 (Xenial)

```
apt-get update -qq
apt-get install -y kmc git python3 python3-setuptools python3-biopython python3-pip
pip3 install git+git://github.com/sanger-pathogens/plasmidtron.git
```

###Ubuntu 14.04 (Trusty)
You can either manually install [KMC](http://sun.aei.polsl.pl/REFRESH/index.php?page=projects&project=kmc&subpage=about) and [SPAdes](http://bioinf.spbau.ru/spades), or use the install_dependancies script (you will need to add some paths to your PATH environment variable).

```
apt-get update -qq
apt-get install -y wget git python3 python3-setuptools python3-biopython python3-pip
wget https://raw.githubusercontent.com/sanger-pathogens/plasmidtron/master/install_dependancies.sh
source ./install_dependancies.sh
pip3 install git+git://github.com/sanger-pathogens/plasmidtron.git
```

###Ubuntu 12.04 (Precise)
PlasmidTron uses BioPython, however the version of Python3 bundled with Precise is too old, so you will have to manually install Python3 (3.3+) along with pip3.
Once you have done this you can proceed with the instructions below. You can either manually install [KMC](http://sun.aei.polsl.pl/REFRESH/index.php?page=projects&project=kmc&subpage=about) and [SPAdes](http://bioinf.spbau.ru/spades), or use the install_dependancies script (you will need to add some paths to your PATH environment variable).

```
apt-get update -qq
apt-get install -y git wget
wget https://raw.githubusercontent.com/sanger-pathogens/plasmidtron/master/install_dependancies.sh
source ./install_dependancies.sh
pip3 install git+git://github.com/sanger-pathogens/plasmidtron.git
```

###Linuxbrew
These instructions are untested. First install [LinuxBrew](http://linuxbrew.sh/), then follow the instructions below.

```
brew tap homebrew/science
brew update
brew install python3 kmc spades
pip3 install git+git://github.com/sanger-pathogens/plasmidtron.git
```

##OSX
###Homebrew
These instructions are untested. First install [HomeBrew](http://brew.sh/), then follow the instructions below.

```
brew tap homebrew/science
brew update
brew install python3 kmc spades
pip3 install git+git://github.com/sanger-pathogens/plasmidtron.git
```

#Linux/OSX/Windows/Cloud
##Docker 
Install [Docker](https://www.docker.com/).  We have a docker container which gets automatically built from the latest version of PlasmidTron. To install it:

```
docker pull sangerpathogens/plasmidtron
```

To use it you would use a command such as this (substituting in your directories), where your files are assumed to be stored in /home/ubuntu/data:
```
docker run --rm -it -v /home/ubuntu/data:/data sangerpathogens/plasmidtron plasmidtron output traits.csv nontraits.csv
```
