[TOC]

# Tips for cpp from cppprimer（p458）

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
#### 1.6关联容器单词转换程序（p392）
```CPP
void word_transform(ifstream &map_file, ifstream &input)
(
	auto trans_map = buildMap(map_file);
	string text;
	while(getline(input, text)){
		istringstream stream(text);
		string word;
		bool firstword = true;
		while (stream >> word){
			if (firstword)
				firstword = false;
			else
				cout<<" ";
			cout << transform(word, trans_map);
		}
		cout << endl;
	}
)

map<string, string> buildMap(ifstream &map_file)
{
	map<string, string >trans_map;
	string key;
	string value;
	while(map_file >> key && getline(map_file, value))
		if (value.size() > 1)
			trans_map[key] = value.substr(1);
		else
			throw runtime_error("no rule for " + key);
	return trans_map;
}

const string&
transform(const string &s, const map<string, string> &m)
{
	auto map_it = m.find(s);
	if(map_it != m.cend())
		return map_it->second;
	else
		return s;
}
```

#### 1.7文本查询程序（p430）

```cpp
// 使用
void runQueries(ifstream &infile)
{
    // infile是一个ifstream，指向处理文件
    TextQuery tq(infile);
    // 与用户交互：提示用户输入要查询的单词，完成并打印结果
    while(true)
    {
        cout<<"enter word to look for, or q to quit: ";
        string s;
        // 若遇到文件尾或用户输入了q
        if(!(cin>>s) || s=="q") break;
        // 指向查询并打印结果
        print(cout, tq.qeury(s))<<endl;
    }
}
```

````cpp
// 定义
class QueryResult;
class TextQuery{
public:
    using line_no = std::vector<std::string>::size_type;
    TextQuery(std::ifstream&);
    QueryResult query(const std::string&) const;
private:
    std::shared_ptr<std::vector<std::string>> file;
    // 每个单词到它所在行号的己合的映射
    std::map<std::string, std::shared_ptr<std::set<line_no>>> wm;
};

class QueryResult {
friend std::ostream& print(std::ostream&, const QueryResult& );
public:
QueryResult(std::string s,
           std::shared_ptr<std::set<line_no>> p,
           std::shared_ptr<std::vector<std::string>> f):
    sought(s),lines(p),file(f){ }
private:
    std::string sought;//查询单词
    std::shared_ptr<std::set<line_no>> lines;
    std::shared_ptr<std::vector<std::string>> file;
};

//构造函数
TextQuery::TextQuery(ifstream &is): file (new vector<string>)
{
    string text;
    while(getline(is ,line))
    {
        file->push_back(text);//输入
        int n = file->size() -1;//保存行号
        istringstream line(text);//拆分文本
        string word;
        while(line >> word)
        {
            // 如果单词不在wm中，以之尾下标在wm中添加一项
            auto &lines - wm[word];// line是一个shared_ptr
            if(!lines)// 首次遇到为空
                lines.reset(new set<line_no);// 分配一个新的set
            lines->insert(n);// 将此行号插入set中
        }
    }
}

//查询
QueryResult
TextQuery::query(const string &sought) const
{
    // 如果未找到sought，我们将返回一个指向此set的指针
    static shared_ptr<set<line_no>> nodata(new set<line_no>);
    auto loc = wm.find(sought);
    if(loc == wm.end())
        return QueryResult(sought, nodata, file);
    else
        return QueryResult(sought, loc->second, file);
}

//打印
ostream &print(ostream &os, const QueryResult &qr)
{
    // 如果找到了单词，打印出现次数和所有出现的位置
    os << qr.sought << " occurs " << qr.lines->size() << " "
        <<make_plural(qr.lines->size(), "time", "s") << endl;
    // 打印单词出现的每一行
    for (auto num : *qr.lines)
        os << "/t(line " << num + 1 << ") "
        << *(qr.file->begin() + num) <<endl;
    return os;
}
````


### 2.位操作
#### 2.1位操作成绩单（p138）

