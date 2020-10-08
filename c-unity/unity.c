#include <cstring>
#include "unity.h"

GameObject::GameObject(const char name[]) {
	strcpy(this->name, name);
}

GameObject::GameObject(const char name[], GameObject* parent) {
	strcpy(this->name, name);
	this->parent = parent;
}