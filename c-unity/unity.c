#include <cstring>
#include <vector>
#include <algorithm>
#include <stdio.h>
#include "properties.h"
#include "unity.h"

std::vector<const char*> tags = std::vector<const char*> {"Default"};

template <class T> int indexOf(std::vector<T> arr, T item) {
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

int Tag::AddTag(const char tagName[]) {
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
	this->AddComponent<Transform>();
}

GameObject::GameObject(const char name[], GameObject* parent) {
	strcpy(this->name, name);
	this->AddComponent<Transform>();
    if (parent && parent->transform) {
        this->transform->ReparentTo(parent->transform);
    }
}

template <class T> T* GameObject::AddComponent() {
    T* component = new T();
    if (std::is_same<T, Transform>::value) {
        for (Component* check : this->components) {
            if (check->type_name == component->type_name) {
                printf(
                    "WARNING: Cannot add %s to the GameObject; it already has one\n",
                    typeid(T).name());
                return NULL;
            }
        }
    }
    this->components.push_back(component);
    if (typeid(T) == typeid(Transform)) {
        this->transform = component;
    }
    
    component->gameObject = this;
    component->transform = this->transform;
    return component;
}

Transform::Transform() {}

void Transform::ReparentTo(Transform* parent) {
    if (this->parent) {
        std::vector<Transform*> children_vector = this->parent->children;
        int index = indexOf(children_vector, this);
        if (index != -1) {
            children_vector.erase(children_vector.begin() + index);
        }
    }
    if (parent) {
        parent->children.push_back(this);
        this->parent = parent;
    }
}