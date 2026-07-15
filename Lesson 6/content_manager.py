materials_queue = [
    {"title": "Алгебра: База", "status": "published"},
    {"title": "Планіметрія", "status": "draft"},
    {"title": "Вектори", "status": "published"},
    {"title": "Теорія ймовірностей", "status": "archived"},
    {"title": "Стереометрія", "status": "published"}
]
for topic in materials_queue:
    if topic['status'] == "draft":
        continue
    elif topic['status'] == "archived":
        break
    else:
        print(f"Опубліковано на платформі: {topic['title']}")
print("Обробку черги завершено.")