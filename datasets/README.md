# New File Creation: 
Dropped empty lines and lines with null values:
```bash
cat  processed_sig03.txt | grep "\S" | grep -v null > sig03.txt
cat  processed_sig05.txt | grep "\S" | grep -v null > sig05.txt
cat  processed_sig06.txt | grep "\S" | grep -v null > sig06.txt
```