```cpp
//操作第27位学生成绩
unsigned long quiz1 = 0;//保证所有平台位数一致
quiz1 |= 1UL << 27;//通过考试
quiz1 &= `(1UL << 27);//没通过
bool status = quizq & (1UL << 27);//查询状态
```
### 3.拷贝控制内存示例（p461）
<a name="anchor-copy-control-p461"></a>
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
### 2.6<font color=red>关联容器(p374)</font>
按关键字保存元素
- map
- set
- multimap
- multiset

无序集合
- unordered_map
- unordered_set
- unordered_mutilmap
- unordered_mutilset
#### 2.6.1重载关键字类型的比较函数（p378）
```cpp
bool compareIsbn(cosnt Sales_data &lhs, const Sales_data &rhs)
{
	return lhs.isbn() < rhs.isbn();
}
mutiset<Sales_data, decltype(compareIsbn)*> bookstore(compareIsbn);
```
#### 2.6.2关联容器的迭代器都为const（p382）
#### 2.6.3关联容器利用insert返回值进行计数&&erase方法会返回删除元素数量（p387）
```cpp
map<string, size_t> word_count;
string word;
while (cin >> word)
{
	auto ret = word_count.insert((word,1));
	if(!ret.second)
		++ret.first->second;
}
```
#### 2.6.4关联容器访问元素&&mutimap查找（p389）
```cpp
c.find(k)//
c.count(k)//
c.lower_bound(k)//第一个不小于
c.upper_bound(k)//第一个大于
c.equal_range(k)//返回一个pair，为k的范围

//方法1
string serach_item("Alain de Botton");
auto entries = authors.count(search_item);
auto iter = authors.find(search_item);
while(entries)
{
	cout<< iter->second << endl;
	++iter;
	--entries;
}
//方法2
for(auto beg = authors.lower_bound(search_item),
		end = authors.upper_bound(search_item);
		beg != end; ++beg)
		cout << beg->second << endl;
//方法3
for (auto pos = authors.equal_range(search_item);
		pos.first != pos.second; ++pos.first)
	cout<<pos.first->second << endl;
```
### 2.7<font color=red>无序容器(p395)</font>

#### 2.7.1无需容器管理操作

| 桶接口                | 正在使用的桶数目                               |
| --------------------- | ---------------------------------------------- |
| c.bucket_count()      | 容器能容纳的最多的桶的数量                     |
| c.max_bucket_count()  | 第n个桶中有多少个元素                          |
| c.bucket_size(n)      | 关键字为k的元素在哪个桶中                      |
| c.bucket(k)           | 关键字为k的元素在哪个桶中                      |
| 桶迭代                |                                                |
| local_iterator        | 可以用来访问桶中元素的迭代类型                 |
| const_local_iterator  | 桶迭代器的const版本                            |
| c.begin(n), c.end(n)  | 桶n的首元素迭代器和尾后迭代器                  |
| c.cbegin(n), c.end(n) | 与前两个函数类似，但是返回cosnt_loacl_iterator |
| 哈希策略              |                                                |
| c.load_factor()       | 每个桶的平均元素数量，返回float值              |
| c.max_load_factor()   | 试图维护的平均桶大小（具体见p395）             |
| c.rehash(n)           | 重组存储（具体见p395）                         |
| c.reserve(n)          | 重组存储（具体见p395）                         |

#### 2.7.2使用自己的hash

```cpp
size_t hasher(const Sales_data &sd)
{
    return hash<string>()(sd.isbn());
}
bool eqOp(const Sales_data &lhs, const Sales_data &rhs)
{
    return lhs.isbn() == rhs.isbn();
}
using SD_mutiset = unordered_mutiset<Sales_data,
					decltype(hasher)*, decltype(eqOp)*>;
