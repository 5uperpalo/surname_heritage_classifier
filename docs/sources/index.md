# SUrname HEritage Classifier

A hobby project to classify surnames to countries and areas of the world. An attempt for an open source alternative to paid services:

* https://nationalize.io/our-data
* https://namsor.app/
* https://forebears.io/onograph/
* https://census.name/
    * ~1000e for their database

used data:

* [data/name_dataset](https://github.com/philipperemy/name-dataset?tab=readme-ov-file#full-dataset)
    * [google drive link](https://drive.google.com/file/d/1QDbtPWGQypYxiS4pC_hHBBtbRHk9gEtr/view?usp=sharing)
* [data/annotated_names_NamePrism.tsv](https://github.com/greenelab/wiki-nationality-estimate)
* [kaggle surname-dataset-classification](https://www.kaggle.com/datasets/alenic/surname-dataset-classification)
    * [data/surname-nationality.csv](https://huggingface.co/datasets/Hobson/surname-nationality/tree/main)
    * [data/surnames_with_splits.csv](https://huggingface.co/datasets/NavidVafaei/surnames/tree/main)
* [data/final_all_names_code.csv](https://www.kaggle.com/datasets/amaleshvemula7/name-and-country-of-origin-dataset?resource=download)
* [data/name2lang.txt](https://www.kaggle.com/datasets/rp1985/name2lang/data)

aggregated data:

* [supercom storage](https://supercom.cttc.es/index.php/supercom-solutions/dataset-storage)

code based on:

* https://www.kaggle.com/code/yonatankpl/surname-classification-with-bert

other ideas:

* query names and origin countries somehow from wiki https://opendata.stackexchange.com/a/13199
    * maybe somehow get more surnames from here: https://en.wiktionary.org/wiki/Appendix:Names
* rerun data gathering from [wiki-nationality-estimate](https://github.com/greenelab/wiki-nationality-estimate)
