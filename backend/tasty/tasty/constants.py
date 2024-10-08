# Models
NAME_MAX_LENGTH: int = 256
MEASUREMENT_UNIT_MAX_LENGTH: int = 64
MIN_COOKING_TIME: int = 1
MAX_COOKING_TIME: int = 32000
MIN_COOKING_TIME_ERROR: str = (f'Время приготовления не может быть '
                               f'меньше {MIN_COOKING_TIME}.')
MAX_COOKING_TIME_ERROR: str = (f'Время приготовления не может быть '
                               f'больше {MAX_COOKING_TIME} минуты.')
MIN_AMOUNT: int = 1
MAX_AMOUNT: int = 32000
MIN_AMOUNT_ERROR: str = (f'Количество ингредиента не может быть '
                         f'меньше {MIN_AMOUNT}.')
MAX_AMOUNT_ERROR: str = (f'Количество ингредиента не может быть '
                         f'больше {MAX_AMOUNT}.')

# Core
INGREDIENTS_DATA_REQUIRED: str = ('Ингредиенты '
                                  'обязательны для создания рецепта.')
TAGS_DATA_REQUIRED: str = 'Теги обязательны для создания рецепта.'
AMOUNT_REQUIRED: str = ('Количество ингредиента '
                        'обязательно для создания рецепта.')
COOKING_TIME_REQUIRED: str = ('Время приготовления рецепта '
                              'обязательно для создания рецепта.')
INGREDIENT_DUPLICATES: str = 'Ингредиенты должны быть уникальными: {}.'
TAG_DUPLICATES: str = 'Теги должны быть уникальными: {}.'
INGREDIENT_DOES_NOT_EXIST: str = 'Ингредиент "{ingredient_id}" не существует.'
TAG_DOES_NOT_EXIST: str = 'Тег "{tag_id}" не существует.'

# Favorites
FAVORITES_NOT_FOUND: str = 'Рецепта нет в избранном.'
FAVORITES_ALREADY_EXISTS: str = 'Рецепт уже в избранном.'

# Shopping list
SHOPPING_LIST_EMPTY: str = 'Список покупок пуст.'
SHOPPING_LIST_NOT_FOUND: str = 'Рецепта нет в списке покупок.'
SHOPPING_LIST_ALREADY_EXISTS: str = 'Рецепт уже в списке покупок.'
SHOPPING_LIST_TXT_FILENAME: str = 'shopping_cart.txt'
SHOPPING_LIST_PDF_FILENAME: str = 'shopping_cart.pdf'

# Subscriptions
SELF_SUBSCRIPTION_ERROR: str = 'Вы не можете подписаться на себя.'
SUBSCRIPTION_ALREADY_EXISTS: str = 'Подписка уже существует.'
SUBSCRIPTION_NOT_FOUND: str = 'Вы не подписаны.'

# Users
NOT_AUTHENTICATED: str = 'Войдите в аккаунт для совершения этого действия.'

# Import
IMPORT_INGREDIENTS_FROM_CSV: str = 'Импортировать ингредиенты из CSV.'
IMPORT_INGREDIENTS_FROM_JSON: str = 'Импортировать ингредиенты из JSON.'
JSON_INVALID: str = 'Файл {file_path} не является валидным JSON.'
FILE_PATH: str = 'Путь к файлу.'
FILE_DOES_NOT_EXIST: str = 'Файл "{file_path}" не существует.'
IMPORT_SUCCESS: str = 'Ингредиент "{name}" успешно импортирован.'
INGREDIENT_EXISTS: str = 'Ингредиент "{name}" уже существует.'