//参数是桶大小、哈希函数指针和相等性判断运算符指针
SD_mutiset bookstore(42, hasher, eqOp);
//使用FooHash生成哈希值；Foo必须有==运算符
unordered_set<Foo, decltype(FooHash)*> fooSet(10, FooHash);
```
## 3.stl迭代器
### 3.1迭代器取中间位
```cpp
//取中间位
auto mid = vi.begin() + vi.size()/2;
//note:不能使用mid = beg + (end - beg)/2
//迭代器仅仅存在“-”操作，不存在“+”操作！！！
```
### 3.2插入迭代器(p358)
- back_inserter:创建一个使用push_bask的迭代器
- front_inserter:创建一个使用push_front的迭代器
- inserter:接受两个参数指向前一个容器
```cpp
list<int> lst = {1,2,3,4};
list<int> lst2, lst3;
//拷贝完成后，lst2包含4 3 2 1
copy(lst.cbegin(), lst.cend(), front_inserter(lst2));
//拷贝完成后，lst3包含1 2 3 4
copy(lst.cbegin(), lst.cend(), inserter(lst3, lst3.begin()));
````
### 3.3iostream迭代器(p359)
- istream_iterator
```cpp
istream_iterator<int> int_it(cin);//从cin读取int
istream_iterator<int> int_eof;//尾后迭代器
ifstream in("afile");
istream_iterator<string> str_it(in);//从"afile"读取字符串

//方法1
istream_iterator<int> in_iter(cin);//从cin读取int
istream_itreator<int> eof;//istream尾后迭代器
while (in_iter != eof)//当有数据可供读取时
//后置递增运算读取，返回迭代器旧值
//解引用迭代器，获得从刘读取的前一个值
vec.push(*in_iter++)
//方法2
istream_iterator<int> in_iter(cin), eof;
vector<int> vec(in_iter, eof);
```
- ostream_iterator \
定义
```cpp
ostream_iterator<T> out(os); //输出T类型变量
ostream_iterator<T> (os, d);//每次输出追加d
out=val//这里等同于<<
*out,++out,out++//这里等于没用
```
案例循环打印并加入空格
```cpp
//方法1
ostream_iterator<int> out_iter(cout, " ");
for(auto e: vec)
	out_iter = e;
cout << endl;
//方法2
copy(vec.begin(), vec.end(), out_iter);
cout << endl;
```
使用流迭代器处理类类型
```cpp
istream_iterator<Sales_item> item_iter(cin),eof;
ostream_iterator<Sales_item> out_iter(cout, "\n");
Sales_item sum = *item_iter++;
while (item_iter != eof)
{
	if(item_iter->isbn() == sum.isbn())
		sum == *item_iter++;
	else
	{
		out_iter = sum;
		sum = *item_iter++;
	}
}
out_iter = sum;
```
### 3.4反向迭代器(p363)
反向变正向使用rcomma.base()
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
#### 4.4参数绑定，可用于替换lamba作为谓词（p354）
```cpp
//标准库bind
auto newCallable = bind(callable ，arg_list);
bool check_size(const string &s, string::size_type sz)
{
	return s.size() >= sz;
}
auto check6 = bind(check_size, _1, 6);//_1为占位符
string s = "hello";
bool b1 = check6(s);// check6(s)会调用check_size(s, 6)
//使用bind替代lambda
auto wc = find_if(word.begin(), words.end(), 
					[sz](cosnt string &a))

using namespace std::placeholders;
auto wc = find_if(word.begin(), word.end(), 
					bind(check_size, _1, sz))
//bind函数处理引用，通过ref()和cref()(const版本),定义于functional中
for_each(word.begin(), words.end(),
			bind(print, ref(os), _1, ' '));
```
#### 4.5泛型算法结构(p365,讲解算法的一些命名规则)
#### 4.6特殊的算法用于list和forward_list（p369）
```cpp
lst.merge(lst2)//合并，要求有序,元素会被删除
lst.merge(lst2.comp)//使用comp作为比较函数

lst.splice(args)//将元素插入到某迭代器之前
```

## 5.动态内存（p404）

## <font color=red>shared_ptr</font>（p400）
需要使用动态内存的类：

1. 程序不知道自己需要使用多少对象
2. 程序不知道所需对象的准确类型
3. 程序需要在多个对象间共享数据

### 5.1定义StrBlob类(p405)

```cpp
class StrBlob
{
	public:
		typedef std::vector<std::string>::size_type size_type;
		StrBlob();
		StrBlob(std::initializer_list<std::string> il);
		size_type size() const {return data->size();}
		bool empty() const {return data->empty();}
		//添加和删除元素
		void push_back(const std::string &t){data->push_back(t);}
		void pop_back();
		//元素访问
		std::string& front();
		std::string& back();
	private:
		std::shared_ptr<std::vector<std::string>> data;
		void check(size_type i, const std::string &msg) const;
};
//构造
StrBlob::StrBlob(): data(make_share<vector<string>>()){ }
StrBlob::StrBlob()(initializer_list<string> il):
					data(make_shared<vector<string>>(il)){ }

void StrBlob::check(size_type i, cosnt string &meg) const
{
	if(i>=data->size())
		throw out_out_of_range(msg);
}

string& StrBlob::front()
{
	check(0, "front on empty StrBlob");
	return data->front();
}
string& StrBlob::back()
{
	check(0,"back on empty StrBlob");
	return data->back();
}
void StrBlob::pop_back()
{
	check(0, "pop_back on empty StrBlob");
	data->pop_back();
}
```
#### 5.2shared_ptr和new结合使用(p412)
智能指针的构造是explicit的因此必须使用显式初始化
```cpp
//错误：产生了内置指针到智能指针的隐式转换（p265）
shared_ptr<int> p1 = new int(1024);
//正确：使用了直接初始化形式
shared_ptr<int> p2(new int(42));
shared_ptr<int> clone(int p)
{
	return shared_ptr<int>(new int (p));
}
```
#### 5.3改变和定义shared_ptr的方法（p412）&&由多个对象共享的指针改变前检查对象用户（p414）

