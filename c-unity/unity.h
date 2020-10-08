#ifndef UNITY_H_
#define UNITY_H_

class GameObject {
	public:
		char name[20];
		GameObject* parent;
		GameObject(const char name[]);
		GameObject(const char name[], GameObject* parent);
};

#endif