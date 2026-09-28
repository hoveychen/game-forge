# "Dark Camp" — Diablo-2-like isometric pixel-art prototype in pure C + raylib, Claude Code (Opus 4.6) agent team

- Repo: https://github.com/senior-sigan/game-v2-ai-slop  (web build: http://senior-sigan.ru/game-v2-ai-slop/)
- Stars: 0 — evidence is weak on popularity, strong on method. Author explicitly calls it a prototype ("ai-slop" in name, self-deprecating).
- Tool/model: Claude Code, Opus 4.6, "no skills other than Claude Code's built-in"; multi-agent team (agent teams / TaskUpdate).
- Genre: top-down isometric action RPG prototype (warrior, skeletons/zombies/liches, safe campfire hub, forest + graveyard)
- Result evidence: playable web (emscripten) build; 27/27 Lua tests passing; ASan/UBSan clean; 21 generated sprite PNGs; 20 commits. README: "Without raylib_tester the quality of the games is very poor" (author's key claim — this is his second attempt, v2).
- One-shot vs multi-session: one main prompt + 5 short follow-ups in one session (agent team).
- Notable process practices:
  - Custom stb-style `raylib_tester.h` + `test.lua`: game binary run with a Lua script injects simulated keys/mouse, reads registered game variables, takes screenshots → the agent can "play" and see the game. This is the author's central finding.
  - Offline API docs in docs/raylib/*.txt with CLAUDE.md line "Prefer retrieval-led reasoning over pre-training-led reasoning" (anti-hallucination for C API).
  - Role-split agent team: game designer writes GDD and "watches the result", testers via raylib_tester, pure-C devs, code-reviewer/architect; team lead does not write code.
  - clang-tidy with all warnings as errors; zero-malloc static arrays.
  - Retrospective written by the agents into docs/RETROSPECTIVE.md with rules for next time. Key failure: sprites were generated but never integrated — the lead marked "create sprites" done while the game still drew circles; the *user* noticed. Lesson: always pair asset-creation tasks with integration tasks; verify deliverables by screenshot, not by the agent's word; requirement changes must go into the task description, not just chat messages.
  - Retro also credits "GDD with concrete numbers (HP, speeds, RGB colors, pixel sizes) let developers work without further questions."

---
## Verbatim prompts (from README; Russian original + English translation)

Original:
## Промпты

Модель: opus 4.6.
Никаких скилов, кроме базовых от claude code.

> Сделай игру на подобии diablo 2, чтобы можно было бегать за персонажа воина с мечом. Из врагов будут скелеты, зомби, личи. Сеттинг - какой-то темный фентези, лагерь в котором безопасно возле костра. Вокруг лес кладбище. Это прототип поэтому больше геймплея не надо. Вид сверху в изометрии, пиксель арт. Запускай работу в несколько агентов: геймдизайнер напишет дизайн документ и будет следаить за результатом, тестировщики которые проверяют игру через raylib_tester.h, разработчики pure C raylib developers, код ревьюер архитектор. Тимлид код не пишет, только координирует работу. Делай коммиты регулярно.

> Запусти параллельно дизайнера-иллюстратора, чтобы он подготовил спрайты вместе с геймдизайнером.

> У спрайтов должны быть анимации (бега, атаки, idle -анимация из 4-8 фреймов. Пусть иллюстратор это учтет

> Спрайты объектов мелкие, а вот деревья могут быть больше - 32x32 пиксселя.

> А ассеты которые иллюстратор создал будут применены в игре вместе с анимациями?

> Проведи потом ретроспективу между агентами и запиши уроки в отдельный файл чтобы в будущем процессы шли намного лучше.

English translation (by collector):
> Make a game similar to Diablo 2 where you can run around as a warrior with a sword. Enemies: skeletons, zombies, liches. Setting: dark fantasy, a camp where it's safe near the campfire. Around it a forest and a graveyard. This is a prototype, so no more gameplay than that. Top-down isometric view, pixel art. Run the work with several agents: a game designer writes the design document and watches over the result, testers who check the game via raylib_tester.h, pure C raylib developers, a code reviewer/architect. The team lead does not write code, only coordinates. Commit regularly.
> Launch in parallel a designer-illustrator so they prepare sprites together with the game designer.
> Sprites should have animations (run, attack, idle — 4–8 frames). Let the illustrator account for this.
> Object sprites are small, but trees can be larger — 32x32 pixels.
> Will the assets the illustrator created be applied in the game along with animations?
> Afterwards run a retrospective between the agents and write the lessons into a separate file so that future processes go much better.

---
## Verbatim: CLAUDE.md
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Raylib docs

[Raylib API Docs Index]|root: docs/raylib|IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning|Raylib version: 5.5|api:{INDEX.md,01_defines.txt,02_structs.txt,03_enums.txt,04_core_window.txt,05_input.txt,06_shapes.txt,07_textures.txt,08_text.txt,09_models.txt,10_audio.txt}

## Build Commands

```bash
make build          # cmake configure + build
make test           # build + run with test.lua
make run            # run without test script
make tidy           # clang-tidy (all warnings are errors)
make clean          # rm -rf build
```

Binary: `./build/Game [script.lua]` — with Lua script runs test mode, without runs normal game.


---
## Verbatim: test.lua (agent-written playtest script)
```lua
-- Dark Camp — Lua integration tests

function test()
    -- Wait for initialization and first frame
    coroutine.yield(0.2)

    ----------------------------------------------------------------
    -- Test 1: Initial player state
    ----------------------------------------------------------------
    game.take_screenshot("01_initial_state.png")

    local start_x = game.get_var("player_x")
    local start_y = game.get_var("player_y")
    local start_hp = game.get_var("player_hp")
    local start_kills = game.get_var("player_kills")

    game.assert_near(start_x, 15.0, 1.0, "player starts near center X (15.0)")
    game.assert_near(start_y, 15.0, 1.0, "player starts near center Y (15.0)")
    game.assert_eq(start_hp, 100.0, "player starts with full HP (100)")
    game.assert_eq(start_kills, 0, "player starts with 0 kills")

    ----------------------------------------------------------------
    -- Test 2: Enemies are spawned
    ----------------------------------------------------------------
    local enemies = game.get_var("enemy_count")
    game.assert_true(enemies >= 0, "enemy_count should be non-negative")

    ----------------------------------------------------------------
    -- Test 3: Movement — D key (iso: x increases, y decreases)
    ----------------------------------------------------------------
    local before_d_x = game.get_var("player_x")
    local before_d_y = game.get_var("player_y")

    game.key_down(game.KEY_D)
    coroutine.yield(0.5)
    game.key_up(game.KEY_D)
    coroutine.yield(0.05)

    local after_d_x = game.get_var("player_x")
    local after_d_y = game.get_var("player_y")
    game.assert_true(after_d_x > before_d_x, "D key should increase player X (iso right)")
    game.assert_true(after_d_y < before_d_y, "D key should decrease player Y (iso right)")
    game.take_screenshot("02_after_move_D.png")

    ----------------------------------------------------------------
    -- Test 4: Movement — A key (iso: x decreases, y increases)
    ----------------------------------------------------------------
    local before_a_x = game.get_var("player_x")
    local before_a_y = game.get_var("player_y")

    game.key_down(game.KEY_A)
    coroutine.yield(0.5)
    game.key_up(game.KEY_A)
    coroutine.yield(0.05)

    local after_a_x = game.get_var("player_x")
    local after_a_y = game.get_var("player_y")
    game.assert_true(after_a_x < before_a_x, "A key should decrease player X (iso left)")
    game.assert_true(after_a_y > before_a_y, "A key should increase player Y (iso left)")

    ----------------------------------------------------------------
    -- Test 5: Movement — W key (iso: x decreases, y decreases)
    ----------------------------------------------------------------
    local before_w_x = game.get_var("player_x")
    local before_w_y = game.get_var("player_y")

    game.key_down(game.KEY_W)
    coroutine.yield(0.5)
    game.key_up(game.KEY_W)
    coroutine.yield(0.05)

    local after_w_x = game.get_var("player_x")
    local after_w_y = game.get_var("player_y")
    game.assert_true(after_w_x < before_w_x, "W key should decrease player X (iso up)")
    game.assert_true(after_w_y < before_w_y, "W key should decrease player Y (iso up)")
    game.take_screenshot("03_after_move_W.png")

    ----------------------------------------------------------------
    -- Test 6: Movement — S key (iso: x increases, y increases)
    ----------------------------------------------------------------
    local before_s_x = game.get_var("player_x")
    local before_s_y = game.get_var("player_y")

    game.key_down(game.KEY_S)
    coroutine.yield(0.5)
    game.key_up(game.KEY_S)
    coroutine.yield(0.05)

    local after_s_x = game.get_var("player_x")
    local after_s_y = game.get_var("player_y")
    game.assert_true(after_s_x > before_s_x, "S key should increase player X (iso down)")
    game.assert_true(after_s_y > before_s_y, "S key should increase player Y (iso down)")

    ----------------------------------------------------------------
    -- Test 7: Player returns near start after opposite movements
    ----------------------------------------------------------------
    local return_x = game.get_var("player_x")
    local return_y = game.get_var("player_y")
    game.assert_near(return_x, start_x, 2.0, "player should be near start X after D+A+W+S")
    game.assert_near(return_y, start_y, 2.0, "player should be near start Y after D+A+W+S")

    ----------------------------------------------------------------
    -- Test 8: Diagonal movement (W+D simultaneously)
    ----------------------------------------------------------------
    local before_diag_x = game.get_var("player_x")
    local before_diag_y = game.get_var("player_y")

    game.key_down(game.KEY_W)
    game.key_down(game.KEY_D)
    coroutine.yield(0.5)
    game.key_up(game.KEY_W)
    game.key_up(game.KEY_D)
    coroutine.yield(0.05)

    local after_diag_x = game.get_var("player_x")
    local after_diag_y = game.get_var("player_y")
    -- W: x-1,y-1; D: x+1,y-1 → combined: x stays ~same, y decreases
    game.assert_near(after_diag_x, before_diag_x, 0.5, "W+D diagonal: X should stay ~same")
    game.assert_true(after_diag_y < before_diag_y, "W+D diagonal: Y should decrease")

    ----------------------------------------------------------------
    -- Test 9: Return to center for camp regen test
    ----------------------------------------------------------------
    -- Move back with S+A (opposite of W+D) to return near center
    game.key_down(game.KEY_S)
    game.key_down(game.KEY_A)
    coroutine.yield(0.5)
    game.key_up(game.KEY_S)
    game.key_up(game.KEY_A)
    coroutine.yield(0.05)

    ----------------------------------------------------------------
    -- Test 10: Camp HP regeneration
    ----------------------------------------------------------------
    -- Player should be in camp zone (near 15,15). HP should be at max.
    local camp_hp = game.get_var("player_hp")
    game.assert_true(camp_hp > 0, "player should be alive in camp")
    game.assert_true(camp_hp <= 100.0, "HP should not exceed max (100)")

    ----------------------------------------------------------------
    -- Test 11: Sword attack (LMB)
    ----------------------------------------------------------------
    local kills_before = game.get_var("player_kills")

    -- Set mouse position and press left button to attack
    game.set_mouse_pos(500, 300)
    game.mouse_press(game.MOUSE_LEFT)
    coroutine.yield(0.1)
    game.take_screenshot("04_attack_swing.png")

```


---
## Verbatim: docs/GDD.md (agent-written, full)
# Game Design Document: Dark Camp

## 1. Концепция

- **Жанр:** Action RPG, вид сверху, изометрическая проекция
- **Сеттинг:** Тёмное фэнтези, вдохновлённое Diablo 2
- **Платформа:** Desktop (raylib, C)
- **Разрешение окна:** 800×600 пикселей
- **Визуальный стиль:** Пиксель-арт через геометрические примитивы
- **Целевой FPS:** 60
- **Статус:** Прототип — минимум механик, максимум атмосферы

## 2. Игровой мир

### 2.1. Карта

- **Размер карты:** 50×50 тайлов (1600×1600 пикселей в экранных координатах)
- **Размер тайла:** 32×32 пикселей (в изометрии: 64×32 — ромб с соотношением 2:1)
- **Проекция:** Изометрическая (2:1 ratio)
  - Экранный X = (tileX - tileY) × 32
  - Экранный Y = (tileX + tileY) × 16
- **Камера:** Следует за игроком, центрирует его на экране

### 2.2. Зоны карты

#### Лагерь (безопасная зона)
- **Расположение:** Центр карты, тайлы [23..27, 23..27] (5×5 тайлов)
- **Особенности:**
  - Костёр в центре (тайл [25, 25])
  - Враги НЕ могут входить в эту зону
  - Игрок регенерирует HP находясь в лагере: +5 HP/сек
- **Визуал:** Земляной пол (коричневые тайлы), камни по периметру

#### Кладбище / Тёмный лес
- **Расположение:** Всё остальное пространство карты вокруг лагеря
- **Наполнение:**
  - Надгробия: ~20 штук, случайно расставлены (серые прямоугольники 8×12 px)
  - Деревья: ~30 штук, расставлены кластерами (являются препятствиями)
  - Кости на земле: декоративные элементы (белые точки 2×2 px)
- **Визуал:** Тёмно-зелёная трава, серые участки кладбищенской земли

### 2.3. Тайлы

| Тип тайла      | Цвет (RGB)          | Проходимость | Описание                     |
|-----------------|----------------------|--------------|------------------------------|
| Трава           | (34, 60, 34)        | Да           | Основной тайл леса           |
| Кладбище        | (80, 80, 70)        | Да           | Серая земля с надгробиями    |
| Лагерь          | (100, 70, 40)       | Да           | Земляной пол безопасной зоны |
| Дерево          | (20, 40, 20)        | Нет          | Непроходимый тайл            |
| Стена (граница) | (10, 10, 10)        | Нет          | Край карты                   |

## 3. Персонаж игрока

### 3.1. Характеристики

| Параметр         | Значение              |
|------------------|-----------------------|
| HP               | 100                   |
| Макс. HP         | 100                   |
| Скорость         | 120 пикселей/сек      |
| Урон мечом       | 25                    |
| Радиус атаки     | 40 пикселей           |
| Кулдаун атаки    | 0.5 сек               |
| Регенерация (лагерь) | +5 HP/сек        |
| Размер хитбокса  | 16×16 пикселей        |

### 3.2. Управление

| Действие            | Ввод                              |
|---------------------|-----------------------------------|
| Движение вверх      | W                                 |
| Движение влево      | A                                 |
| Движение вниз       | S                                 |
| Движение вправо     | D                                 |
| Атака мечом         | Левый клик мыши                   |
| Направление атаки   | Позиция курсора мыши              |

- Поддерживается **8 направлений** движения (диагонали при одновременном нажатии двух клавиш)
- При диагональном движении скорость нормализуется (120 / √2 ≈ 85 px/s по каждой оси)

### 3.3. Визуал игрока

- **Тело:** Зелёный прямоугольник 14×16 px, цвет (0, 180, 0)
- **Меч:** Белая линия 12 px длиной, цвет (240, 240, 240)
  - Меч вращается в направлении курсора
  - При атаке — анимация взмаха (дуга 90° за 0.2 сек)

## 4. Враги

### 4.1. Общие правила

- Враги патрулируют свою зону (случайное блуждание с радиусом 80 px от точки спавна)
- При обнаружении игрока (вход в агро-радиус) — преследуют игрока
- Теряют агро если игрок отошёл дальше чем агро-радиус × 1.5
- Враги **НЕ заходят** в безопасную зону лагеря — останавливаются на границе
- При смерти — респавн через 5 сек в случайной точке кладбища (не ближе 100 px к лагерю)
- **Начальное количество:** 8 скелетов, 4 зомби, 3 лича

### 4.2. Типы врагов

#### Скелет

| Параметр         | Значение              |
|------------------|-----------------------|
| HP               | 30                    |
| Скорость         | 80 пикселей/сек       |
| Урон             | 10                    |
| Агро-радиус      | 150 пикселей          |
| Кулдаун атаки    | 1.0 сек               |
| Радиус атаки     | 20 пикселей (ближний бой) |
| Размер хитбокса  | 12×14 пикселей        |
| Визуал           | Белый прямоугольник 12×14 px, цвет (220, 220, 200) |

**Поведение:** Быстрый, слабый. Атакует ближним боем. Преследует игрока напрямую.

#### Зомби

| Параметр         | Значение              |
|------------------|-----------------------|
| HP               | 60                    |
| Скорость         | 40 пикселей/сек       |
| Урон             | 15                    |
| Агро-радиус      | 100 пикселей          |
| Кулдаун атаки    | 1.5 сек               |
| Радиус атаки     | 24 пикселя (ближний бой) |
| Размер хитбокса  | 14×16 пикселей        |
| Визуал           | Тёмно-зелёный прямоугольник 14×16 px, цвет (30, 100, 30) |

**Поведение:** Медленный, крепкий. Атакует ближним боем. Движется к игроку по прямой.

#### Лич

| Параметр         | Значение              |
|------------------|-----------------------|
| HP               | 40                    |
| Скорость         | 60 пикселей/сек       |
| Урон             | 20 (снаряд)           |
| Агро-радиус      | 200 пикселей          |
| Кулдаун атаки    | 2.0 сек               |
| Дальность стрельбы | 180 пикселей        |
| Предпочтительная дистанция | 120 пикселей (держит дистанцию) |
| Размер хитбокса  | 12×16 пикселей        |
| Визуал           | Фиолетовый прямоугольник 12×16 px, цвет (140, 40, 180) |

**Поведение:** Дальний бой. Стреляет магическими снарядами. Пытается держать дистанцию ~120 px от игрока. Если игрок подходит слишком близко (<60 px) — отступает.

**Снаряд лича:**
- Скорость: 160 пикселей/сек
- Размер: 6×6 пикселей
- Цвет: (180, 0, 255) — фиолетовый
- Время жизни: 2 сек (затем исчезает)
- Урон: 20

## 5. Боевая система

### 5.1. Атака игрока (меч)

1. Игрок нажимает ЛКМ
2. Проверяется кулдаун (0.5 сек с последней атаки)
3. Вычисляется направление от игрока к курсору
4. Создаётся зона поражения: сектор 90° в направлении курсора, радиус 40 px
5. Все враги в зоне поражения получают 25 урона
6. Проигрывается анимация взмаха (0.2 сек)

### 5.2. Атака врагов (ближний бой)

1. Враг находится в радиусе своей атаки от игрока
2. Проверяется кулдаун атаки врага
3. Игрок получает урон (10/15 в зависимости от типа врага)
4. Короткий эффект отталкивания: игрок сдвигается на 8 px от врага

### 5.3. Атака лича (дальний бой)

1. Лич обнаруживает игрока (агро-радиус 200 px)
2. Лич занимает позицию на дистанции ~120 px
3. Каждые 2 сек выпускает снаряд в направлении игрока
4. Снаряд летит прямолинейно со скоростью 160 px/сек
5. При попадании: 20 урона игроку, снаряд исчезает
6. Снаряд исчезает через 2 сек или при столкновении с препятствием

### 5.4. Смерть

- **Враг:** При HP ≤ 0 — исчезает, увеличивается счётчик убийств, через 5 сек респавн
- **Игрок:** При HP ≤ 0 — экран "GAME OVER", отображается счёт убийств, клавиша R для перезапуска

## 6. Визуальный стиль

### 6.1. Объекты (всё рисуется примитивами raylib)

| Объект         | Форма                          | Цвет (RGB)              |
|----------------|--------------------------------|--------------------------|
| Игрок          | Прямоугольник 14×16            | (0, 180, 0) — зелёный   |
| Меч            | Линия 12 px                    | (240, 240, 240) — белый  |
| Скелет         | Прямоугольник 12×14            | (220, 220, 200) — белый  |
| Зомби          | Прямоугольник 14×16            | (30, 100, 30) — тёмно-зелёный |
| Лич            | Прямоугольник 12×16            | (140, 40, 180) — фиолетовый |
| Снаряд лича    | Квадрат 6×6                    | (180, 0, 255) — ярко-фиолет. |
| Костёр         | 3 круга 4-8 px (анимация)      | (255, 160, 0) / (255, 100, 0) |
| Надгробие      | Прямоугольник 8×12             | (150, 150, 140) — серый  |
| Дерево (ствол) | Прямоугольник 6×12             | (80, 50, 20) — коричневый |
| Дерево (крона) | Круг радиус 10 px              | (20, 60, 20) — тёмно-зелёный |

### 6.2. Эффекты

- **Костёр:** 3 круга с разными радиусами (4, 6, 8 px), случайное смещение ±2 px каждый кадр, чередование оранжевого и жёлтого
- **Получение урона:** Мигание красным на 0.1 сек (цвет сущности → красный → обратно)
- **Смерть врага:** Мигание белым 3 раза за 0.3 сек, затем исчезновение
- **Взмах мечом:** Белая дуга 90° вокруг игрока за 0.2 сек

### 6.3. Освещение (упрощённое)

- Базовая яркость мира: 60% (тёмная атмосфера)
- Костёр: круг света радиусом 80 px, яркость 100%
- За пределами лагеря: градиентное затемнение к краям экрана

## 7. UI

### 7.1. HUD (всегда на экране)

| Элемент              | Позиция        | Описание                              |
|----------------------|----------------|---------------------------------------|
| HP бар               | Сверху слева (10, 10) | Красная полоска 200×20 px, рамка 1 px |
| Текст HP             | На HP баре     | "HP: 75/100" белым шрифтом 16 px      |
| Счётчик убийств      | Сверху справа (790, 10), выравнивание вправо | "Kills: 12" белым шрифтом 16 px |
| Мини-сообщения       | Снизу по центру (400, 560) | Исчезают через 2 сек, шрифт 14 px |

### 7.2. Мини-сообщения (события)

| Событие              | Текст                        | Цвет          |
|----------------------|------------------------------|---------------|
| Убийство скелета     | "Skeleton slain!"            | Белый         |
| Убийство зомби       | "Zombie destroyed!"          | Зелёный       |
| Убийство лича        | "Lich banished!"             | Фиолетовый    |
| Вход в лагерь        | "Safe zone - Regenerating..."| Жёлтый        |
| Выход из лагеря      | "Entering the darkness..."   | Красный       |
| Получение урона      | "-15 HP"                     | Красный       |

### 7.3. Экран Game Over

- Затемнение экрана (чёрный overlay 70% прозрачности)
- По центру: "GAME OVER" красным шрифтом 40 px
- Ниже: "Enemies slain: 12" белым шрифтом 24 px
- Ниже: "Press R to restart" серым шрифтом 18 px, мигание каждые 0.5 сек

## 8. Игровой цикл (Game Loop)

```
1. InitWindow(800, 600, "Dark Camp")
2. Загрузка/генерация карты
3. Спавн игрока в центре лагеря [25, 25]
4. Спавн врагов в случайных точках кладбища

Каждый кадр (60 FPS):
  5. Обработка ввода (WASD + мышь)
  6. Обновление позиции игрока (коллизии с тайлами)
  7. Обновление AI врагов:
     - Проверка агро-радиуса
     - Движение (патруль / преследование / отступление)
     - Атака (если в радиусе)
  8. Обновление снарядов лича (движение, коллизии)
  9. Проверка регенерации в лагере
  10. Обновление эффектов и анимаций
  11. Проверка смерти (игрок / враги)
  12. Респавн мёртвых врагов (таймер 5 сек)
  13. Отрисовка:
      a. Тайловая карта
      b. Декорации (деревья, надгробия, кости)
      c. Враги (сортировка по Y для правильного перекрытия)
      d. Игрок + меч
      e. Снаряды
      f. Эффекты (костёр, мигание)
      g. Освещение overlay
      h. HUD (HP, убийства, сообщения)
      i. Game Over экран (если игрок мёртв)
```

## 9. Структуры данных (ориентировочные)

```c
typedef struct Player {
    Vector2 position;      // мировые координаты
    int hp;
    int max_hp;
    float attack_cooldown;
    int kill_count;
    bool is_dead;
    float sword_angle;     // текущий угол меча (к курсору)
    bool is_attacking;     // анимация атаки
    float attack_timer;    // таймер анимации
} Player;

typedef enum EnemyType {
    ENEMY_SKELETON = 0,
    ENEMY_ZOMBIE,
    ENEMY_LICH
} EnemyType;

typedef enum EnemyState {
    ENEMY_PATROL = 0,
    ENEMY_CHASE,
    ENEMY_ATTACK,
    ENEMY_RETREAT,   // только для лича
    ENEMY_DEAD
} EnemyState;

typedef struct Enemy {
    EnemyType type;
    EnemyState state;
    Vector2 position;
    Vector2 spawn_point;
    int hp;
    int max_hp;
    float attack_cooldown;
    float respawn_timer;
    bool is_alive;
    float damage_flash;    // таймер мигания при уроне
} Enemy;

typedef struct Projectile {
    Vector2 position;
    Vector2 direction;
    float speed;
    float lifetime;
    int damage;
    bool active;
} Projectile;

typedef struct GameMessage {
    char text[64];
    Color color;
    float lifetime;        // исчезает через 2 сек
} GameMessage;

typedef enum TileType {
    TILE_GRASS = 0,
    TILE_CEMETERY,
    TILE_CAMP,
    TILE_TREE,
    TILE_WALL
} TileType;

typedef struct GameState {
    Player player;
    Enemy enemies[MAX_ENEMIES];     // MAX_ENEMIES = 15
    Projectile projectiles[MAX_PROJECTILES]; // MAX_PROJECTILES = 10
    TileType tilemap[MAP_SIZE][MAP_SIZE];    // MAP_SIZE = 50
    GameMessage messages[MAX_MESSAGES];      // MAX_MESSAGES = 5
    bool game_over;
} GameState;
```

## 10. Константы

```c
#define SCREEN_WIDTH        800
#define SCREEN_HEIGHT       600
#define TARGET_FPS          60
#define TILE_SIZE           32
#define MAP_SIZE            50
#define MAX_ENEMIES         15
#define MAX_PROJECTILES     10
#define MAX_MESSAGES        5

// Лагерь
#define CAMP_START          23
#define CAMP_END            27
#define CAMP_CENTER_X       25
#define CAMP_CENTER_Y       25
#define CAMP_REGEN_RATE     5.0f    // HP/сек

// Игрок
#define PLAYER_HP           100
#define PLAYER_SPEED        120.0f  // пикс/сек
#define PLAYER_ATTACK_DMG   25
#define PLAYER_ATTACK_RANGE 40.0f   // пикс
#define PLAYER_ATTACK_CD    0.5f    // сек
#define PLAYER_ATTACK_ARC   90.0f   // градусы
#define PLAYER_HITBOX_W     16
#define PLAYER_HITBOX_H     16

// Скелет
#define SKEL_HP             30
#define SKEL_SPEED          80.0f
#define SKEL_DAMAGE         10
#define SKEL_AGGRO          150.0f
#define SKEL_ATTACK_CD      1.0f
#define SKEL_ATTACK_RANGE   20.0f

// Зомби
#define ZOMB_HP             60
#define ZOMB_SPEED          40.0f
#define ZOMB_DAMAGE         15
#define ZOMB_AGGRO          100.0f
#define ZOMB_ATTACK_CD      1.5f
#define ZOMB_ATTACK_RANGE   24.0f

// Лич
#define LICH_HP             40
#define LICH_SPEED          60.0f
#define LICH_DAMAGE         20
#define LICH_AGGRO          200.0f
#define LICH_ATTACK_CD      2.0f
#define LICH_SHOOT_RANGE    180.0f
#define LICH_PREFERRED_DIST 120.0f
#define LICH_RETREAT_DIST   60.0f

// Снаряд
#define PROJ_SPEED          160.0f
#define PROJ_SIZE           6
#define PROJ_LIFETIME       2.0f

// Респавн
#define ENEMY_RESPAWN_TIME  5.0f
#define ENEMY_MIN_SPAWN_DIST 100.0f // от лагеря

// Эффекты
#define DAMAGE_FLASH_TIME   0.1f
#define DEATH_FLASH_TIME    0.3f
#define SWORD_SWING_TIME    0.2f
#define MESSAGE_LIFETIME    2.0f
#define KNOCKBACK_DIST      8.0f
```


---
## Verbatim: docs/RETROSPECTIVE.md (Russian)
# Ретроспектива: Dark Camp Prototype

## Участники
- **Team Lead** — координация, коммиты, контроль качества
- **Game Designer** — GDD
- **Architect** — архитектура кода
- **Core Developer** — ядро игры (game.h, map, player, render, main.c)
- **Enemy Developer** — враги, AI, боевая система
- **Sprite Artist** — генерация пиксель-арт спрайтшитов
- **Sprite Integrator** — интеграция текстур в рендер
- **Tester** — Lua тесты
- **Code Reviewer** — code review

## Что пошло хорошо

1. **Параллельная работа фаз** — GDD и архитектура писались одновременно, что сэкономило время. Core Developer и Sprite Artist тоже работали параллельно.

2. **Чёткие спецификации** — GDD с конкретными числами (HP, скорости, цвета RGB, размеры в пикселях) позволил разработчикам работать без дополнительных вопросов.

3. **Архитектура с заглушками** — Core Developer создал stubs для enemy.h/c и combat.h/c, что позволило собрать проект сразу. Enemy Developer потом заполнил заглушки реальным кодом без конфликтов.

4. **Тесты робастные** — 14 тестов не зависят от реализации врагов (assert enemy_count >= 0, а не == 20). Работали на каждом этапе: и с заглушками, и с полной реализацией.

5. **Zero-malloc архитектура** — статические массивы, нет утечек памяти, ASan/UBSan чистый.

6. **Code review нашёл реальные проблемы** — clang-tidy с неверным стандартом и архитектурное нарушение (player.c -> render.h).

7. **27/27 тестов** на каждом этапе — регрессий не было.

## Что пошло плохо

### CRITICAL: Тимлид не отследил интеграцию ассетов

**Проблема:** Sprite Artist создал 21 PNG файл, но тимлид не создал задачу на интеграцию спрайтов в рендер. Игра продолжала рисовать примитивами (DrawCircle), а спрайты просто лежали в assets/. Проблему заметил пользователь, а не тимлид.

**Причина:** Тимлид мыслил задачами ("создать спрайты" — готово!), но не отследил end-to-end поток (спрайты созданы → спрайты подключены → спрайты рендерятся).

**Урок:** При создании ассетов ВСЕГДА создавать парную задачу на интеграцию. Задача "создать спрайты" не завершена, пока они не отображаются в игре.

### HIGH: Sprite Artist проигнорировал обновление требований

**Проблема:** Тимлид отправил сообщение о необходимости анимированных спрайтшитов вместо одиночных кадров. Sprite Artist завершил задачу #7 с одиночными кадрами, не обработав обновление. Потребовалось 2 дополнительных сообщения и ручная проверка.

**Причина:** Сообщение пришло параллельно с завершением задачи. Агент не проверил inbox перед маркировкой задачи как completed.

**Урок:** Агенты должны проверять входящие сообщения ПЕРЕД маркировкой задачи как completed. Тимлид должен проверять deliverables перед принятием задачи (не верить на слово — смотреть файлы).

### MEDIUM: WASD клавиши не были в тестовом фреймворке

**Проблема:** raylib_tester.h регистрировал только KEY_LEFT/RIGHT/UP/DOWN, но игра использует WASD. Тестировщик нашёл это и использовал raw key codes (87, 65, 83, 68) как workaround.

**Причина:** Тестовый фреймворк был написан для предыдущего проекта с arrow keys. При смене управления на WASD никто не обновил фреймворк.

**Урок:** При изменении схемы управления — обновлять тестовый фреймворк в той же задаче. Архитектор должен включить это в план.

### LOW: tree.png остался 16x16 вместо 32x32

**Проблема:** Пользователь попросил деревья 32x32, но Sprite Artist сделал 16x16. Тимлид исправил вручную.

**Причина:** Сообщение об изменении размера пришло после основной работы и было потеряно.

**Урок:** Изменения требований должны идти через TaskUpdate (обновление описания задачи), а не только через сообщения.

## Метрики

| Метрика | Значение |
|---------|----------|
| Всего задач | 10 |
| Агентов задействовано | 9 |
| Коммитов | 8 |
| Тестов | 27/27 passed |
| Файлов исходного кода | 13 (.h + .c) |
| Спрайтов | 21 PNG |
| Критических багов в code review | 0 |
| Архитектурных замечаний | 2 (оба исправлены) |

## Правила на будущее

### Для тимлида:
1. **End-to-end мышление**: каждый ассет/артефакт должен быть НЕ ТОЛЬКО создан, но и ИНТЕГРИРОВАН. Создавай парные задачи (создание + интеграция).
2. **Verify deliverables**: не принимай задачу на слово — проверяй файлы, запускай билд, смотри скриншоты.
3. **Обновления требований**: изменения в требованиях фиксировать через TaskUpdate description, не только через сообщения.
4. **Регулярные коммиты**: коммитить после каждой завершённой задачи, не накапливать.

### Для агентов:
5. **Проверяй inbox перед завершением**: перед TaskUpdate(completed) прочитай входящие сообщения — могли прийти обновления.
6. **Тестовый фреймворк = часть задачи**: если меняешь input scheme — обнови и тесты и фреймворк.
7. **Не верь заглушкам**: если задача зависит от другой и та помечена completed, всё равно проверь реальное состояние файлов.

### Для архитектора:
8. **Планируй интеграцию**: в плане реализации должны быть не только "создать X" но и "подключить X к Y".
9. **Указывай зависимости тестового фреймворка**: если новые клавиши/переменные нужны для тестов — включи это в архитектуру.
