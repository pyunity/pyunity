#ifndef UNITY_H_
#define UNITY_H_

#include <string>
#include <vector>

class Tag;
class GameObject;
class Component;
class Transform;

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
        template <class T> T* AddComponent();
};

class Component {
	public:
		GameObject* gameObject;
		Transform* transform;
};

class Transform : public Component {
	public:
		GameObject* gameObject;
        std::vector<Transform*> children;
		Transform* parent;
		Transform();
        void ReparentTo(Transform* parent);
};

#endif