# reportio_logger_demo

This project mostly contain the report io demo code .



## Install the bellow package.

```python
python -m pip install -r requiement.txt 
```


## Set the environment variable before execute for linux.  
```shell
export REPORT_IO_ENDPOINT="https://demo.reportportal.io"
export REPORT_IO_PROJECT="default_personal"
export REPORT_IO_TOKEN="12ce7721-d852-4b1e-bc0a-686105307071"
```


## Set the environment variable before execute for windows.  
```shell
set REPORT_IO_ENDPOINT=https://demo.reportportal.io
set REPORT_IO_PROJECT=default_personal
set REPORT_IO_TOKEN=12ce7721-d852-4b1e-bc0a-686105307071
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


