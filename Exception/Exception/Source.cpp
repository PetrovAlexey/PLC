#include <csetjmp>
#include <cstdlib>
#include <cassert>
#include <iostream>
// Класс от которого все должно наследоваться
class CNode {
private:
	CNode *prev; // Указатель на предыдущ. элемент
public:
	CNode();
	virtual ~CNode();
	void SetPrev(CNode *object); // Добавляем предыдущий элемент
	CNode *GetPrev(); // Получить предыдущий элемент
	void Logout(); // Удалиться
};

class CJmpMaster {
private:
	CJmpMaster *prev;
	CNode *object;
public:
	jmp_buf env;

	CJmpMaster();
	virtual ~CJmpMaster();

	CNode *GetObject();
	void SetObject(CNode *object_);
	CJmpMaster *GetPrev();
};

CJmpMaster *master = nullptr; // Создаем изначальный блок

CNode::CNode() {
	if (master != nullptr) {

		this->SetPrev(master->GetObject());

		master->SetObject(this);
	}
}

CNode::~CNode() {
	this->Logout();
}

void CNode::Logout() {
	if (master != nullptr && prev != nullptr) {
		master->SetObject(prev);
		prev = nullptr;
	}
}

void CNode::SetPrev(CNode *obj) {
	prev = obj;
}

CNode *CNode::GetPrev() {
	return prev;
}

CJmpMaster::CJmpMaster() {
	object = nullptr;
	prev = master;
	master = this;
}

CJmpMaster::~CJmpMaster() {
	master = prev;
}

CNode *CJmpMaster::GetObject() {
	return master->object;
}

void CJmpMaster::SetObject(CNode *obj) {
	object = obj;
}

CJmpMaster *CJmpMaster::GetPrev() {
	return prev;
}

//определяем исключения
#define LocalException '1'
#define LogicException '2'
#define Exception '3'

//Для простоты, будем бросать только исключения типа const char *
void Throw(const char *id);

bool deleting = false;
bool catched = true;

#define TRY {\
  CJmpMaster slave;\
  char *exc;\
  int env = setjmp(slave.env);\
  if (env == 1) {\
    char exc_ = '1';\
    exc = &exc_;\
	std::cout << "Throw "<<exc[0]<< std::endl;\
  } \
  if (env == 2) {\
    char exc_ = '2';\
    exc = &exc_;\
	std::cout << "Throw "<<exc[0]<< std::endl;\
  } \
  if (env == 3) {\
    char exc_ = '3';\
    exc = &exc_;\
	std::cout << "Throw "<<exc[0]<< std::endl;\
  } \
  if (env == 0) {

#define CATCH(type)\
  } else if ((type == exc[0]) || (type == '3')) {\
	  std::cout << "Catching"<<type<< std::endl;\
      catched = true;

#define FINALLY\
    }\
  if (catched == false) {\
    std::cout << "No handle for this exception. Program terminating..." << std::endl;\
    exit(-1);\
  }\
  }

#define THROW(type)\
  catched = false;\
  Throw(type);

#define RETHROW_IN_BLOCK  \
  Throw(exc[0]);

void Throw(const char id) {
	if (master == nullptr) {
		std::cout << "Exception thrown outside try-catch block. Program terminating..." << std::endl;
		exit(-1);
	}

	if (deleting) {
		std::cout << "Some Exception thrown during another called. Program terminating..." << std::endl;
		exit(-1);
	}

	CJmpMaster *tmp = master;
	CNode *object = master->GetObject();

	// Удаляем объекты со стека
	deleting = true;
	while (object != nullptr) {
		CNode *objectBuf = object;
		object = object->GetPrev();
		objectBuf->~CNode();
	}
	deleting = false;

	// Меняем текующий стек
	CJmpMaster *fake = master;
	assert(fake != nullptr);
	master = fake->GetPrev();
	int result = 0;
	if (LocalException == id) {
		result = 1;
	} else if (LogicException == id) {
		result = 2;
	}
	else {
		result = 3;
	}
	longjmp(tmp->env, result);
}


class _A : public CNode {
public:
	_A() :val_(0) { std::cout << "A::A(" << val_ << ")\n"; }
	_A(int i) :val_(i) { std::cout << "A::A(" << val_ << ")\n"; }
	virtual ~_A() { std::cout << "A::~A(" << val_ << ")\n";
	}
private:
	int val_;
};

// Пример проброса исключения
int main() {
	_A a(1);
	TRY{
		TRY{
			_A b(2);
		THROW(LocalException);
		std::cout << "Donottogoto" << std::endl;
		}
		CATCH(LocalException) {
			std::cout << "Catched number"  << LocalException << " Exception" << std::endl;
			RETHROW_IN_BLOCK
		}
		FINALLY;
	}
		CATCH(Exception) {
		std::cout << "Catched any Exception" << std::endl;
	}
	FINALLY;
	return 0;
}
