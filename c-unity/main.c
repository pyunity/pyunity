#include <stdio.h>
#include "unity.h"

int main() {
	GameObject* a = new GameObject("1");
	GameObject* b = new GameObject("2", a);
	GameObject* b_parent = b->transform->parent->gameObject;
	printf("%s %s %s", a->name, b->name, b_parent->name);
	return 0;
}