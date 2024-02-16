import json
import os

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Удалите все продукты
        Product.objects.all().delete()
        Category.objects.all().delete()

        data_catagory_1 = Category.objects.create(name="Телевизоры",
                                                  description="У нас любые телевизоры под ваши запросы")
        data_catagory_2 = Category.objects.create(name="Бритвы", description="Бренды бритв из разных точек мира")
        data_catagory_3 = Category.objects.create(name="Планшеты",
                                                  description="Только лучшие планшеты в нашем магазине")

        data_product_1 = Product.objects.create(name="Samsung Телевизор QE50Q60CAUXCE 50 4K UHD, черный",
                                                 description="Телевизор Samsung Q60CAUXCE 65 - это модель телевизора от компании Samsung.\n\nОписание модели:\n\nРазмер экрана: 65 дюймов (диагональ экрана составляет 65 дюймов).\nСерия: Q60CAUXCE. Это может указывать на определенную линейку или модель телевизора в рамках серии Q60CAUXCE.\nПроизводитель: Samsung. Samsung - один из ведущих производителей телевизоров в мире, известный своим качеством и инновациями.\nДополнительные функции: Возможно, этот телевизор имеет различные функции, такие как поддержка высокого разрешения (например, 4K или 8K), подключение к Интернету, смарт-функции, HDR (High Dynamic Range) и другие.",
                                                 category=data_catagory_1, price=76790, created_at="2021-01-10",
                                                 updated_at="2023-05-13",)
        data_product_2 = Product.objects.create(name="Polaris Электробритва PMR 0305R wet&dry Pro 5 blades, черный",
                                                 description="Электрическая бритва Polaris PMR 0305R со встроенным триммером – удобный прибор 2 в 1 для ценителей практичности и функциональности. Оснащена продуманной 4D-системой повторения контуров лица и уникальной конструкцией бритвенной насадки PRO 5 BLADES с супермягкими кольцами для гладкого скольжения без раздражения и плавающей конструкцией лезвий для точного повторения контура подбородка.",
                                                 category=data_catagory_2, price=2699, created_at="2022-02-11",
                                                 updated_at="2022-07-18",)
        data_product_3 = Product.objects.create(name="Планшет Digma Pro PRIME 18 T606 8C/8Gb/256Gb 11",
                                                 description="Планшет Digma Pro PRIME 18 T606 Занимайся тем, что нравится, в своем комфортном пространстве! Стильные планшеты Digma Pro привлекают внимание. Эти тонкие и легкие устройства изготовлены из материалов высочайшего качества. Они выглядят красиво, а вы с ними –эффектно. Погрузитесь в магию кино, насладитесь сервисами потокового вещания Twitch, Netflix, YouYube, VK Play, Kion. Смотрите все любимые шоу и фильмы в идеальном качестве на 11-дюймовом экранe с матрицей IPS, который не имеет себе равных по яркости изображения и точности цветопередачи. Наполните окружающее пространство насыщенным реалистичным звуком благодаря четырем динамикам. Откройте для себя многогранный мир музыкальных передач, видеотрансляций с концертов и фестивалей.",
                                                 category=data_catagory_3, price=13324, created_at="2022-02-11",
                                                 updated_at="2022-07-18",)
        # Удалите все категории

        # Создайте списки для хранения объектов
        product_for_create = [data_product_1, data_product_2, data_product_3]
        category_for_create = [data_catagory_1, data_catagory_2, data_catagory_3]
        #
        # # Обходим все значения категорий из фиктсуры для получения информации об одном объекте

        #
        # 		# Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)
        #
        # 		# Обходим все значения продуктов из фиктсуры для получения информации об одном объекте

        #
        # 		# Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
