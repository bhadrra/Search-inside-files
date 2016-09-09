# Search-inside-files
**Multithreaded, recursive text or regex search in all text-containing files in a directory (pure Python).**


## Additional features:

    - Case sensitivity
    - print results as PrettyTable
        (one table for all files or one table per file)
    - can also return the result as an OrderedDict 
    

## Usage examples: 

  - Real example of what I wanted to do when I wrote this program: 

  `python search_in_files.py "sleep" -d beloglazov-openstack-neat-a5a853a -fn *.py`

  - Other possible examples:

  `python search_in_files.py " Watson " -d sherlockHolmesBooks -fn *.txt -s`
  
  `python search_in_files.py caseSensitiveWord -C -d ../foldername -fn *.txt`
  
  `python search_in_files.py #FIXME -fn *.py`
  
  `python search_in_files.py #[A-Z]{3,5} -r -C -fn *.py`
  
  `python search_in_files.py "Hello World"`
  
## Screenshot:
![Screenshot](https://raw.githubusercontent.com/nperezzz/Search-inside-files/master/screenshot_search_in_files.PNG)
