# Nona skills для Claude

Два скилла для подготовки генераций в Seedance и Kling:

| Скилл | Для чего |
|---|---|
| [`/nona-prompter`](nona-prompter/) | UGC и рекламные ролики: ТЗ → промпты персонажей, первых кадров и видео |
| [`/nona-microdrama`](nona-microdrama/) | Микродрамы и короткий метр: сценарий → кадры, карты, multi-shot промпты, 3D-раскадровка |

Оба скилла выдают результат в виде артефакта, интерактивной HTML-доски. Промпты в ней можно править, отмечать готовые генерации и делиться доской ссылкой.

## Установка в Claude Code

Подходит и приложение Claude (вкладка Code), и CLI.

```bash
git clone https://github.com/fayzets/nona-skills.git
mkdir -p ~/.claude/skills
cp -R nona-skills/nona-prompter nona-skills/nona-microdrama ~/.claude/skills/
```

Перезапусти сессию. Скиллы появятся как `/nona-prompter` и `/nona-microdrama`.

Обновиться: `git pull` в папке репозитория и снова скопировать папки.

## Codex и другие агенты

Скиллы написаны в формате Agent Skills, поэтому их можно положить в папку скиллов Codex (`~/.codex/skills/`) или другого агента:

```bash
mkdir -p ~/.codex/skills
cp -R nona-skills/nona-prompter nona-skills/nona-microdrama ~/.codex/skills/
```

Без Claude доска собирается в один HTML-файл, который открывается двойным кликом. Отличия от Claude:

- правки сохраняются в браузере, а не по ссылке;
- кнопка «Скачать HTML» скачивает доску со всеми правками одним файлом: его можно переслать или отдать агенту;
- кнопка «Скачать data.json» скачивает только данные проекта;
- нет режима «только просмотр»: доску видит и правит тот, у кого файл.

Сборка и обратная распаковка — `scripts/nona_embed.py` (`build` / `extract`), агент запускает её сам по инструкции в `SKILL.md`.
