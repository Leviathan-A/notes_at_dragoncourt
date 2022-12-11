[TOC]

# Tips for cpp from cppprimer（p354）

---
## 正则表达式
---
## 一些有趣的小代码模版
### 1.关于输入输出思考
#### 1.1.通过getline获取string,并通过istringstream初始化类(p288)以及使用ostringstream进行输出（p289）
```cpp
//每次读入一整行，遇到空字符直接跳过
string line;
while(getline(cin,line))
  if(!line.empty())
      cout<<line<<endl;

//每次读入一整行，输出其中超过80个字符的行
string line;
while(getline(cin,line))
  if(line.size()>80)
      cout<<line<<endl;
//note:line.size()返回的始终为无符号类型，因此不可与int进行比较

//istringstream输入
string line, word;
vector<PersonInfo> people;
while(getline(cin, line))
{
	PersonInfo info;
	istringstream record(line);
	record >> info.name;
	while(record >> word)
	{
		info.phones.push_back(word);
	}
	people.push_back(info);
}

//ostringstream输出
for(const auto &entry : people)
{
	ostringstream formatted, badNums;
	for(const auto &nums : entry.phones){
		if(!valid(nums)){
			badsum << " " << num;
		}else
			formatted << " " << format(nums);
	}
	if(badNum.str().empty())
		os << entry.name << " "
		<< formatted.str() <<endl;
		else
			cerr << "input error: " << entry.name
				<< " invalid number(s) " << badNums.str() <<endl;
}

//利用istringstream和命令行初始化类参数
string line, word;
vector<PersonInfo> people;
while(getline(cin,line))
{
	PersonInfo info;
	istringstream record(line);
	record >> info.name;
	while(record >> word)
		info.phones.push_back(word);
	people.push_back(info);
}

```
#### 1.2.类中的read和print函数
```cpp
std::ostream &print(std::ostream&, const Sales_data&);
std::istream &read(std::istream&, Sales_data&);

istream &read(istream &is, Sales_data &item)
{
  double price = 0;
  is >> item.bookNo >> item.units_sold >> price;
  item.revenue = price * item.units_sold;
  return is;
}

osstream &print(ostream &os, const Sales_data &item)
{
  os << item.isbn() << " " << item.units_sold << ""
     << item.isbn() << " " << item.avg_price();
     return os;
}
```
#### 1.3ifstream处理文件列表（p285）
```cpp
//每个循环input都会离开作用域，因此会自动销毁，并且在销毁时自动调用close
for(auto p = argv + 1; p = != argv + argc; ++p)
	ifstream input(*p);
	if(input){
		process(input);
	}else
		cerr<<"couldn't open: " + string(*p);
```
#### 1.4关于打开文件(p286)
```cpp
ofstream out("file")//默认覆写
ofstream out1("file"， ofstream::trunc)//默认覆写
ofstream app("file2", ofstream::app);//追加

ofstream out;
out.open("scratchpad");
out.close();
out.open("precious", ofstream::app);
out.close();
```
#### 1.5关于string字符串操作（p325）
```cpp
s.find();//args第一次
s.rfind();//args最后一次
s.find_first_of();//args中第一次出现的位置
s.find_last_of();//args中最后出现的位置
s.find_first_not_of();//第一个不在args中的字符
s.find_last_not_of();//最后一个不在args中的字符
```
## 2.stl容器
### 2.1利用数组初始化vector
```cpp
int int_arr={0,1,2,3,4,5};
vector<int> ivec(begin(int_arr),end(int_arr));
```
### 2.2没有默认构造函数的类在使用容器时需要传递一个元素初始化器（p295）
```cpp
vector<noDefault> v1(10, init)
```
### 2.3assign可以将不同类型但是相容的类型进行拷贝（p302）
```cpp
list<string> names;
vector<const char*> oldstyle;
name.assign(oldstyle.cbegin(),oldstyle.cend());
```
### 2.4向一个vector、string或deque插入元素会使得所有指向容器的迭代器、引用和指针失效
### 2.5insert的返回值为指向新元素的迭代器
## 3.stl迭代器
### 3.1迭代器取中间位
```cpp
//取中间位
auto mid = vi.begin() + vi.size()/2;
//note:不能使用mid = beg + (end - beg)/2
//迭代器仅仅存在“-”操作，不存在“+”操作！！！
```
## 4.泛型&&算法
#### 4.1消除重复单词
```cpp
//消除重复单词
void elimDups(vector<string> &words)
{
	sort(words.begin(), words.end());
	auto end_unique = unique(words.begin(), words.end());
	words.erase(end_unique, words.end());
}
```
#### 4.2算法可以传递可调用对象，可调用对象有函数，函数指针，重载了函数调用符的类和lambda表达式（p346）

#### 4.3lamba隐式捕获&&捕获列表&&尾置返回（p351-352）

