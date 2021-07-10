# Web crawler Pratice Program
A pratice for web crawler and gui application using python.<br></br>
Facing difficult due to lack of performance.<br></br>
Using Multi-threading to downloading picture(decrease I/O time).

# Next update
- [x] program flow
- [ ] Thread information for cpython


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

## Thread Information

updating...
