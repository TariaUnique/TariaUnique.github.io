decltype 和auto都是c++11引入的自动类型推导的关键字。

decltype可以从表达式推导其类型，而并不需要计算表达式。
auto 可以通过变量的初始值推导变量的类型，而不需要我们显示提供变量的类型。

在使用auto做类型推导时，实际type的const，reference属性会被省略，而decltype(auto)会保留实际type的const，reference属性。
```c++
#include <iostream>
using std::cout;
using std::endl;



int main(){
    int x = 0;
    auto a = x;  // a is int
    cout<<"a const "<<std::is_const<decltype(a)>::value<<endl; //0
    cout<<"a reference "<<std::is_reference<decltype(a)>::value<<endl; //0
    const int y = 0;
    auto b = y;  // b is int, not const int
    cout<<"b const "<<std::is_const<decltype(b)>::value<<endl; //0
    cout<<"b reference "<<std::is_reference<decltype(b)>::value<<endl; //0

    int& z =x;
    auto c = z; //c is int, not int&
    cout<<"c const "<<std::is_const<decltype(c)>::value<<endl; //0
    cout<<"c reference "<<std::is_reference<decltype(c)>::value<<endl; //0

    int xx = 0;
    decltype(auto) cc = xx;  // cc is int
    cout<<"cc const "<<std::is_const<decltype(cc)>::value<<endl; //0
    cout<<"cc reference "<<std::is_reference<decltype(cc)>::value<<endl; //0

    int& yy = xx;
    decltype(auto) dd = yy;  // dd is int&, not int
    cout<<"dd const "<<std::is_const<decltype(dd)>::value<<endl; //0
    cout<<"dd reference "<<std::is_reference<decltype(dd)>::value<<endl; //1

    const int ee = 0;
    decltype(auto) ff = ee;  // ff is const int
    cout<<"ff const "<<std::is_const<decltype(ff)>::value<<endl; //1
    cout<<"ff reference "<<std::is_reference<decltype(ff)>::value<<endl; //0

}
```

如果我们写如下的一个简单的bind函数
```c++
template <typename Func, typename... Args>
auto bind(Func&& f, Args&&... args)
{
    return [&f, &args...]() -> auto
    {
        return f(args...);
    };
};
```
bind 给Func绑定参数。其lambda返回的是auto。 如果被绑定的函数返回的是引用，则会丢失引用的属性，测试如下
```c++
#include <iostream>
using std::cout;
using std::endl;
namespace me{
template <typename Func, typename... Args>
auto bind(Func&& f, Args&&... args)
{
    return [&f, &args...]() -> auto //或者auto省略
    {
        return f(args...);
    };
};

}


int global = 10;

int& get_global_val(){
    return global;
};

int main(){
    auto bf2 = me::bind(get_global_val);
    cout<<std::is_reference<decltype(bf2())>::value<<endl; //输出 0
}
```

将bind改为 
```c++
template <typename Func, typename... Args>
auto bind(Func&& f, Args&&... args)
{
    return [&f, &args...]() -> decltype(auto)
    {
        return f(args...);
    };
};
```
最后才会是返回`int&`