```cpp
//当使用混合使用隐式捕获和显示捕获时，捕获列表中的第一个元素必须是一个&或=
void biggies(vector<string> &words, vector<string>::size_type sz, ostream &os = cout, char c = ' ')
{
    //os为隐式捕获，引用捕获方式；c隐式捕获，值捕获方式
    for_each(words.begin(),words.end(),
            [&,c](const string &s){os << s << c;});
    //os为显示捕获，引用捕获方式；c隐式捕获，值捕获方式
    for_each(words.begins(),words.end(),
            [=,&os](const string &s){os << s <<c;});
}
//捕获列表
[]
[name]
[&]
[=]
[& , identifer_list]
[= , identifer_list]
//lamba返回
transform(vi.begin(), vi.end(), vi.begin(),
         [](int i) -> int
         { if (i < 0) return -i; else return i; });
```

### 4.4参数绑定，可用于替换lamba作为谓词（p354）

### 4.位操作成绩单（p138）
```cpp
//操作第27位学生成绩
unsigned long quiz1 = 0;//保证所有平台位数一致
quiz1 |= 1UL << 27;//通过考试
quiz1 &= `(1UL << 27);//没通过
bool status = quizq & (1UL << 27);//查询状态
```
### 5.关于switch用法（p162）
```cpp
char vowelCnt;
switch (ch){
  case 'a':
  case 'e':
  case 'i':
  case 'o':
  case 'u':
    ++vowelCnt;
    break;
  default:
    ++otherCnt;
    break;
}
```
### 6.使用const_cast实现函数同时接受常量和非常量(p209)
```cpp
const string &shorterString(string &s1, string &s2)
{
  auto &r = shorterString(const_cast<const string&>(s1),
                          const_cast<const string&>(s2))
  return const_cast<string&>(&r);
}
```
### 7.decltype的有趣小用法
#### 7.1返回数组指针
```cpp
int odd[] = {1,2,3,5,9};
int even[] = {0,2,4,6,10};
decltype(odd) *arrPtr(int i)
{
  return (i%2) ? &odd : &even;
}
```
#### 7.2快速定义函数指针
```cpp
typedef decltype(lengthCompare) *FuncP2
```
### 8.如何实现连续调用类成员变量
```cpp

class Screen {
public:
  //根据对象是否是const重载了display函数,cosnt对象（指针）只能调用const成员函数和static成员函数
	Screen &display(std::ostream &os)
		{do_display(os); return *this}
	const Sreeen &display(std::ostream &os) const
		{do_display(os); return *this;}
private:
		void do_display(std::ostream &os) const {os << contents;}
}

Screen myScreen(5,3);
const Screen blank(5,3);
myScreen.set('#').display(cout);//调用非常量版本
blank.display(cout);//调用常量版本
```
---
## 关于C++类的一些使用细节
### 0.C11新特性
#### 0.1委托构造函数（p261）
一个委托构造函数使用它所属类的其他构造函数执行它自己的初始化过程，或者说把它自己的一些（或者全部）职责委托给了其他构造函数，可以减少重复代码
```cpp
class Sales_data {
public:
	//非委托构造函数使用对应的实参初始化成员
	Sales_data(std::string s, unsigned cnt, double price):
		bookNo(s), units_sold(cnt), revence(cnt*price){ }
	//其余构造函数全都委托给另外一个构造函数
	Sales_data(): Sales_data("", 0, 0){}
	Sales_data(std::string): Sales_data(s, 0, 0){}
	Sales_data(std::isstream &is): Sales_data()
										{read(is,*this);}
}
```
### 1.如果成员是const、引用。或者属于某种未提供默认构造函数的类类型，必须通过构造函数初始值列表为这些成员提供初值(p259)
```cpp
ConstRef::ConstRef(int(ii):i(ii),ci(ii),ri(i)){}
```
### 2.C++类中成员初始化顺序(p259)
### 3.不能同时多个构造函数都全部使用默认实参，多个空参数会导致二义性冲突（p261）
构造函数初始值列表中初始值的前后位置关系不影响实际初始化顺序\
成员初始化顺序与类定义中的出现顺序一致\
<font color=red>Best Practice:</font>\
最好令构造函数初始值的顺序与成员声明顺序保持一致。\
而且如果可能的话，尽量避免使用某些成员初始化其他成员（否则无法通过<font color=red>-Werror</font>选项）
### 4.<font color=red>Best Practice：</font>如果定义其他构造函数，那么最好提供一个默认构造函数（p262）
### 5.<font color=red>隐式的类类型转化</font>（p264）
若Sales_data类中，接受string的构造函数和接受istream的构造函数分别定义了从这两种类型向Sales_data隐式转换的规则。\
同时编译器只会自动执行一步类型转换。如果需要抑制构造函数的隐式转换，可以将构造函数声明为explicit。
```cpp
//隐式转换
string null_book = "9-999-99999999";
item.combine(null_book);

item.combine("9-999-99999999");//只允许一步类类型转换，因此以下代码会产生错误,正确做法需要显示调用
item.combine(string("9-999-99999999"));//显示转换成string，隐式转换成Sales_data
item.combine(Sales_data("9-999-99999999"));//隐式转换成string，显示转化成Sales_data

