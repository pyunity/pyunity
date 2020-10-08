#ifndef UNITY_H_
#define UNITY_H_

class GameObject;
class Component;
class Transform;

class GameObject {
	public:
		char name[20];
		Transform* transform;
		GameObject(const char name[]);
		GameObject(const char name[], GameObject* parent);
};

class Component {
	public:
		GameObject* gameObject;
		Transform* transform;
};

class Transform : Component {
	public:
		GameObject* gameObject;
		Transform* parent;
		Transform(Transform* parent);
};

#endif