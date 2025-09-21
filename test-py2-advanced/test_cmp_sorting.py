#!/usr/bin/env python2
"""
Test file specifically for fissix cmp parameter conversion
"""


def custom_compare(a, b):
    """Custom comparison function for sorting"""
    return cmp(a.lower(), b.lower())


def test_cmp_sorting():
    """Test various cmp parameter patterns"""
    print("Testing cmp parameter patterns that need fissix conversion")

    # List of strings to sort
    words = ["Apple", "banana", "Cherry", "date", "Elderberry"]

    # Test 1: sort with cmp parameter
    print("Original list:", words)
    sorted_words = words[:]
    sorted_words.sort(cmp=custom_compare)
    print("Sorted with cmp function:", sorted_words)

    # Test 2: sorted() with cmp parameter
    numbers = [10, 5, 8, 3, 12, 1]

    def reverse_cmp(x, y):
        return cmp(y, x)  # Reverse comparison

    sorted_numbers = sorted(numbers, cmp=reverse_cmp)
    print("Numbers sorted in reverse:", sorted_numbers)

    # Test 3: Complex objects with cmp
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def __repr__(self):
            return "Person('%s', %d)" % (self.name, self.age)

    people = [Person("Alice", 30), Person("Bob", 25), Person("Charlie", 35)]

    def compare_by_age(p1, p2):
        return cmp(p1.age, p2.age)

    people.sort(cmp=compare_by_age)
    print("People sorted by age:", people)

    # Test 4: Multiple cmp usages
    data = [("c", 3), ("a", 1), ("b", 2)]

    def compare_by_second(item1, item2):
        return cmp(item1[1], item2[1])

    data.sort(cmp=compare_by_second)
    print("Tuples sorted by second element:", data)


if __name__ == "__main__":
    test_cmp_sorting()