| shared_ptr<T> (q)    | <font color=red>必须是new的</font>|
| --------------------- | ----------------------------------- |
| shared_ptr<T> p(u)    | 从unique_ptr那里接管所有权，将u置空 |
| shared_ptr<T> p(q，d)  | 从<font color=red>内置指针</font>接管，调用可调用对象d代替delete，<font color=red>q必须能转化为T*</font> |
| shared_ptr<T> p(p2，d) | 从<font color=red>智能指针</font>接管，其余同上 |
| p.reset() | 如果p是唯一指向对象的shared_ptr，reset将会释放该对象，将p置空 |
| p.reset(q) | 若传递了q会令p指向q |
| p.reset(q,d) | 同时调用d代替原来的delete |

```cpp
p = new int(1024);//错误：不能将普通指针赋予shared_ptr
p.reset(new int(1024));//正确：将p指向一个新对象

if(!p.unique())
	p.reset(new string(*p));//不是唯一用户；分配新的拷贝
*p += newVal;//现在我们为唯一用户，可以改变对象的值
```
### 5.4使用智能指针管理资源示范（网络资源管理）（p416）
错误示范：如果connect没有析构函数会导致问题
```cpp
struct destination;
struct connection;
connection connect(destination*)
void disconnect(connection);
void f(destination &d /*其他参数*/)
{
	//获得一个连接；记住使用后需要关闭
	connection c = connect(&d);
	//使用连接
	//如果推出前忘记调用disconnect，就无法关闭c了
}
```
正确方法：支持优雅退出？？？
```cpp
void end_connection(connection *p) { disconnect(*p); }
void f(destionation &d /*其他参数*/)
{
	connection c = connect(&d);
	std::shared_ptr<connection> p(&c, [](connection *p){ disconnect(*p); });//使用匿名函数
	shared_ptr<connection> p(&c, end_connection);//注意第一个参数必须能转化为指针
	//使用连接
	//当f退出时（即时由于异常），connection会被正确关闭
}
```
### 5.5智能指针陷阱（p417）
- 不使用相同的内置指针初始化（或reset）多个智能指针
- 不delete get（）返回的指针
- 不使用get（）初始化或reset另外一个智能指针
- get（）的返回，在智能指针销毁后失效
- 管理不是new的内存需要指定一个删除器，<font color=red>区别5.3</font>

## <font color=red>unique_ptr</font>（p417）
### 5.6unique_ptr不支持拷贝和赋值（p417）&&智能指针常见操作（p418）
以下行为均不支持
```cpp
unique_ptr<string> p2(p1);//不支持拷贝
unique_ptr<string> p3;
p3(p2);//不支持赋值
```
可用的拷贝和转移方法

```cpp
unique_ptr<string> p2(p1.release());//将控制权转移至p2，p1置空
unique_ptr<string> p3(new string("Trex"));
//将所有权从p3转移至p2
p2.reset(p3.release());//使用reset释放了原来指向p2的内存
```

| unique_ptr<T> u1      |                                            |
| --------------------- | ------------------------------------------ |
| unique_ptr<T,D> u2    | 使用类型D的可调用对象来释放指针            |
| unique_ptr<T,D> u2(d) | 传入d的具体类型                            |
| u = nullptr           | 释放，置空                                 |
| u.release()           | u放弃对指针的控制权，返回指针，并将u置为空 |
| u.reset()             | 释放u所指对象                              |
| u.reset(q)            | 提供内置指针q，则指向这个对象，否则置空    |
| u.reset(nullptr)      |                                            |

## <font color=red>weak_ptr</font>（p420）

### 5.7weak_ptr常见操作

| weak_ptr<T> w      | 空weak_ptr |
| --------------------- | ------------------------------------------ |
| weak_ptr<T> w(sp)    | 与shared_ptr指向相同对象的weak_ptr。T必须能够转换为sp指向的类型。 |
| w = p | p可以是一个share或者weak，赋值后w和p共享对象 |
| w.reset()           | 将w置空                             |
| w.use_count()           | 与w共享的shared_ptr数量 |
| w.expired()             | w.use_count()，返回ture否则返回false |
| w.lock()            | w.expire()为true返回一个空的shared_ptr；否则返回一个指向w的对象的shared_ptr |

