# reportio_logger_demo

This project mostly contain the report io demo code .



## Install the bellow package.

```python
python -m pip install -r requiement.txt 
```


## Set the environment variable before execute.  
```shell
export REPORT_IO_ENDPOINT="http://10.176.106.65:8080"
export REPORT_IO_PROJECT="marketplace"
export REPORT_IO_TOKEN="0bbf9a2f-b0fd-4f3b-8f1d-4e3f5d0fba30"
```


## How to execute the demo 
```python

# demo1 , show analytics
 python3 -m demo.demo_1.generate_data 

# demo2 , show filter,dashboard ,merger capability 
python3 -m demo.demo_2.generate_data
python3 -m demo.demo_2.merger

# demo3 integrate with pytest
python3 -m pytest demo/demo_3/tests/report_portal_test.py --reportportal

# demo4 integrate with custom automation framework
python3 -m pytest demo/demo_4/tests/report_portal_test.py 


```


