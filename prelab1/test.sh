#!/bin/bash

# loop files in current directory
for file in *;
do
	# if file is script then continue
	if [ ./$file == $0 ]
   then
      continue
   fi
	# declare int counter
	declare -i counter=1
	# loop lines in file
	while IFS= read -r line
	do 
		echo $file
		isEven=$(expr $counter % 2)
		# check if odd
		if [ $isEven != 0 ]
		then
			echo "$file: $line"
		fi
		# increment counter
		counter=$((counter+1))
	done
done
