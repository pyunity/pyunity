#include <stdio.h>
#include "unity.h"

int main() {
	GameObject* a = new GameObject("1");
	GameObject* b = new GameObject("2", a);
	printf("%s %s %d", a->name, b->name, b->transform->parent->gameObject->name);
	return 0;
}