```cpp
//基本使用
auto p = make_shared<int>(42);
weak_ptr<int> wp(p);

//由于对象可能不存在，因此使用前要进行检查
if(shared_ptr<int> np = wp.lock())
{
	//在if中，np和p共享对象
}
```
### 5.8weak_ptr使用案例核查指针类StrBlobPtr（p421）
```cpp
class StrBlobPtr{
	public:
		StrBlobPtr():curr(0){ }
		StrBlobPtr(StrBlob &a, size_t sz = 0):
				wptr(a.data), curr(sz){ }
		std::string& deref() const;
		StrBlobPtr& incr();//前缀递增
	private:
		//检查成功，check返回一个指向vector的shared_ptr
		std::shared_ptr<std::vector<std::string>>
			check(std::size_t, const std::string&) const;
		//保存一个weak_ptr意味着底层vector可能会被销毁
		std::weak_ptr<std::vector<std::string>> wptr;
		std::size_t curr;//在数组中的当前位置
}；

std::shared_ptr<std::vector<std::string>>
StrBlobPtr::check(std::size_t i, const std::string &msg) const
{
	auto ret = wptr.lock();//判断vector是否存在
	if(!ret)
		throw std::runtime_error("unbound StrBlobPtr");
	if(i >= ret->size())
		throw std::out_of_range(msg);
	return ret;//否则，返回指向vector的shared_ptr
}

//解引用函数
std::string& StrBlobPtr::deref() const
{
	auto p = check(curr, "derefence past end");
	return (*p)[curr];// (*p)是对象所指向的vector
}

//前缀递增
StrBlobPtr& StrBlobPtr::incr()
{
	//如果curr已经指向容器的尾后位置，就不能递增它
	check(curr, "increment past end of StrBlobPtr");
	++curr;
	return *this;
}

//为了访问data成员，指针类必须申明为StrBlob的friend，同时还需要定义begin和end操作，返回一个自身指向它自身的StrBlobPtr
//对于StrBlob中的友元来说，此前声明是必要的
class StrBlobPtr;
class StrBlob{
	friend class StrBlobPtr;
	StrBlobPtr begin() { return StrBlobPtr(*this); }
	StrBlobPtr end()
	{
		auto ret = StrBlobPtr(*this, data->size());
		return ret;
	}
}
```
## <font color=red>allocator类</font>（p427）

标准库allocator类定义在头文件memory中，它帮助我们将内存分配和对象构造分离开来。

```cpp
allorator<string> alloc;//可以分配string的allocator对象
auto const p = alloc.allocate(n);//分配n个未初始化的string
auto q = p;
alloc.construct(q++);
alloc.construct(q++,10,'c');
alloc.constrcut(q++,"hi");
cout<<*p<<endl;
cout<<*q<<endl;
while(q!=p)
    alloc.destroy(--q);
alloc.deallocate(p,n);
```

### 5.8allocator基本用法（p428）

| 标准库allocator类及算法 |                                                              |
| ----------------------- | ------------------------------------------------------------ |
| allocator<T> a          | 定义一个名为a的allocator对象，它可以为类型为T的对象分配内存  |
| a.allocate(n)           | 分配一段原始的、未构造的内存，保存n个类型为T的对象           |
| a.deallocate(p, n)      | 释放从T*指针p中的地址开始的内存，这块内存保存了n个类型为T的对象；p必须是一个先前由allocate返回的指针，且n必须是p创建时所要求的大小。在调用deallocate之前，用户必须对每个在这块内存中创建的对象调用destroy |
| a.construct(p, *argv*)  | p必须是一个类型为T*的指针，指向一块原始内存：arg被传递给类型为T的构造函数，用来在p指向的内存中构造一个对象 |
| a.destory(p)            | p为T*类型的指针，此算法对p指向的对象执行析构函数（参照p402） |

### 5.9allocator的拷贝填充算法（p429）

## 6.拷贝控制
### 6.1行为像值的类(p453)

