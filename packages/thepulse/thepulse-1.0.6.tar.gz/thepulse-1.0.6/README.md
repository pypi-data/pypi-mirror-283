# thepulse-sdk-python


```ipython

>>> import thepulse
>>> kit = keepintouch.Init() 
>>> kit.update('your_key','your_value')
{'_id': '27809a60de71', '_key': 'your_key', '_url': 'https://httpbin.cn/greetings/27809a60de71', '_value': 'your_value'}
>>> kit.get('27809a60de71')
{'_key': 'your_key', '_value': 'your_value'}
>>> kit.update('your_key_updated','your_value_updated', greeting_id='27809a60de71')
{'_id': '27809a60de71', '_key': 'your_key_updated', '_url': 'https://httpbin.cn/greetings/27809a60de71', '_value': 'your_value_updated'}
>>> kit.get('27809a60de71')
{'_key': 'your_key_updated', '_value': 'your_value_updated'}
>>> 


```