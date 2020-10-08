#include <cstring>
#include <vector>
#include "properties.h"
#include "unity.h"

using namespace std;

vector<string> tags = vector<string> {"Default"};

template <class T> int indexOf(vector<T> arr, T item) {
    auto it = find(arr.begin(), arr.end(), item);
    if (it != arr.end()) {
        return distance(arr.begin(), it);
    } else {
        return -1;
    }
}

Tag::Tag(string tagName) {
    this->tagName = tagName;
    this->tag = indexOf(tags, tagName);
}

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

template <class T> T* GameObject::AddComponent() {
    return new T();
}