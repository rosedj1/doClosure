for name in ./*.txt
do
   echo $name
   sed -i '/^\s*$/d' $name 
   sort -n -k3 $name > tmp.txt
   mv tmp.txt $name
   cat $name
done
