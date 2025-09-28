from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
import random


class SnakePart(Widget):
    pass


class Food(Widget):
    pass


class SnakeGame(Widget):
    # Игровые объекты
    snake = ObjectProperty(None)
    food = ObjectProperty(None)

    # Направление движения
    dx = NumericProperty(0)
    dy = NumericProperty(0)
    direction = ReferenceListProperty(dx, dy)

    # Счет
    score = NumericProperty(0)

    # Части змеи
    snake_parts = []

    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self.reset_game()

    def reset_game(self):
        # Очищаем предыдущие части змеи
        for part in self.snake_parts:
            self.remove_widget(part)
        self.snake_parts = []

        # Начальная позиция змеи
        start_x = self.width / 2
        start_y = self.height / 2

        # Создаем голову змеи
        head = SnakePart()
        head.pos = (start_x, start_y)
        self.snake_parts.append(head)
        self.add_widget(head)

        # Добавляем начальные сегменты
        for i in range(1, 3):
            part = SnakePart()
            part.pos = (start_x - 20 * i, start_y)
            self.snake_parts.append(part)
            self.add_widget(part)

        # Сбрасываем счет и направление
        self.score = 0
        self.direction = (20, 0)  # Движение вправо

        # Создаем еду
        if self.food:
            self.remove_widget(self.food)
        self.food = Food()
        self.place_food()
        self.add_widget(self.food)

    def place_food(self):
        # Размещаем еду в случайном месте
        max_x = int(self.width - 20)
        max_y = int(self.height - 20)

        self.food.x = random.randint(0, max_x // 20) * 20
        self.food.y = random.randint(0, max_y // 20) * 20

    def update(self, dt):
        # Двигаем змею
        self.move_snake()

        # Проверяем столкновения
        if self.check_collision():
            self.reset_game()
            return

        # Проверяем, съела ли змея еду
        if self.check_food_collision():
            self.score += 10
            self.place_food()
            self.grow_snake()

    def move_snake(self):
        # Двигаем змею: каждая часть занимает позицию предыдущей
        for i in range(len(self.snake_parts) - 1, 0, -1):
            self.snake_parts[i].pos = self.snake_parts[i - 1].pos

        # Двигаем голову
        head = self.snake_parts[0]
        head.x = (head.x + self.dx) % self.width
        head.y = (head.y + self.dy) % self.height

    def grow_snake(self):
        # Добавляем новый сегмент змеи
        last_part = self.snake_parts[-1]
        new_part = SnakePart()
        new_part.pos = last_part.pos
        self.snake_parts.append(new_part)
        self.add_widget(new_part)

    def check_collision(self):
        # Проверяем столкновение головы с телом
        head = self.snake_parts[0]
        for part in self.snake_parts[1:]:
            if head.pos == part.pos:
                return True
        return False

    def check_food_collision(self):
        # Проверяем, достигла ли голова еды
        head = self.snake_parts[0]
        return (head.x == self.food.x and head.y == self.food.y)

    def on_touch_down(self, touch):
        # Управление касанием (для мобильных устройств)
        head = self.snake_parts[0]

        if touch.x < head.x and abs(self.dx) == 0:
            self.direction = (-20, 0)  # Влево
        elif touch.x > head.x and abs(self.dx) == 0:
            self.direction = (20, 0)  # Вправо
        elif touch.y < head.y and abs(self.dy) == 0:
            self.direction = (0, -20)  # Вниз
        elif touch.y > head.y and abs(self.dy) == 0:
            self.direction = (0, 20)  # Вверх

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None


class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, 1.0 / 10.0)  # 10 FPS

        # Обработка клавиатуры (для тестирования на ПК)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, game)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        return game

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        game = self.root

        if keycode[1] == 'left' and game.dx == 0:
            game.direction = (-20, 0)
        elif keycode[1] == 'right' and game.dx == 0:
            game.direction = (20, 0)
        elif keycode[1] == 'down' and game.dy == 0:
            game.direction = (0, -20)
        elif keycode[1] == 'up' and game.dy == 0:
            game.direction = (0, 20)

        return True


if __name__ == '__main__':
    SnakeApp().run()
