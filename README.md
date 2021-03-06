# Web crawler Pratice Program
A pratice for web crawler and gui application using python.<br></br>
Facing difficult due to lack of performance.<br></br>
Using Multi-threading to downloading picture(decrease I/O time).

# Next update
- [x] program flow
- [x] MultiThread vs MultiProcessing
- [ ] Program explain MultiThread vs MultiProcessing


## Program flow chart
create by Hackmd

```flow
io=>inputoutput: 輸入日期和按讚數

cond2=>condition: 發文案讚數 > Like count?
cond1=>condition: 確認發文日期
op1=>operation: 收集發文
op2=>operation: 建立 QThread下載發文圖片

io->cond1(yes)->op1->cond2
cond2(yes)->op2
cond2(no)->cond1
cond1(no)->cond1
```

![image](https://user-images.githubusercontent.com/34651757/125172253-33598100-e1eb-11eb-9e70-caa511e811c8.png)

## MultiThread vs MultiProcessing (from https://medium.com/contentsquare-engineering-blog/multithreading-vs-multiprocessing-in-python-ece023ad55a)

|Task        |MultiThreading|MultiProcessing|Original    |
|----------- |-----------|-----------|-----------|
|IO Bounding |  **Fast**         |   **Fast**(slower than thread)        |     slow      |
|CPU Bounding|  slow     |**Fast**   |   slow        |

Testing for IO Bounding task : 


Testing for CPU Bounding task : 
<p align="left"><img width="40%" src="result/test_result.png"/></p>
Explanations : 

We have four task, each task is to looping numeric addition.<br></br>
In our pool we have four workers for process and thread and in the result you can see that the cost time of thread is merely four times of process.

<img width="914" alt="image" src="https://user-images.githubusercontent.com/34651757/126960009-ab66442f-30ab-4ac2-94c4-67d681ca3691.png">
There is a restriction of threading in python due to the GIL(global interpreter Lock),when cpu is processing the program multithread will switch to another thread frequently.<br></br>
But when it comes to multiprocessing there were no GIL restriction so the four workers works parallelly.<br></br>

## Other Information

Python - if __name__ == '__main__'
-> If you only wrote one python file it doesn't matter.
```python=
def test_main():
    print('I\'m cool!')
    
test_main()

```
![image](https://user-images.githubusercontent.com/34651757/125195528-99e0ac80-e288-11eb-8600-7638ec91dcdd.png)

-> But if you import python to other file

```python=

from cool import test_main 

print('other_program call : ')
test_main()

```
![image](https://user-images.githubusercontent.com/34651757/125195592-e0360b80-e288-11eb-9969-7be7cedaf06c.png)

--> Because when you import other python module the python Interpreter will execute the import module(cool.py).

--> To correct this problem, use __name__ . <br></br>
__name__ is Builtin variable and value of it is differ in every file.

![image](https://user-images.githubusercontent.com/34651757/125195826-0b6d2a80-e28a-11eb-9f00-2c2baad03cf1.png)
![image](https://user-images.githubusercontent.com/34651757/125195835-1627bf80-e28a-11eb-8654-c3f948f38941.png)

cool2.py import cool.py in cool.py the builtin variable __name__ is cool but in cool2.py(execute file) the value is __main__.<br></br>
So add the condition if __name__ == '__main__' to both file(cool.py, cool2.py) and you can fix the output result.

![image](https://user-images.githubusercontent.com/34651757/125196026-d44b4900-e28a-11eb-91ca-ca2045819eb3.png)
![image](https://user-images.githubusercontent.com/34651757/125196043-dd3c1a80-e28a-11eb-8366-16c09707da3d.png)


