# Search-inside-files
**Multithreaded, recursive text or regex search in all text-containing files in a directory.**


## Additional features:

* Case sensitivity
* Can search recursively in the folder or not
* Print results as PrettyTable (one table for all files or one table per file)
* Can also return the result as an OrderedDict 
    

## Usage examples: 

  - Real example of what I wanted to do when I wrote this program: 

  `python search_in_files.py "sleep" -d beloglazov-openstack-neat-a5a853a -R -fn *.py`

  - Other possible examples:

  `python search_in_files.py " Watson " -d sherlockHolmesBooks -fn *.txt -s`
  
  `python search_in_files.py caseSensitiveWord -C -d ../foldername -fn *.txt`
  
  `python search_in_files.py #FIXME -R -fn *.py`
  
  `python search_in_files.py #[A-Z]{3,5} -r -C -R -fn *.py`
  
  `python search_in_files.py "Hello World"`
  
## Screenshots:
![Screenshot 1](https://raw.githubusercontent.com/nperezzz/Search-inside-files/master/screenshot_search_in_files.PNG)

![Screenshot 2 (just for fun)](https://raw.githubusercontent.com/nperezzz/Search-inside-files/master/screenshot_search_in_files_2.PNG)
