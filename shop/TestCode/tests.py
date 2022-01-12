from django.test import TestCase
from shop.model.models import Product, Category


# Create your tests here.
class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(
            name='Meat',
            slug='meat'
        ).save()

    def test_category_exists(self):
        category_name = Category.objects.get(id=1).name
        # print("This is the category", category_name)
        self.assertEqual(category_name, 'Meat')


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(
            category=Category.objects.create(name='mangsho', slug='mangsho'),
            name='Chicken',
            slug='chicken',
            description='This is a really good chicken',
            price='20',
            available=True,
        ).save()

    def test_model_created(self):
        product_name = Product.objects.get(id=1)
        product_category_name = Category.objects.get(id=1)
        print("This is the category", product_name)
        print("This is the category", product_category_name)
        self.assertEqual(str(product_name), 'Chicken')
        self.assertEqual(str(product_category_name), 'mangsho')

    def test_model_works(self):
        category_demo = Category.objects.create(name='Meat', slug='meat')
        category_demo.save()
        product_1 = Product.objects.create(
            category=category_demo,
            name='Chicken',
            slug='chicken',
            description='This is a really good chicken',
            price='20',
            available=True,
        )
        product_1.save()
        print(product_1.name)
        self.assertEqual(str(product_1.name), 'Chicken')
        self.assertEqual(str(category_demo.name), 'Meat')

    def test_string_representation(self):
        string_name = Product(name="My entry title")
        self.assertEqual(str(string_name), string_name.name)