```cpp
class HasPtr
{
public:
	HasPtr(const std::string &s = std::string()):
		ps(new std::string(s), i(0)){ }
	// 对ps指向的string， 每个HasPtr对象都有自己的拷贝
	HasPtr(const HasPtr &p):
		ps(new std::string(*p.ps)), i(p.i){ }
	HasPtr& operate=(const HasPtr &);
	~HasPtr() { delete ps; }
private:
	std::string *ps;
	int 		i;
}

HasPtr& HasPtr::operate=(const HasPtr &rhs)
{
	auto newp = new string(*rhs.ps);// 拷贝底层string
	delete ps;// 释放旧内存
	ps = newp;// 从右侧运算符拷贝数据到本对象
	i = rhs.i;
	return *this;// 返回本对象
}
```
### 6.2行为像指针的类(p455)
建议使用智能指针，如果希望直接管理资源，则需要使用<font color=red>引用计数</font>
```cpp
#include <string>
#include <iostream>
#include <memory>
#include <fstream>
using namespace std;
class HasPtr{
	public:
		HasPtr(const string &s = string());
		HasPtr& operator=(const HasPtr&s);
		HasPtr(const HasPtr&);
		~HasPtr();
		string str(){return *ps;}
		size_t use_count()const{
			return *use;
		}		
 
 
	private:
		string *ps;
		int i;
		std::size_t* use;
 
};
HasPtr::HasPtr(const string &s):ps(new string(s)),
	i(0),use(new std::size_t(1)){}
HasPtr::HasPtr(const HasPtr& p ):ps(p.ps),use(p.use),i(p.i){++*use;}
HasPtr::~HasPtr(){
//析构函数不能无条件释放ps和use
if(--*use == 0)
	{
		delete ps;
		delete use;
	}
}
HasPtr& HasPtr::operator=(const HasPtr & p){
//拷贝赋值运算符必须在自赋值情况下正确工作
++ *p.use;
if(--*use == 0)
	{
		delete ps;
		delete use;	
	}
ps = p.ps;
i  = p.i;
use = p.use;
//注意这里得写对
return *this;
}
```
智能指针写法
```cpp
#include <memory>

class PointerLike {
private:
    std::unique_ptr<int> ptr;
public:
    PointerLike(int* p = nullptr) : ptr(p) {}
    PointerLike(const PointerLike& other) : ptr(std::make_unique<int>(*other.ptr)) {}
    PointerLike& operator=(const PointerLike& other) {
        if (this != &other) {
            ptr = std::make_unique<int>(*other.ptr);
        }
        return *this;
    }
    int& operator*() const {
        return *ptr;
    }
    int* operator->() const {
        return ptr.get();
    }
};
```
### 6.3交换操作（正确使用swap函数）(p458)
#### 6.3.1使用自定义的swap函数（p458）
```cpp
class HasPtr {
	friend void swap(HasPtr&, HasPtr&);
};
inline
void swap(HasPtr &lhs, HasPtr &rhs)
{
	//这样写会优先使用已经存在的swap函数，而不是std中的函数
	using std::swap;
	swap(lhs.ps, rhs.ps);
	swap(lhs.i, rhs.i);
}

```
#### 6.3.2在赋值运算中使用swap（copy and swap）（p458）
Tip:使用拷贝和交换的赋值运算符自动就是安全的，且能正确处理自赋值
```cpp
HasPtr& HasPtr::operater=(HasPtr rhs)
{
	//交换左侧运算对象和局部变量rhs
	swap(*this, rhs);
	return *this;
}
```
#### 6.3.3拷贝控制示例（p461）
- [拷贝控制示例](#anchor-copy-control-p461)
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
### 5.<font color=red>explict隐式的类类型转化</font>（p264）
explict关键字使得函数确定为只能显示使用构造函数来进行 \
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
|   函数   |                功能                 |
| :------: | :---------------------------------: |
| isalnum  |        检查字符是否为字母数         |
| isalpha  |         检查字符是否为字母          |
| isblank  | 检查字符是否为空白（C++11以上支持） |
| iscntrl  |       检查字符是否为控制字符        |
| isdigit  |        检查字符是否为小数位         |
| isgraph  |       检查字符是否有图形表示        |
| islower  |       检查字符是否为小写字母        |
| isprint  |         检查字符是否可打印          |
| ispunct  |     检查字符是否为标点符号字符      |
| isspace  |         检查字符是否为空白          |
| isupper  |       检查字符是否为大写字母        |
| isxdigit |       检查字符是否为六分位数        |
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
__func__//局部静态变量，用于存放当前执行的函数名字
__FILE__//存放文件名的字符串字面值
__LINE__//存放当前行号的整型字面值
__TIME__//存放文件编译时间的字符串字面值
__DATE__//存放文件编译日期的字符串字面值
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
### 8.布尔值不参与加减运算（“-”不能取反，用！）（p125）
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