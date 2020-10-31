#ifndef UNITY_H_
#define UNITY_H_

#include <string>
#include <vector>

class Vector3;
class Tag;
class GameObject;
class Component;
class Transform;

template<typename T, typename C>
class Property{
public:
  using SetterType = C& (C::*)(T);
  using GetterType = T (C::*)() const;

  Property(C* theObject, SetterType theSetter, GetterType theGetter)
   :itsObject(theObject),
    itsSetter(theSetter),
    itsGetter(theGetter)
    { }

  operator T() const
    { return (itsObject->*itsGetter)(); }

  C& operator = (T theValue) {
    return (itsObject->*itsSetter)(theValue);
  }

private:
  C* const itsObject;
  SetterType const itsSetter;
  GetterType const itsGetter;
};

class Vector3 {
	public:
		float x, y, z;
		Vector3(float, float, float);
		Vector3(Vector3&&);
		Vector3();
		bool operator==(Vector3);
		bool operator!=(Vector3);
		Vector3 operator+(Vector3);
		Vector3 operator+(float);
		Vector3 operator-(Vector3);
		Vector3 operator-(float);
		Vector3 operator*(Vector3);
		Vector3 operator*(float);
		Vector3 operator/(Vector3);
		Vector3 operator/(float);
		Vector3 copy();
		float get_length_sqrd();
		float get_length() const;
		Vector3& set_length(float);
		Property<float, Vector3> length = Property<float, Vector3>(this,&Vector3::set_length,&Vector3::get_length);
		Vector3 normalized();
		float normalize_return_length();
		float get_distance(Vector3 other);
		float get_dist_sqrd(Vector3 other);
		float dot(Vector3 other);
		Vector3 cross(Vector3 other);
		static Vector3 zero();
		static Vector3 one();
		static Vector3 left();
		static Vector3 right();
		static Vector3 up();
		static Vector3 down();
		static Vector3 forward();
		static Vector3 back();
};

class Tag {
    public:
        char tagName[20];
        int tag;
        Tag(const char tagName[]);
        Tag(int tagNum);
		static int AddTag(const char tagName[]);
};

class GameObject {
	public:
		char name[20];
        std::vector<Component*> components;
		Transform* transform;
		GameObject(const char name[]);
		GameObject(const char name[], GameObject* parent);
		Tag* tag;
        template <class T> T* AddComponent();
        template <class T> T* GetComponent();
};

class Component {
	public:
		static constexpr const char* const type_name = "Component";
		GameObject* gameObject;
		Transform* transform;
};

class Transform : public Component {
	public:
		static constexpr const char* const type_name = "Transform";
		GameObject* gameObject;
        std::vector<Transform*> children;
		Transform* parent;
		Vector3 localPosition;
		Vector3 localScale;
		Transform();
        void ReparentTo(Transform* parent);
};

#endif