//抑制构造函数的隐式转换,但是explicit构造函数之恶能用于直接初始化
class Sales_data{
public:
	Sales_data() = default;
	Sales_data(const std::string &s, unsigned n, double p):
			boolNo(s), units_sold(n), revenue(p*n){ }
	explicit Sales_data(const std::string &s):bookNo(s){ }
	explicit Sales_data(std::istream&);
}
Sales_data item1(null_book);//正确：直接初始化
Sales_data item2 = null_book;//错误：不能将explicit函数用于发生隐式转换的拷贝初始化
```
### 6.static成员函数中的static仅出现在声明中（p270）
---
## 精华碎碎念

### 1.#ifndef头文件保护（p68）
```cpp
#ifndef SALES_DATA_H
#define SALES_DATA_H
//头文件内容
#endif
```
### 2.cctype头文件针对单个字符的相关操作（p82）
|函数|	功能|
|:---:|:---:|
|isalnum|	检查字符是否为字母数|
|isalpha|	检查字符是否为字母|
|isblank|	检查字符是否为空白（C++11以上支持）|
|iscntrl|	检查字符是否为控制字符|
|isdigit|	检查字符是否为小数位|
|isgraph|	检查字符是否有图形表示|
|islower|	检查字符是否为小写字母|
|isprint|	检查字符是否可打印|
|ispunct|	检查字符是否为标点符号字符|
|isspace|	检查字符是否为空白|
|isupper|	检查字符是否为大写字母|
|isxdigit|	检查字符是否为六分位数|
### 3.迭代器操作
#### 3.1 尽量使用！=
#### 3.2 不涉及写尽量采用.cbegin()以返回const_iterator
### 4.指针操作
#### 4.1获取头指针和尾后指针
```cpp
int ia[]={0,1,2,3,4,5};
int *beg = begin(ia);
int *end = end(ia);
```
### 5.多层循环中，除了最内层循环，其他所有循环都应使用引用。（p114）
### 6.赋值运算符的优先级低于关系运算符优先级，在条件语句中，赋值部分应该加上括号（p130）
### 7.巧用*iter++（打印当前并++）
### 8.对于<<，只有算数运算是优先的
### 9.int mat[10]（指针数组）,int (p)[4]（数组指针）（p196）
### 10.整型提升问题（p142）
### 11.建议将内联函数和constexpr函数放在头文件内（p215）
### 12.<font color=red>五个实用编译器变量（p220）</font>

```cpp
//类型为const char数组
_ _func_ _//局部静态变量，用于存放当前执行的函数名字
_ _FILE_ _//存放文件名的字符串字面值
_ _LINE_ _//存放当前行号的整型字面值
_ _TIME_ _//存放文件编译时间的字符串字面值
_ _DATE_ _//存放文件编译日期的字符串字面值
```
---
## 碎碎念
### 1.文件输入重定向（p19）
`$ additem <infile> outline`
### 2.默认初始化（p40）
- 定义于**函数体内的内置类型**对象如果没有初始化，其值未定义。
- 类对象没有显式初始化，其值有类的默认初始化定义（大概）。

### 3.声明和定义的可分离性（p41）
C++支持分离式编译，即声明和定义分离
```cpp
extern int i;     //声明i而非定义i
int j;            //声明并定义j
```
### 4.void*可用于存放任何内容的指针（p50）
 **void\*指针作用**：

- 和别的指针进行比较；
- 作为函数的输入或是输出；
- 给其他void*指针的赋值；
- 不能直接操作void*指向对象。

### 5.constexpr和常量表达式（p59）
-   **常量表达式**指编译就能确定具体数值，且不会改变。
-   使用*constexpr*前缀可以用于检查该值是否为常量表达式。

### 6.类型别名(typedef和using)（p60）
```cpp
//传统方法typedef:
typedef double wages;
//别名声明alias declaration
using SI = Sales_item; 
```
### 7.decltype（p62）
```cpp
//不调用函数f()但是取得该函数的返回值
decltype(f()) sum = x;

const int ci = 0, &cj =ci;
decltype(ci) x = 0;//x类型是const int
decltype(cj) y = x;//y类型是cosnt int&，y绑定到x
decltype(cj) sum = x;//错误：z是一个引用，必须初始化

```
### 8.布尔值不参与加减运算（“-”不能取反）（p125）
### 9.进行位运算时“小整型”会被自动提升为更大的整型（p136）
### 10.对于vector和string，sizeof仅会返回固定部分的大小（p140）
### 11.static_cast(常用类型转换)，const_cast（去掉底层const），reinterpret_cast（相当于强转）（p145）
### 12.for循环多重定义只能定义一种类型变量（p167）
### 13.<font color=red>返回数组指针(p206)</font>
```cpp
//原始方法
int (*func(int i))[10]
//尾置返回
auto func(int i) -> int(*)[10]
//巧用decltype
int odd[] = {1,2,3,5,9};
int even[] = {0,2,4,6,10};
decltype(odd) *arrPtr(int i)
{
  return (i%2) ? &odd : &even;
}
```