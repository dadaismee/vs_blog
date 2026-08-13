# Годовой отчёт лаборатории

<style>
.lab-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 24px 0; }
.lab-grid.two { grid-template-columns: 1fr 1fr; }
@media (max-width: 700px) { .lab-grid, .lab-grid.two { grid-template-columns: 1fr; } }
.lab-card { background: #f5f5f5; border-left: 3px solid #00f; padding: 16px 20px; border-radius: 6px; }
.lab-card.center { text-align: center; border-left: none; }
.lab-card h3 { margin: 0 0 8px; font-size: 15px; }
.lab-card ul { margin: 0; padding-left: 20px; }
.lab-card li { margin-bottom: 6px; font-size: 14px; }
.lab-metric { font-size: 20px; font-weight: 600; color: #00f; }
.lab-label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; color: #666; }
.lab-tag { display: inline-block; background: #eef2ff; color: #00f; padding: 4px 10px; border-radius: 4px; font-size: 13px; margin: 0 4px 8px 0; }
.lab-cta { display: inline-block; padding: 12px 24px; background: #00f; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; margin: 24px 8px 0 0; }
.lab-cta.secondary { background: transparent; color: #00f; border: 1px solid #00f; }
</style>

Научно-исследовательская лаборатория федерального вуза собирала годовой отчёт вручную по три месяца каждый год. Форматирование, вёрстка и вставка библиографии зависели от навыков одного человека.

Я спроектировал и внедрил систему, где текст, картинки, ссылки на литературу и шаблоны оформления разделены, а итоговый документ собирается автоматически.

<div class="lab-grid">
<div class="lab-card center">
<div class="lab-metric">3 мес → 3 дня</div>
<div class="lab-label">Время сборки отчёта</div>
</div>
<div class="lab-card center">
<div class="lab-metric">на 80% меньше ошибок</div>
</div>
<div class="lab-card center">
<div class="lab-metric">5 → 2 итерации</div>
<div class="lab-label">Правок после внедрения</div>
</div>
</div>

<!-- | ❌ Было | ✅ Стало | -->
<!-- |---|---| -->
<!-- | Координатор вручную собирает, верстает и проверяет отчёт | Отчёт собирается автоматически из текстов авторов | -->
<!-- | Сборка 3 месяца | Сборка одной командой | -->
<!-- | Плавающее форматирование, потерянные ссылки | Zotero + BetterBibTeX → единая библиография | -->
<!-- | Правки до последнего дня перед сдачей | Pandoc собирает PDF по ГОСТу 7.32-2017 одной командой | -->
<!-- |  | Git — история изменений, никаких потерь | -->



## Демо: как работает автор

<video src="/assets/lab.mp4" controls="" style="width:100%; max-width:720px;"></video>


## Как это меняет работу

| | До: автор — верстальщик | После: автор — исследователь |
|---|---|---|
| **Подготовка** | Пишет текст и оформляет заголовки, списки, таблицы | Пишет текст, оформление автоматизировано |
| **Библиография** | Оформляет по ГОСТ вручную | Вставляет ключи цитирования `[@author2026]` — библиография по ГОСТ собирается сама |
| **Оформление** | Сдаёт файл → координатор перепроверяет | Титульный, нумерация, ГОСТ-библиография — автоматически |
| **Правки** | Правки возвращаются 3–5 раз | Закончил писать → автоматически готов DOCX/PDF |

<div style="display: flex;">
<a href="https://github.com/dadaismee/lab-demo" class="lab-cta secondary" target="_blank">Код проекта на GitHub</a>
<a href="https://calendar.app.google/vZyjjXtrXN5Sb2JN8" target="_blank"class="lab-cta">Обсудить пилот для вашей компании</a>
</div>
