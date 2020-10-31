#include <stdio.h>
#include "unity.h"

int main() {
	GameObject* a = new GameObject("1");
	GameObject* b = new GameObject("2", a);
	printf("%s %s %s\n", a->name, b->name, b->transform->parent->gameObject->name);
	Vector3 vec = Vector3(0, 1, 2);
	printf("Vector3(%f, %f, %f) length=%f\n", vec.x, vec.y, vec.z, vec.length);
	return 0;
}