#Edbel Basaldua
#Filename: script.sh
# Assignment:Lab1 
#Description: Returns the entire set of even lines wihtin 
# a file and echos them on the CLI or terminal
#!/bin/bash

#Follows the format
# awk 'pattern {action}' in file > out file or cli args(*)
awk 'NR %2 ==0 {print FILENAME ":",$0 }' * 
