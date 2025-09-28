from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Triangle
from random import randint


class ImprovedGame(Widget):
    score = NumericProperty(0)
    level = NumericProperty(1)

    def __init__(self, **kwargs):
        super(ImprovedGame, self).__init__(**kwargs)

        self.enemies = []
        self.bullets = []
        self.game_over = False
        self.ship_x = self.center_x - 25
        self.ship_size = 50

        self.setup_graphics()
        self.setup_ui()

        # Запуск игры
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.add_enemy, 1.0)

        print("Космический защитник запущен!")

    def setup_graphics(self):
        # Фон
        with self.canvas:
            Color(0, 0, 0.3)
            Rectangle(pos=self.pos, size=self.size)

        # Корабль
        with self.canvas:
            Color(0, 0.8, 1)
            self.ship_graphics = Triangle()

    def setup_ui(self):
        # Счет и уровень
        self.score_label = Label(
            text='Счет: 0',
            pos=(10, self.height - 40),
            font_size='20sp',
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.score_label)

        self.level_label = Label(
            text='Уровень: 1',
            pos=(10, self.height - 80),
            font_size='20sp',
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.level_label)

        # Инструкция
        self.help_label = Label(
            text='Двигайте мышью и кликайте для стрельбы',
            pos=(self.center_x - 150, 10),
            font_size='16sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        self.add_widget(self.help_label)

    def update_ship(self):
        self.ship_graphics.points = [
            self.ship_x, 10,
            self.ship_x + self.ship_size, 10,
            self.ship_x + self.ship_size / 2, 10 + self.ship_size
        ]

    def on_size(self, *args):
        self.canvas.clear()
        self.setup_graphics()
        self.update_ship()

        # Обновляем UI
        self.score_label.pos = (10, self.height - 40)
        self.level_label.pos = (10, self.height - 80)
        self.help_label.pos = (self.center_x - 150, 10)

    def on_touch_move(self, touch):
        if not self.game_over:
            self.ship_x = touch.x - self.ship_size / 2
            # Ограничение движения в пределах экрана
            if self.ship_x < 0:
                self.ship_x = 0
            if self.ship_x > self.width - self.ship_size:
                self.ship_x = self.width - self.ship_size
            self.update_ship()

    def on_touch_down(self, touch):
        if not self.game_over:
            self.shoot()
        else:
            # Если игра окончена, тап перезапускает игру
            self.restart_game()

    def shoot(self):
        if len(self.bullets) < 5:  # Максимум 5 пуль
            bullet_x = self.ship_x + self.ship_size / 2 - 2
            self.bullets.append({'x': bullet_x, 'y': 60, 'speed': 12})

            # Звуковой эффект (в консоли)
            print("Пиу!")

    def add_enemy(self, dt):
        if not self.game_over and len(self.enemies) < 10:  # Максимум 10 врагов
            enemy_speed = 2 + (self.level * 0.5)  # Увеличиваем скорость с уровнем
            x = randint(20, self.width - 60)
            self.enemies.append({
                'x': x,
                'y': self.height,
                'speed': enemy_speed,
                'size': randint(30, 50)
            })

    def update(self, dt):
        if self.game_over:
            return

        # Обновляем уровень каждые 100 очков
        self.level = (self.score // 100) + 1
        self.level_label.text = f'Уровень: {self.level}'

        # Движение пуль
        new_bullets = []
        for bullet in self.bullets:
            bullet['y'] += bullet['speed']
            if bullet['y'] < self.height:
                new_bullets.append(bullet)
        self.bullets = new_bullets

        # Движение врагов
        new_enemies = []
        for enemy in self.enemies:
            enemy['y'] -= enemy['speed']
            if enemy['y'] > 0:
                new_enemies.append(enemy)
            else:
                # Враг достиг низа - игра окончена
                self.game_over = True
                self.show_game_over()
                return
        self.enemies = new_enemies

        # Проверяем столкновения
        self.check_collisions()

        # Перерисовываем графику
        self.redraw()

    def check_collisions(self):
        bullets_to_remove = []
        enemies_to_remove = []

        for i, bullet in enumerate(self.bullets):
            for j, enemy in enumerate(self.enemies):
                if (abs(bullet['x'] - enemy['x']) < 25 and
                        abs(bullet['y'] - enemy['y']) < 30):
                    bullets_to_remove.append(i)
                    enemies_to_remove.append(j)
                    self.score += 10
                    self.score_label.text = f'Счет: {self.score}'
                    print("Враг уничтожен! +10 очков")

        # Удаляем столкнувшиеся объекты
        for i in sorted(bullets_to_remove, reverse=True):
            if i < len(self.bullets):
                self.bullets.pop(i)
        for j in sorted(enemies_to_remove, reverse=True):
            if j < len(self.enemies):
                self.enemies.pop(j)

    def redraw(self):
        self.canvas.clear()

        # Фон
        with self.canvas:
            Color(0, 0, 0.3)
            Rectangle(pos=self.pos, size=self.size)

            # Корабль
            Color(0, 0.8, 1)
            self.ship_graphics = Triangle(points=[
                self.ship_x, 10,
                self.ship_x + self.ship_size, 10,
                self.ship_x + self.ship_size / 2, 10 + self.ship_size
            ])

            # Пули
            Color(1, 1, 0)
            for bullet in self.bullets:
                Rectangle(pos=(bullet['x'], bullet['y']), size=(4, 20))

            # Враги (разного цвета в зависимости от размера)
            for enemy in self.enemies:
                if enemy['size'] > 40:
                    Color(1, 0, 0)  # Большой - красный
                else:
                    Color(1, 0.5, 0)  # Маленький - оранжевый

                Rectangle(
                    pos=(enemy['x'], enemy['y']),
                    size=(enemy['size'], enemy['size'])
                )

    def show_game_over(self):
        self.game_over = True

        # Затемняем экран
        with self.canvas:
            Color(0, 0, 0, 0.7)
            Rectangle(pos=self.pos, size=self.size)

        # Сообщение о Game Over
        game_over_label = Label(
            text=f'ИГРА ОКОНЧЕНА!\nВаш счет: {self.score}',
            pos=(self.center_x - 100, self.center_y + 50),
            font_size='24sp',
            color=(1, 0, 0, 1)
        )
        self.add_widget(game_over_label)

        # Кнопка перезапуска
        restart_btn = Button(
            text='НОВАЯ ИГРА',
            size=(200, 60),
            pos=(self.center_x - 100, self.center_y - 30),
            background_color=(0, 0.7, 0, 1),
            font_size='18sp'
        )
        restart_btn.bind(on_press=self.restart_game)
        self.add_widget(restart_btn)

    def restart_game(self, instance=None):
        # Удаляем UI элементы игры
        for child in self.children[:]:
            if isinstance(child, (Label, Button)) and child not in [self.score_label, self.level_label,
                                                                    self.help_label]:
                self.remove_widget(child)

        # Сбрасываем состояние игры
        self.score = 0
        self.level = 1
        self.bullets = []
        self.enemies = []
        self.game_over = False

        # Обновляем labels
        self.score_label.text = 'Счет: 0'
        self.level_label.text = 'Уровень: 1'

        # Перерисовываем
        self.redraw()
        print("Новая игра началась!")


class ImprovedSpaceApp(App):
    def build(self):
        return ImprovedGame()


if __name__ == '__main__':
    ImprovedSpaceApp().run()

