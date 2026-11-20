# Nona skills для Claude

Два скилла для подготовки генераций в Seedance и Kling:

| Скилл | Для чего |
|---|---|
| [`/nona-prompter`](nona-prompter/) | UGC и рекламные ролики: ТЗ → промпты персонажей, первых кадров и видео |
| [`/nona-microdrama`](nona-microdrama/) | Микродрамы и короткий метр: сценарий → кадры, карты, multi-shot промпты, 3D-раскадровка |

Оба скилла выдают результат в виде артефакта, интерактивной HTML-доски. Промпты в ней можно править, отмечать готовые генерации и делиться доской ссылкой.

## Установка

Нужен Claude Code: приложение Claude, вкладка Code, или CLI.

```bash
git clone https://github.com/fayzets/nona-skills.git
mkdir -p ~/.claude/skills
cp -R nona-skills/nona-prompter nona-skills/nona-microdrama ~/.claude/skills/
```

Перезапусти сессию. Скиллы появятся как `/nona-prompter` и `/nona-microdrama`.

Обновиться: `git pull` в папке репозитория и снова скопировать папки.
