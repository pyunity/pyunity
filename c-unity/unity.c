#include <cstring>
#include <vector>
#include <algorithm>
#include <cmath>
#include <stdio.h>
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

Vector3::Vector3(float x, float y, float z) {
	this->x = x;
	this->y = y;
	this->z = z;
}
Vector3::Vector3() {
	this->x = 0;
	this->y = 0;
	this->z = 0;
}
bool Vector3::operator==(Vector3 other) {
	return this->x == other.x && this->y == other.y && this->z == other.z;
}
bool Vector3::operator!=(Vector3 other) {
	return this->x != other.x || this->y != other.y || this->z != other.z;
}
Vector3 Vector3::operator+(Vector3 other) {
	return Vector3(this->x + other.x, this->y + other.y, this->z + other.z);
}
Vector3 Vector3::operator+(float val) {
	return Vector3(this->x + val, this->y + val, this->z + val);
}
Vector3 Vector3::operator-(Vector3 other) {
	return Vector3(this->x - other.x, this->y - other.y, this->z - other.z);
}
Vector3 Vector3::operator-(float val) {
	return Vector3(this->x - val, this->y - val, this->z - val);
}
Vector3 Vector3::operator*(Vector3 other) {
	return Vector3(this->x * other.x, this->y * other.y, this->z * other.z);
}
Vector3 Vector3::operator*(float val) {
	return Vector3(this->x * val, this->y * val, this->z * val);
}
Vector3 Vector3::operator/(Vector3 other) {
	return Vector3(this->x / other.x, this->y / other.y, this->z / other.z);
}
Vector3 Vector3::operator/(float val) {
	return Vector3(this->x / val, this->y / val, this->z / val);
}
inline Vector3 operator+(float val, Vector3 vector) {
	return vector + val;
}
inline Vector3 operator-(float val, Vector3 vector) {
	return Vector3(val - vector.x, val - vector.y, val - vector.z);
}
inline Vector3 operator*(float val, Vector3 vector) {
	return vector * val;
}
inline Vector3 operator/(float val, Vector3 vector) {
	return Vector3(val / vector.x, val / vector.y, val / vector.z);
}
Vector3 Vector3::copy() {
	return Vector3(this->x, this->y, this->z);
}
float Vector3::get_length_sqrd() {
	return std::pow(this->x, 2) + std::pow(this->y, 2) + std::pow(this->z, 2);
}
float Vector3::get_length() const {
	return std::sqrt(std::pow(this->x, 2) + std::pow(this->y, 2) + std::pow(this->z, 2));
}
Vector3& Vector3::set_length(float value) {
	float length = this->get_length();
	if (length != 0) {
		this->x *= value / length;
		this->y *= value / length;
		this->z *= value / length;
	}
	return *this;
}
Vector3 Vector3::normalized() {
	float length = this->get_length();
	if (length != 0) {
		float ratio = 1 / length;
		return Vector3(this->x * ratio, this->y * ratio, this->z * ratio);
	} else {
		return Vector3(0, 0, 0);
	}
}
float Vector3::normalize_return_length() {
	float length = this->get_length();
	if (length != 0) {
		this->x /= length;
		this->y /= length;
		this->z /= length;
	}
	return length;
}
float Vector3::get_distance(Vector3 other) {
	return std::sqrt(
		std::pow(this->x - other.x, 2) + std::pow(this->y - other.y, 2) + std::pow(this->y - other.y, 2)
	);
}
float Vector3::get_dist_sqrd(Vector3 other) {
	return (
		std::pow(this->x - other.x, 2) + std::pow(this->y - other.y, 2) + std::pow(this->y - other.y, 2)
	);
}
float Vector3::dot(Vector3 other) {
	return this->x * other.x + this->y + other.y + this->z + other.z;
}
Vector3 Vector3::cross(Vector3 other) {
	float x = this->y * other.z - this->z * other.y;
	float y = this->z * other.x - this->x * other.y;
	float z = this->x * other.y - this->y * other.x;
	return Vector3(x, y, z);
}
Vector3 Vector3::zero() {
	return Vector3(0, 0, 0);
}
Vector3 Vector3::one() {
	return Vector3(1, 1, 1);
}
Vector3 Vector3::left() {
	return Vector3(-1, 0, 0);
}
Vector3 Vector3::right() {
	return Vector3(1, 0, 0);
}
Vector3 Vector3::up() {
	return Vector3(0, 1, 0);
}
Vector3 Vector3::down() {
	return Vector3(0, -1, 0);
}
Vector3 Vector3::forward() {
	return Vector3(0, 0, 1);
}
Vector3 Vector3::back() {
	return Vector3(0, 0, -1);
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
	this->tag = new Tag(0);
}

GameObject::GameObject(const char name[], GameObject* parent) {
	strcpy(this->name, name);
	this->AddComponent<Transform>();
	if (parent && parent->transform) {
		this->transform->ReparentTo(parent->transform);
	}
	this->tag = new Tag(0);
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

template <class T> T* GameObject::GetComponent() {
	Component* test = new T();
	for (Component* component : this->components) {
		if (component->type_name == test->type_name) {
			return component;
		}
	}
	return NULL;
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
	}
	this->parent = parent;
}