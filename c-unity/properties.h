#define PROPERTY_GEN(Class, Type, Name, GetMethod, SetMethod) \
    class Property_##Name { \
    public: \
        Property_##Name(Class* parent) : _parent(parent) { } \
        Type operator = (Type value) \
        { \
            _parent->SetMethod(value); \
            return _parent->GetMethod(); \
        } \
        operator Type() const \
        { \
            return static_cast<const Class*>(_parent)->GetMethod(); \
        } \
        Property_##Name& operator =(const Property_##Name& other) \
        { \
            operator=(other._parent->GetMethod()); return *this; \
        }; \
        Property_##Name(const Property_##Name& other) = delete; \
    private: \
        Class* _parent; \
    } Name { this };


    #define PROPERTY(Class, Type, Name) PROPERTY_GEN(Class, Type, Name, get_##Name, set_##Name)

// template <class T> class Property {
	// private:
		// float getter() const {return 0;};
		// T& setter(float);
		// T& operator=(const float i) {return this->setter();}
		// friend T;
	// public:
		// operator float() const {return this->getter();}
// };
