# News

The log at `/news/` is generated. It is not a blog engine. Home shows the three newest posts. A product page shows the posts tagged with that product.

## Add a post

1. Add one object to `data/news.json`.
2. Run `python3 tools/render_site.py`.
3. Commit the data file and the regenerated HTML.

Newest first. The renderer sorts by `datetime`. Do not invent an event or a time you do not have. If you only know the day, use `YYYY-MM-DD`. The page prints the date and no clock time. Those posts sort at noon Brisbane so they stay on that day.

Each post is rendered with the maker’s mark, the name TechGnomo, the time as the permalink, a status chip, and, when `product` is an announced slug, a small card in that product’s colours. Write the text as a person would say it. No pull-request numbers, commit ids, or time-zone notes.

```json
{
  "id": "short-unique-id",
  "datetime": "2026-09-28T09:00:00+10:00",
  "text": "One or two sentences.",
  "status": "UPDATE",
  "product": "clearmoneypath"
}
```

| Field | Required | Notes |
| --- | --- | --- |
| `id` | yes | Becomes the permalink `/news/#id`. Letters, numbers, hyphens. |
| `datetime` | yes | ISO 8601, with a Brisbane offset when you know the time. Date only when you do not. |
| `text` | yes | The whole post. Plain text. It is escaped. |
| `status` | no | `BUILDING`, `SHIPPING`, `UPDATE`, or `TEASER`. |
| `product` | no | A slug from `data/products.json`. The name links to that product. An unannounced slug is refused at render if it is not in the file, and an unannounced product does not get a public link. |
| `image` | no | Path under `/assets/`. Also set `imageAlt`, `imageWidth`, and `imageHeight`. |

Do not publish a teaser for a product that does not exist.

## Announce a product

Add an object to `data/products.json` with `"announced": true` and a `status` of `available`, `beta`, `coming-soon`, or `in-development`. Set `phrase` for the public line (ClearMoneyPath uses “Coming in 3 weeks”, with no exact date). Then add the theme the way `DESIGN.md` describes, and run the renderer.

GnomoRestaurant is not announced. Its theme file is the empty slot. Do not add a card for it.
