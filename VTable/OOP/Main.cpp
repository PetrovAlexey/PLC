#include <iostream>
#include <map>
#include <string>
#include <functional>

#define VIRTUAL_CLASS(Base) class Base {\
public:\
std::map<std::string, std::function<void(void*)>> vtable;

#define END_CLASS(Base) };

#define BASE_CONSTRUCTOR(Base, Code) Base() { Code };

#define START_METHOD(Base, Method)\
static void Method(void* ptr) {\
Base* this_ = reinterpret_cast<Base*>(ptr);\

#define END_METHOD std::cout << std::endl; };


#define ADD_FUNCTION(Base, Method)\
this->vtable[#Method] = std::function<void(void*)>(this->Method);


#define VIRTUAL_CALL(ptr, Method)\
ptr->vtable[#Method](ptr);                                                

#define VIRTUAL_CLASS_DERIVED(Base, Derived) class Derived {\
public:\
std::map<std::string, std::function<void(Derived*)>> vtable;

#define DERIVED_CONSTRUCTOR(Base, Derived, Code) Derived() {\
    Code\
    Base b;\
    for (auto i = b.vtable.begin(); i != b.vtable.end(); ++i) {\
        if (this->vtable.count(i->first) == 0) {\
            this->vtable[i->first] = std::function<void(Derived*)>(i->second);\
        }\
    }\
};   

// базовый класс
VIRTUAL_CLASS(Base)
	int a;
// методы
START_METHOD(Base, Both)
std::cout << "class Base " << "method " << "Both ";
std::cout << this_->a << std::endl;
END_METHOD

START_METHOD(Base, OnlyBase)
std::cout << "class Base " << "method " << "OnlyBase " << std::endl;
END_METHOD

BASE_CONSTRUCTOR(Base,
	ADD_FUNCTION(Base, Both)
	ADD_FUNCTION(Base, OnlyBase)
)
END_CLASS(Base)

// класс-наследник
VIRTUAL_CLASS_DERIVED(Base, Derived)

int b = 1;

// методы
START_METHOD(Derived, Both)
std::cout << "class Base " << "method " << "Both ";
std::cout << this_->b << std::endl;
END_METHOD

START_METHOD(Derived, OnlyDerived)
std::cout << "class Derived " << "method " << "OnlyDerived " << std::endl;
END_METHOD

DERIVED_CONSTRUCTOR(Base, Derived,
	ADD_FUNCTION(Derived, Both)
	ADD_FUNCTION(Derived, OnlyDerived)
)
END_CLASS(Derived)

void main() 
{
	Base base;
	base.a = 0; // работаем как со структурой
	Derived derived;

	// полиморфизм
	Base* reallyDerived = reinterpret_cast<Base*>(&derived);

	VIRTUAL_CALL((&base), Both);
	VIRTUAL_CALL(reallyDerived, Both);
	VIRTUAL_CALL(reallyDerived, OnlyBase);
	VIRTUAL_CALL(reallyDerived, OnlyDerived);
}