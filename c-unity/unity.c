#include <cstring>
#include <vector>
#include <algorithm>
#include "properties.h"
#include "unity.h"

using namespace std;

vector<const char*> tags = vector<const char*> {"Default"};

template <class T> int indexOf(vector<T> arr, T item) {
    auto it = find(arr.begin(), arr.end(), item);
    if (it != arr.end()) {
        return distance(arr.begin(), it);
    } else {
        return -1;
    }
}

Tag::Tag(const char tagName[]) {
    strcpy(this->tagName, tagName);
    this->tag = indexOf(tags, tagName);
}

Tag::Tag(int tagNum) {
    this->tag = tagNum;
    strcpy(this->tagName, tags[tagNum]);
}

static int Tag::AddTag(const char tagName[]) {
	int idx = indexOf(tags, tagName);
	if (idx == -1) {
		tags.push_back(tagName);
		return indexOf(tags, tagName);
	} else {
		return idx;
	}
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