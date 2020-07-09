echo $0
for file in *;
do
   # if file is script then continue
   if [ ./$file == $0 ]
   then
      continue
   fi
	echo $file
done
