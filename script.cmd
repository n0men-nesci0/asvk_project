for /l %%x in (1, 1, 50) do (
   py main.py -i test32.xml >>log_test32_base.txt
)
echo FINISH!!!