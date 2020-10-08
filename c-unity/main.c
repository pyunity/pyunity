#include <stdio.h>
#include "unity.h"

int main() {
	GameObject* a = new GameObject("1");
	GameObject* b = new GameObject("2", a);
	printf("%s %s %s", a->name, b->name, b->parent->name);
}