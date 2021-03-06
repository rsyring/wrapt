from __future__ import print_function

import unittest

import wrapt

from wrapt import six

class TestClassInheritence(unittest.TestCase):

    def test_function_type_inheritence(self):
        @wrapt.decorator
        def _decorator(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)

        @_decorator
        def _function(*args, **kwargs):
            return args, kwargs

        self.assertTrue(isinstance(_function, wrapt.FunctionWrapper))
        self.assertTrue(isinstance(_function, wrapt.ObjectProxy))

    def test_instancemethod_type_inheritence(self):
        @wrapt.decorator
        def _decorator(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)

        class Class(object):
            @_decorator
            def function(self, args, **kwargs):
                return args, kwargs

            self.assertTrue(isinstance(function, wrapt.FunctionWrapper))
            self.assertTrue(isinstance(function, wrapt.ObjectProxy))

        instance = Class()

        self.assertFalse(isinstance(instance.function, wrapt.FunctionWrapper))
        self.assertTrue(isinstance(instance.function, wrapt.ObjectProxy))

    def test_classmethod_type_inheritence(self):
        @wrapt.decorator
        def _decorator(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)

        class Class(object):
            @_decorator
            @classmethod
            def function(cls, *args, **kwargs):
                return args, kwargs

            self.assertTrue(isinstance(function, wrapt.FunctionWrapper))
            self.assertTrue(isinstance(function, wrapt.ObjectProxy))

        instance = Class()

        self.assertFalse(isinstance(instance.function, wrapt.FunctionWrapper))
        self.assertTrue(isinstance(instance.function, wrapt.ObjectProxy))

    def test_staticmethod_type_inheritence(self):
        @wrapt.decorator
        def _decorator(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)

        class Class(object):
            @_decorator
            @staticmethod
            def function(*args, **kwargs):
                return args, kwargs

            self.assertTrue(isinstance(function, wrapt.FunctionWrapper))
            self.assertTrue(isinstance(function, wrapt.ObjectProxy))

        instance = Class()

        self.assertFalse(isinstance(instance.function, wrapt.FunctionWrapper))
        self.assertTrue(isinstance(instance.function, wrapt.ObjectProxy))

class TestAttributeAccess(unittest.TestCase):

    def test_function_attributes(self):
        def decorator1(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)
        decorator2 = wrapt.decorator(decorator1)

        def function1(*args, **kwargs):
            return args, kwargs
        function2 = decorator2(function1)

        self.assertEqual(function2.__wrapped__, function1)
        self.assertEqual(function2._self_wrapper, decorator1)
        self.assertNotEqual(function2._self_bound_type, None)

    def test_instancemethod_attributes(self):
        def decorator1(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)
        decorator2 = wrapt.decorator(decorator1)

        class Class(object):
            def function1(self, *args, **kwargs):
                return args, kwargs
            function2 = decorator2(function1)

            self.assertEqual(function2.__wrapped__, function1)
            self.assertEqual(function2._self_wrapper, decorator1)
            self.assertNotEqual(function2._self_bound_type, None)

        instance = Class()

        self.assertEqual(instance.function2.__wrapped__, instance.function1)
        self.assertEqual(instance.function2._self_instance, instance)
        self.assertEqual(instance.function2._self_wrapper, decorator1)

    def test_classmethod_attributes(self):
        def decorator1(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)
        decorator2 = wrapt.decorator(decorator1)

        class Class(object):
            @classmethod
            def function1(cls, *args, **kwargs):
                return args, kwargs
            function2 = decorator2(function1)

            self.assertEqual(function2.__wrapped__, function1)
            self.assertEqual(function2._self_wrapper, decorator1)
            self.assertNotEqual(function2._self_bound_type, None)

        instance = Class()

        self.assertEqual(instance.function2.__wrapped__, instance.function1)
        self.assertEqual(instance.function2._self_instance, instance)
        self.assertEqual(instance.function2._self_wrapper, decorator1)

    def test_staticmethod_attributes(self):
        def decorator1(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)
        decorator2 = wrapt.decorator(decorator1)

        class Class(object):
            @staticmethod
            def function1(*args, **kwargs):
                return args, kwargs
            function2 = decorator2(function1)

            self.assertEqual(function2.__wrapped__, function1)
            self.assertEqual(function2._self_wrapper, decorator1)
            self.assertNotEqual(function2._self_bound_type, None)

        instance = Class()

        self.assertEqual(instance.function2.__wrapped__, instance.function1)
        self.assertEqual(instance.function2._self_instance, instance)
        self.assertEqual(instance.function2._self_wrapper, decorator1)

class TestParentReference(unittest.TestCase):

    def test_function_decorator(self):
        @wrapt.decorator
        def _decorator(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)

        @_decorator
        def function():
            pass

        self.assertEqual(function._self_parent, None)

    def test_class_decorator(self):
        @wrapt.decorator
        def _decorator(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)

        @_decorator
        class Class:
            pass

        self.assertEqual(Class._self_parent, None)

    def test_instancemethod(self):
        @wrapt.decorator
        def _decorator(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)

        class Class:
            @_decorator
            def function_im(self):
                pass

        c = Class()

        self.assertNotEqual(c.function_im._self_parent, None)
        self.assertNotEqual(Class.function_im._self_parent, None)

    def test_classmethod(self):
        @wrapt.decorator
        def _decorator(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)

        class Class:
            @_decorator
            @classmethod
            def function_cm(cls):
                pass

        self.assertNotEqual(Class.function_cm._self_parent, None)

    def test_staticmethod_inner(self):
        @wrapt.decorator
        def _decorator(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)

        class Class:
            @_decorator
            @staticmethod
            def function_sm_inner():
                pass

        self.assertNotEqual(Class.function_sm_inner._self_parent, None)

if __name__ == '__main__':
    unittest.main()
