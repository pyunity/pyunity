#include <cstring>
#include "unity.h"

GameObject::GameObject(const char name[]) {
	strcpy(this->name, name);
	this->transform = new Transform(NULL);
	this->transform->gameObject = this;
}

GameObject::GameObject(const char name[], GameObject* parent) {
	strcpy(this->name, name);
	this->transform = new Transform(parent->transform);
	this->transform->gameObject = this;
}

Transform::Transform(Transform* parent) {
	this->parent = parent;
}